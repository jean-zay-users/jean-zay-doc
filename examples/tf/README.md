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
Notice that this time you need to use the python module with tensorflow loaded, because [dask will
by default use the same python for the worker as the one you used for the
scheduler](https://jobqueue.dask.org/en/latest/debug.html).
See this [GitHub issue](https://github.com/dask/dask-jobqueue/issues/408) for more information.
```
module load tensorflow-gpu/py3/2.1.0 &&\
pip install click dask-jobqueue
```

You can then do:
```
python jean-zay-doc/examples/tf/dask_script.py 64
```

where 64 is the batch size you want to run the mnist example with.
If you want multiple batch sizes just have them space-separated.

Be sure to load the tensorflow module before launching the dask script because otherwise Tensorflow will not be loaded.
This is because the python executable used to launch the dask worker is the same as the one used to launch the scheduler by default.
You can set it otherwise in the cluster if you want something more tailored.
