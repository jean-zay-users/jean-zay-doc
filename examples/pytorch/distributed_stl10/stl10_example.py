import os
import time
import subprocess
import torch
import argparse

import torch.nn as nn
import torch.distributed as dist
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models

from typing import Tuple
from torch.optim import SGD
from torch.optim.optimizer import Optimizer
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
from torch.nn.parallel import DistributedDataParallel


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val: float, n: int = 1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def accuracy(output: torch.Tensor,
             target: torch.Tensor,
             topk: Tuple[int] = (1,)):
    """Computes the precision@k for the specified values of k"""
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size))
        return res


def reduce_tensor(tensor: torch.Tensor, world_size: int):
    """Reduce tensor across all nodes."""
    rt = tensor.clone()
    dist.all_reduce(rt, op=dist.reduce_op.SUM)
    rt /= world_size
    return rt


def to_python_float(t: torch.Tensor):
    if hasattr(t, 'item'):
        return t.item()
    else:
        return t[0]


def train(train_loader: DataLoader,
          model: nn.Module,
          criterion: nn.Module,
          optimizer: Optimizer,
          epoch: int,
          world_size: int,
          is_master: bool,
          log_interval: int = 100):
    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()
    top5 = AverageMeter()

    # switch to train mode
    model.train()

    end = time.time()
    for i, (input, target) in enumerate(train_loader):

        # measure data loading time
        data_time.update(time.time() - end)

        # Create non_blocking tensors for distributed training
        input = input.cuda(non_blocking=True)
        target = target.cuda(non_blocking=True)

        # compute output
        logits = model(input)
        loss = criterion(logits, target)

        # compute gradients in a backward pass
        optimizer.zero_grad()
        loss.backward()

        # Call step of optimizer to update model params
        optimizer.step()

        if i % log_interval == 0:
            # Every log_freq iterations, check the loss, accuracy, and speed.
            # For best performance, it doesn't make sense to print these metrics every
            # iteration, since they incur an allreduce and some host<->device syncs.

            # Measure accuracy
            prec1, prec5 = accuracy(logits.data, target.data, topk=(1, 5))

            # Average loss and accuracy across processes for logging
            reduced_loss = reduce_tensor(loss.data, world_size)
            prec1 = reduce_tensor(prec1, world_size)
            prec5 = reduce_tensor(prec5, world_size)

            # to_python_float incurs a host<->device sync
            batch_size = input[0].size(0)
            losses.update(to_python_float(reduced_loss), batch_size)
            top1.update(to_python_float(prec1), batch_size)
            top5.update(to_python_float(prec5), batch_size)

            torch.cuda.synchronize()
            batch_time.update((time.time() - end) / log_interval)
            end = time.time()

            # Only the first node should log infos.
            if is_master:
                print(
                    f"Epoch: [{epoch}][{i}/{len(train_loader)}]\t"
                    f"Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t"
                    f"Speed {world_size * batch_size / batch_time.val:.3f} ({world_size * batch_size / batch_time.avg:.3f})\t"
                    f"Loss {loss.val:.10f} ({loss.avg:.4f})\t"
                    f"Prec@1 {top1.val:.3f} ({top1.avg:.3f})\t"
                    f"Prec@5 {top5.val:.3f} ({top5.avg:.3f})"
                )


