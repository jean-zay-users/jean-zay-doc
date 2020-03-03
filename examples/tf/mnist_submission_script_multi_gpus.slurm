#!/bin/bash
#SBATCH --job-name=tf_mnist_multi_gpus     # nom du job
#SBATCH --ntasks=2                   # nombre de tâche MPI
#SBATCH --ntasks-per-node=2          # nombre de tâche MPI par noeud
#SBATCH --gres=gpu:2                 # nombre de GPU à réserver par nœud
#SBATCH --cpus-per-task=10           # nombre de coeurs à réserver par tâche
# /!\ Attention, la ligne suivante est trompeuse mais dans le vocabulaire
# de Slurm "multithread" fait bien référence à l'hyperthreading.
#SBATCH --hint=nomultithread         # on réserve des coeurs physiques et non logiques
#SBATCH --distribution=block:block   # on épingle les tâches sur des coeurs contigus
#SBATCH --time=3:00:00              # temps d’exécution maximum demande (HH:MM:SS)
#SBATCH --output=tf_mnist_multi_gpus%j.out # nom du fichier de sortie
#SBATCH --error=tf_mnist_multi_gpus%j.out  # nom du fichier d'erreur (ici commun avec la sortie)

set -x
cd $WORK/jean-zay-doc/examples/tf

module purge
module load python/3.7.5
module load tensorflow-gpu/py3/2.1.0

srun --ntasks=1 python ./mnist_example.py -gpus 0&
srun --ntasks=1 python ./mnist_example.py -gpus 1&

wait
