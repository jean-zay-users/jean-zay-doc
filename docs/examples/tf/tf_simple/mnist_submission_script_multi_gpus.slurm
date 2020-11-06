#!/bin/bash
#SBATCH --job-name=tf_mnist_multi_gpus     # job name
#SBATCH --ntasks=1                   # number of MP tasks
#SBATCH --ntasks-per-node=1          # number of MPI tasks per node
#SBATCH --gres=gpu:1                 # number of GPUs per node
#SBATCH --cpus-per-task=10           # number of cores per tasks
# /!\ Caution, in the following line, "multithread" refers to hyperthreading.
#SBATCH --hint=nomultithread         # we get physical cores not logical
#SBATCH --distribution=block:block   # we pin the tasks on contiguous cores
#SBATCH --time=3:00:00              # maximum execution time (HH:MM:SS)
#SBATCH --output=tf_mnist_multi_gpus%A_%a.out # output file name
#SBATCH --error=tf_mnist_multi_gpus%A_%a.out  # error file name
#SBATCH --array=0-1            # one job array with 2 jobs
#SBATCH --qos=qos_gpu-dev         # we are submitting a test job

set -x
cd ${SLURM_SUBMIT_DIR}

# no particular option here but you could imagine it being different parameters,
# for example for running two jobs with differente learning rates (0.1 and 1):
# opt[0]="0.1"
# opt[1]="1"
opt[0]=""
opt[1]=""

module purge
module load tensorflow-gpu/py3/2.1.0

srun python ./mnist_example.py ${opt[$SLURM_ARRAY_TASK_ID]}

wait
