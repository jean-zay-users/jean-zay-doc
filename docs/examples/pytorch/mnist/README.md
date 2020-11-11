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

This is the example script (`mnist_example.py`):

{{code_from_file("examples/pytorch/mnist/mnist_example.py", "python")}}

And the launching script for a single GPU version (`pytorch_example_script.sh`):

{{code_from_file("examples/pytorch/mnist/pytorch_example_script.sh", "bash")}}
