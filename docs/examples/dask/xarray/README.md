This example shows how to use dask through xarray on Jeanzay. You will need a python environment with xarray installed to get it work. The easiest way to create an environment is to load the anaconda package and create your own environment - 

```
module load anaconda-py3/2021.05
conda create --prefix=./xarray python xarray netCDF4 pandas numpy scipy
```

The above conda command will create a python environment in a directory called `xarray` in the directory where the command is issued. The module `anaconda-py3/2021.05` will be needed during runtime too.

The submission script `example.slurm` is submitted through a **single core** process. That **single core** process then spawn the distributed computing processes. Typically, one can use `prepost` partition if the required time is less than 20 hours. If more, the job may be submitted through a `cpu_p1` node. The actual scaling of cluster is done through the `example.py` script.

The `example.py` file shows an example script for computing confidence interval through bootstrapping over a very large dataset. The definition for a single machine in the cluster is defined in the variable `cluster`. In `example.py`, a single cluster is defined as a 40-core [40-process] node (e.g., no multithreading). The number of node is scalled using `cluster.scale(jobs=4)`, where `jobs=4` means total 4 nodes, i.e., 4*40 = 160 processes. The `dask_jobqueue` will spawn computing nodes one by one based on avaiability by SLURM, and distribute the job. 

Note that, if 4 nodes are demanded, but only one node is allocated by the SLURM, then the job will get started with one node only, and more node will be/or not be added based on their availability while running. This implies that, during busy hours, all required nodes may not be alloted. 

Also note that, the **single core** task does not do anything other than managing the job. During busy hours, it is not unlikely that a compute node is allocated hours after starting of the **single core** job. Hence, it is necessary to keep some provision of extra time for the **single core** job.