# [Weights&Biases - Hydra](https://github.com/jean-zay-users/jean-zay-doc/tree/master/docs/examples/tf/tf_wandb_hydra)

Weights&Biases and Hydra are 2 tools used in Machine Learning Projects.
Weights&Biases allows you to easily save a lot of information about your different experiments in the cloud, like meta data, system data, model weights and of course your different metrics and logs.
Hydra is a configuration management tool that allows you to build command line interfaces and create robust and readable configuration files.
These 2 tools can be used together very elegantly and easily, but their setup on Jean Zay is not straightforward.
In this example, we will show you how to setup both tools on Jean Zay in a TensorFlow example.

## Installation

To run this example, you need to clone the jean-zay repo in your `$WORK` dir:
```
cd $WORK &&\
git clone https://github.com/jean-zay-users/jean-zay-doc.git
```

You can then install the requirements:
```
module purge
module load tensorflow-gpu/py3/2.6.0
pip install --user -r $WORK/jean-zay-doc/docs/examples/tf/tf_wandb_hydra/requirements.txt
```

## Run
In order to run the example on SLURM you can just issue the following command from the example directory:
```
python train_mnist.py --multirun hydra/launcher=base +hours=1
```

### SLURM parametrization
Different parameters can be set for the SLURM job, using the `hydra.launcher` config group.
For example to launch a longer job, you can use:
```
python train_mnist.py --multirun hydra/launcher=base +hours=10 hydra.launcher.qos='qos_gpu-t3'
```

If you want to use more gpus:
```
python train_mnist.py --multirun hydra/launcher=base +hours=10 hydra.launcher.qos='qos_gpu-t3' hydra.launcher.gpus_per_node=4
```

### Weights&Biases
This will require you to create a [Weights&Biases account](https://wandb.ai/).
`wandb` is run offline because the compute nodes are not connected to the internet.
In order to have the results uploaded to the cloud, you need to manually sync them using the `wandb sync run_dir` command.
The run directories are located in `$SCRATCH/wandb/jean-zay-doc`, but this can be changed using the `wandb.dir` config variable.
You can also run a script to sync the runs before they are finished on a front node, for example using the script [here](https://gist.github.com/zaccharieramzi/3e1abc67aefac106ede2883c56ac8e1a).

### Hydra and submitit outputs
The outputs created by Hydra and submitit are located in the `multirun` directory.
You can change this value by setting the `hydra.dir` config variable.

### Batch jobs
In order to batch multiple similar jobs you can use the sweep feature of Hydra.
For example, if you want to run multiple training with different batch sizes, you can do the following:
```
python train_mnist.py --multirun hydra/launcher=base +hours=1 fit.batch_size=32,64,128
```

This can be extended to the grid search of a Cartesian product for example:
```
python train_mnist.py --multirun hydra/launcher=base +hours=1 fit.batch_size=32,64,128 compile.optimizer=rmsprop,adam
```

## Similar resources

- [slurm-hydra-submitit](https://github.com/RaphaelMeudec/slurm-hydra-submitit) presents a similar concept in a more general case for any SLURM cluster, without W&B. In particular, it specifies [how to run specific parameters combinations grid search](https://github.com/RaphaelMeudec/slurm-hydra-submitit#specific-parameters-combinations).
- [jz-hydra-submitit-launcher](https://github.com/zaccharieramzi/jz-hydra-submitit-launcher) a pip installable (`pip install jz-hydra-submitit-launcher`) custom launcher that has the correct default for JZ, and several default configurations:
```
hydra-submitit-launch train_mnist.py dev hydra.launcher.setup=\["'#SBATCH -C v100-32g'","'export WANDB_MODE=offline'"\]
```


## References
- Weights&Biases: https://wandb.ai/site
- Hydra: https://hydra.cc/
- Submitit: https://github.com/facebookincubator/submitit
- Hydra submitit launcher: https://hydra.cc/docs/plugins/submitit_launcher/

## Alternatives

To Weights&Biases:
- MLFlow
- Tensorboard

To Hydra:
- argparse
- click