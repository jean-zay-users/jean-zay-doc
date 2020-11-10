# [PyTorch STL10 example script](https://github.com/jean-zay-users/jean-zay-doc/tree/master/docs/examples/pytorch/distributed_stl10)

stl10_example.py is based on [https://github.com/pytorch/examples/tree/master/imagenet](https://github.com/pytorch/examples/tree/master/imagenet).

## Slurm configuration

By default we use the following configuration. 

```bash
#!/bin/bash
#SBATCH --job-name=pytorch_stl10     # job name
#SBATCH --ntasks=2                   # number of MP tasks
#SBATCH --ntasks-per-node=1          # number of MPI tasks per node
#SBATCH --gres=gpu:1                 # number of GPUs per node
#SBATCH --cpus-per-task=10           # number of cores per tasks
#SBATCH --hint=nomultithread         # we get physical cores not logical
#SBATCH --time=00:10:00              # maximum execution time (HH:MM:SS)
#SBATCH --output=pytorch_stl10%j.out # output file name
#SBATCH --error=pytorch_stl10%j.err  # error file name
```

This configuration will start a distributed training on two nodes with one GPU
each. 

You can change the `ntasks`, `ntasks-per-node` and `gres` options to modify
this behaviour. In this context, `ntasks` corresponds to the total number of
GPUs you want to use (world size), while `ntasks-per-node` and `gres` describe
the number of local GPUs on each node.

For example, the following configuration will launch a distributed training
with one node and two GPUs:

```bash
#!/bin/bash
#SBATCH --job-name=pytorch_stl10     # job name
#SBATCH --ntasks=2                   # number of MP tasks
#SBATCH --ntasks-per-node=2          # number of MPI tasks per node
#SBATCH --gres=gpu:2                 # number of GPUs per node
#SBATCH --cpus-per-task=10           # number of cores per tasks
#SBATCH --hint=nomultithread         # we get physical cores not logical
#SBATCH --time=00:10:00              # maximum execution time (HH:MM:SS)
#SBATCH --output=pytorch_stl10%j.out # output file name
#SBATCH --error=pytorch_stl10%j.err  # error file name
```

And this one will use two entire nodes (4 GPUs per node on the default Slurm
partition):

```bash
#!/bin/bash
#SBATCH --job-name=pytorch_stl10     # job name
#SBATCH --ntasks=8                   # number of MP tasks
#SBATCH --ntasks-per-node=4          # number of MPI tasks per node
#SBATCH --gres=gpu:4                 # number of GPUs per node
#SBATCH --cpus-per-task=10           # number of cores per tasks
#SBATCH --hint=nomultithread         # we get physical cores not logical
#SBATCH --time=00:10:00              # maximum execution time (HH:MM:SS)
#SBATCH --output=pytorch_stl10%j.out # output file name
#SBATCH --error=pytorch_stl10%j.err  # error file name
```

You can then launch the job with:
```
cd jean-zay-doc/examples/pytorch/distributed_stl10/
sbatch ./pytorch_distributed_stl10_example.sh
```
