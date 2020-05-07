#!/bin/bash
#SBATCH --job-name=tf_mnist_multi_gpus     # job name
#SBATCH --ntasks=2                   # number of MP tasks
#SBATCH --ntasks-per-node=2          # number of MPI tasks per node
#SBATCH --gres=gpu:2                 # number of GPUs per node
#SBATCH --cpus-per-task=10           # number of cores per tasks
# /!\ Caution, in the following line, "multithread" refers to hyperthreading.
#SBATCH --hint=nomultithread         # we get physical cores not logical
#SBATCH --distribution=block:block   # we pin the tasks on contiguous cores
#SBATCH --time=3:00:00              # maximum execution time (HH:MM:SS)
#SBATCH --output=tf_mnist_multi_gpus%j.out # output file name
#SBATCH --error=tf_mnist_multi_gpus%j.out  # error file name
#SBATCH --qos=qos_gpu-dev         # we are submitting a test job

set -x
cd $WORK/jean-zay-doc/examples/tf

module purge
module load tensorflow-gpu/py3/2.1.0

srun --multi-prog ./mpmd_multi_gpu.conf

wait