def adjust_learning_rate(initial_lr: float,
                         optimizer: Optimizer,
                         epoch: int):
    """Sets the learning rate to the initial LR decayed by 10 every 30 epochs"""
    lr = initial_lr * (0.1 ** (epoch // 30))
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


def validate(val_loader: DataLoader,
             model: nn.Module,
             criterion: nn.Module,
             world_size: int,
             is_master: bool,
             log_freq: int = 100):
    batch_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()
    top5 = AverageMeter()

    # switch to evaluate mode
    model.eval()

    with torch.no_grad():
        end = time.time()
        for i, (input, target) in enumerate(val_loader):

            input = input.cuda(non_blocking=True)
            target = target.cuda(non_blocking=True)

            with torch.no_grad():
                # compute output
                logits = model(input)
                loss = criterion(logits, target)

            # Measure accuracy
            prec1, prec5 = accuracy(logits.data, target.data, topk=(1, 5))

            # Average loss and accuracy across processes for logging
            reduced_loss = reduce_tensor(loss.data, world_size)
            prec1 = reduce_tensor(prec1, world_size)
            prec5 = reduce_tensor(prec5, world_size)

            # to_python_float incurs a host<->device sync
            batch_size = input[0].size(0)
            losses.update(to_python_float(reduced_loss), batch_size)
            top1.update(to_python_float(prec1), batch_size)
            top5.update(to_python_float(prec5), batch_size)

            torch.cuda.synchronize()
            batch_time.update((time.time() - end) / log_freq)
            end = time.time()

            if i % log_freq == 0 and is_master:
                # Only the first node should log infos.
                print(
                    f"Test: [{i}/{len(val_loader)}]\t"
                    f"Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t"
                    f"Speed {world_size * batch_size / batch_time.val:.3f} ({world_size * batch_size / batch_time.avg:.3f})\t"
                    f"Loss {loss.val:.10f} ({loss.avg:.4f})\t"
                    f"Prec@1 {top1.val:.3f} ({top1.avg:.3f})\t"
                    f"Prec@5 {top5.val:.3f} ({top5.avg:.3f})"
                )

        if is_master:
            print(f' * Prec@1 {top1.avg:.3f} Prec@5 {top5.avg:.3f}')

    return top1.avg


def run(batch_size: int,
        epochs: int,
        learning_rate: float,
        log_interval: int,
        save_model: bool):
    # number of nodes / node ID
    node_id = int(os.environ['SLURM_NODEID'])

    # local rank on the current node / global rank
    local_rank = int(os.environ['SLURM_LOCALID'])
    global_rank = int(os.environ['SLURM_PROCID'])

    # number of processes
    world_size = int(os.environ['SLURM_NTASKS'])

    # define master address and master port
    hostnames = subprocess.check_output(['scontrol', 'show', 'hostnames', os.environ['SLURM_JOB_NODELIST']])
    master_addr = hostnames.split()[0].decode('utf-8')

    # set environment variables for 'env://'
    os.environ['MASTER_ADDR'] = master_addr
    os.environ['WORLD_SIZE'] = str(world_size)
    os.environ['RANK'] = str(global_rank)

    # define whether this is the master process
    is_master = node_id == 0 and local_rank == 0

    # set GPU device
    torch.cuda.set_device(local_rank)

    print("Initializing PyTorch distributed ...")
    torch.distributed.init_process_group(
        init_method='env://',
        backend='nccl',
    )

    print("Initialize Model...")
    # Construct Model
    model = models.resnet18(pretrained=False, num_classes=10).cuda()
    # Make model DistributedDataParallel
    model = DistributedDataParallel(model, device_ids=[local_rank], output_device=local_rank)

    # define loss function (criterion) and optimizer
    criterion = nn.CrossEntropyLoss().cuda()
    optimizer = SGD(model.parameters(), learning_rate, momentum=0.9, weight_decay=1e-4)

    print("Initialize Dataloaders...")
    transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize(mean=[0.485, 0.456, 0.406],
                              std=[0.229, 0.224, 0.225])])

    # Initialize Datasets.
    trainset = datasets.STL10(root=os.environ["SCRATCH"], split='train', download=False, transform=transform)
    valset = datasets.STL10(root=os.environ["SCRATCH"], split='test', download=False, transform=transform)

    # Create DistributedSampler to handle distributing the dataset across nodes
    # This can only be called after torch.distributed.init_process_group is called
    train_sampler = DistributedSampler(trainset)
    val_sampler = DistributedSampler(valset)

    # Create the Dataloaders to feed data to the training and validation steps
    train_loader = DataLoader(trainset,
                              batch_size=batch_size,
                              num_workers=10,
                              sampler=train_sampler,
                              pin_memory=True)
    val_loader = DataLoader(valset,
                            batch_size=batch_size,
                            num_workers=10,
                            sampler=val_sampler,
                            pin_memory=True)

    best_prec1 = 0

    for epoch in range(epochs):
        # Set epoch count for DistributedSampler.
        # We don't need to set_epoch for the validation sampler as we don't want
        # to shuffle for validation.
        train_sampler.set_epoch(epoch)

        # Adjust learning rate according to schedule
        adjust_learning_rate(learning_rate, optimizer, epoch)

        # train for one epoch
        train(train_loader, model, criterion, optimizer, epoch, world_size, is_master, log_interval)

        # evaluate on validation set
        prec1 = validate(val_loader, model, criterion, world_size, is_master)

        # remember best prec@1 and save checkpoint if desired
        if prec1 > best_prec1:
            best_prec1 = prec1
            if is_master and save_model:
                torch.save(model.state_dict(), "stl10_resnet18.pt")

        if is_master:
            print("Epoch Summary: ")
            print(f"\tEpoch Accuracy: {prec1}")
            print(f"\tBest Accuracy: {best_prec1}")


if __name__ == "__main__":
    # Training settings
    parser = argparse.ArgumentParser(description='PyTorch STL10 Example')
    parser.add_argument('--batch-size', type=int, default=64, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--epochs', type=int, default=14, metavar='N',
                        help='number of epochs to train (default: 14)')
    parser.add_argument('--lr', type=float, default=.1, metavar='LR',
                        help='learning rate (default: .1)')
    parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                        help='how many batches to wait before logging training status')
    parser.add_argument('--save-model', action='store_true', default=False,
                        help='For Saving the current Model')
    args = parser.parse_args()

    run(batch_size=args.batch_size,
        epochs=args.epochs,
        learning_rate=args.lr,
        log_interval=args.log_interval,
        save_model=args.save_model)
