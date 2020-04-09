# Tensorflow example script

To run the examples you will need to first install `click` in your environment.
```
module load python/3.7.5 &&\
pip install click
```

Then you need to clone the jean-zay repo in your `$WORK` dir:
```
cd $WORK &&\
git clone https://github.com/jean-zay-users/jean-zay-doc.git
```

## Classical examples

For the single GPU job you can do:
```
sbatch jean-zay-doc/examples/tf/mnist_submission_script.slurm
```

For the multi GPU job you can do:
```
sbatch jean-zay-doc/examples/tf/mnist_submission_script_multi_gpus.slurm
```

## Dask example

To run the dask example you will need to install `dask-jobqueue` in your environment additionally.
```
module load python/3.7.5 &&\
pip install click dask-jobqueue
```

You can then do:
```
python jean-zay-doc/examples/tf/dask_script.py
```
