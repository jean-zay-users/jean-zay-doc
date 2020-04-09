#!/bin/bash
#SBATCH --job-name=tf_mnist     # job name
#SBATCH --ntasks=1                   # number of MP tasks
#SBATCH --ntasks-per-node=1          # number of MPI tasks per node
#SBATCH --gres=gpu:1                 # number of GPUs per node
#SBATCH --cpus-per-task=10           # number of cores per tasks
# /!\ Caution, in the following line, "multithread" refers to hyperthreading.
#SBATCH --hint=nomultithread         # we get physical cores not logical
#SBATCH --distribution=block:block   # we pin the tasks on contiguous cores
#SBATCH --time=3:00:00              # maximum execution time (HH:MM:SS)
#SBATCH --output=tf_mnist%j.out # output file name
#SBATCH --error=tf_mnist%j.out  # error file name
#SBATCH --qos=qos_gpu-t4         # we are submitting a test job

set -x
cd $WORK/jean-zay-doc/examples/tf

module purge
module load tensorflow-gpu/py3/2.1.0

srun python ./mnist_example.py -s&

wait
