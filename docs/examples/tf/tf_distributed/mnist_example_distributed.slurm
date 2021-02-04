#!/bin/bash
#SBATCH --job-name=mnist_tf_distributed     # job name
#SBATCH --nodes=2                 # number of nodes
#SBATCH --ntasks-per-node=1         # number of MPI task per node
#SBATCH --gres=gpu:4                # number of GPUs per node
#SBATCH --cpus-per-task=40          # since nodes have 40 cpus
#SBATCH --hint=nomultithread         # we get physical cores not logical
#SBATCH --distribution=block:block  # distribution, might be better to have contiguous blocks
#SBATCH --time=01:00:00             # job length
#SBATCH --output=mnist_tf_distr_log_%j.out  # std out
#SBATCH --error=mnist_tf_distr_log_%j.out   # std err
#SBATCH --exclusive                 # we reserve the entire node four our job
#SBATCH --qos=qos_gpu-dev         # we are submitting a test job
#SBATCH -A changeme@gpu

set -x
cd ${SLURM_SUBMIT_DIR}

module purge
module load tensorflow-gpu/py3/2.4.0

srun python ./mnist_example.py
