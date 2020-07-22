#!/bin/bash
#SBATCH --job-name=pytorch_stl10     # job name
#SBATCH --ntasks=2                   # number of MP tasks
#SBATCH --ntasks-per-node=1          # number of MPI tasks per node
#SBATCH --gres=gpu:1                 # number of GPUs per node
#SBATCH --cpus-per-task=10           # number of cores per tasks
#SBATCH --hint=nomultithread         # we get physical cores not logical
#SBATCH --time=03:00:00              # maximum execution time (HH:MM:SS)
#SBATCH --output=pytorch_stl10%j.out # output file name
#SBATCH --error=pytorch_stl10%j.err  # error file name

set -x
cd $WORK/jean-zay-doc/examples/pytorch/distributed_stl10

module purge
module load pytorch-gpu/py3/1.5.0

srun python ./stl10_example.py
