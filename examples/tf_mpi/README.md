# MNIST with TensorFlow using MPI through Horovod

This little example show you how to do some distributed training using TensorFlow and Horovod.
Since Jean-Zay nodes are connected using MPI and with NCCL, synchronous training is theoretically well scalable.

# Step 1: Download the MNIST dataset

Jean-Zay nodes are not connected to the web for security reasons.
Unfortunately, classic MNIST examples relies on the `keras.datasets.mnist.load_data` that wants to download the dataset.
Here we have first to download the MNIST dataset from the Jean-Zay frontal node.

`wget https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz`

The dataset should have been downloaded as `mnist.npz`.

# Step 2: Submit the job

## Just a few things

Before submitting things, here are a few details.
If you take a look in `tf_mpi_mnist.py`, you can see that our modified version of the MNIST example needs explicitely the absolute path of the `mnist.npz` file (using the `--mnist` argument).
Now look at the slurm script, `tf_mpi_mnist.job`. 
There is a few important things:
 - `#SBATCH --partition=gpu_p1`: We use the `gpu_p1` partition, which has nodes with 4 GPUs each,
 - `#SBATCH --ntasks-per-node=4`: We set 4 MPI tasks per node: one task per GPU,
 - `#SBATCH --cpus-per-task=10`: Since nodes have 40 CPUs each, we have to ask slurm to allocate 1/4 of the node resources (i.e. 10)
 - `#SBATCH --ntasks=32`: We ask for a total of 32 MPI tasks. Since we have 4 tasks per node, this means that we will use 8 nodes.

## Now enjoy

```
sbatch tf_mpi_mnist.job
```
