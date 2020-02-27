# Tensorflow example script

To run this script you will need to first install click in your environment.
```
module load python/3.7.5 &&\
pip install click
```

Then you need to clone the jean-zay repo in your `$WORK` dir:
```
cd $WORK &&\
git clone https://github.com/jean-zay-users/jean-zay-doc.git
```

Finally you can just launch the batch job (single GPU) via:
```
sbatch jean-zay-doc/tf-example/mnist_submission_script.slurm
```
