#!/bin/bash
# This job will run 32 MPI process on 8 nodes, each node will host 4 MPI process, each one pinned on a GPU.
#SBATCH --job-name=toto             # job name
#SBATCH --ntasks=32                 # number of MPI task
#SBATCH --ntasks-per-node=4         # number of MPI task per node
#SBATCH --gres=gpu:4                # number of GPUs per node
#SBATCH --cpus-per-task=10          # since nodes have 40 cpus, we tell slurm to allocate 1/4 of the node resources (i.e. 10)
#SBATCH --distribution=block:block  # distribution, might be better to have contiguous blocks
#SBATCH --time=20:00:00             # job length
#SBATCH --output=toto_log_%j.out    # std out
#SBATCH --error=toto_log_%j.out     # std err
#SBATCH --exclusive                 # we reserve the entire node four our job
#### >> Add SBATCH instructions for QoS, Partitions, Account, etc << ###
 
cd ${SLURM_SUBMIT_DIR}

# Modules (03/2020)
module load cudnn/10.1-v7.5.1.10
module load nccl/2.4.2-1+cuda10.1
module load tensorflow-gpu/py3/1.14-openmpi

# Show comands
set -x

# Execution
srun --mpi=pmix python ~/your_stuff.py
