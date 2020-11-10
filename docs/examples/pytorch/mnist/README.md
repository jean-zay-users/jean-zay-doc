# [Pytorch MNIST example script](https://github.com/jean-zay-users/jean-zay-doc/tree/master/docs/examples/pytorch/mnist)

You can launch the batch job (single GPU version) via:
```
cd jean-zay-doc/docs/examples/pytorch/mnist/
sbatch ./pytorch_example_script.sh
```

Alternatively, a multi GPU version is available. It launches the training with
10 different values for a single parameter. In SLURM language this is called a
*job array*.

This script implements a kind of parallelism (when data is not shared between
different jobs). It can be useful to optimize the values of the hyperparameters
during the training:

```
cd jean-zay-doc/docs/examples/pytorch/mnist/
sbatch ./pytorch_example_script_multigpu.sh
```
