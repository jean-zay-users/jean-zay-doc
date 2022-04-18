#!/bin/bash
#SBATCH --partition=prepost
#SBATCH --account=your_account
#SBATCH --job-name=xarray
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --hint=nomultithread
#SBATCH --time=20:00:00
#SBATCH --output=xarray_%j.out
#SBATCH --error=xarray_%j.out

cd /path/to/your/scratch/folder

# Loading module
module purge
module load anaconda-py3/2021.05

# change the path to your own conda environment
conda activate /path/to/conda/environment
echo `which python`

python example.py