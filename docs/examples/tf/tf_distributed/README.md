# [MNIST with TensorFlow using SlurmClusterResolver](https://github.com/jean-zay-users/jean-zay-doc/tree/master/docs/examples/tf/tf_distributed)

This toy-example shows how to do distributed training using TensorFlow 2 and
`SlurmClusterResolver`. 

# Submit the job

```
cd jean-zay-doc/docs/examples/tf/tf_distributed
sbatch mnist_example_distributed.slurm
```

## Code

The code for the distributed training (`mnist_example.py`):

{{code_from_file("examples/tf/tf_distributed/mnist_example.py", "python")}}

and the script to launch the job:

{{code_from_file("examples/tf/tf_distributed/mnist_example_distributed.slurm", "bash")}}

