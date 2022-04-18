import dask
from dask_jobqueue import SLURMCluster 

cluster = SLURMCluster(
    project='your_account', 
    cores=40, 
    processes=40,
    memory='160GB', 
    walltime='20:00:00', 
    interface='ib0', 
    death_timeout=300, 
    job_extra=['--job-name=worker', '--hint=nomultithread'],
    env={'HDF5_USE_FILE_LOCKING':'FALSE'}
)
cluster.scale(jobs=4) # jobs=4 means total 4 nodes, 4*40 = 160 processes

from dask.distributed import Client 
client = Client(cluster) 
dask.config.set({'distributed.comm.timeouts.connect': '60s'})
# print(client) # Will throw warning if all asked jobs are not started e.g., jeanzay

# Other libraries
import xarray as xr
import numpy as np

# Setting seed for reproducibility
np.random.seed(42)

# Helper functions
# numpy ufunc
def calc_ci_lower(x):
    ci = np.quantile(np.sort(np.random.choice(x, size=(len(x), 10000)), axis=0), 0.025, axis=1)
    return(ci)

def calc_ci_lower_array(arr, axis=0):
    ci = np.apply_along_axis(calc_ci_lower, axis, arr)
    return(ci)

# Computation on data
ds = xr.open_dataset(
    'input_data_file.nc', 
    chunks={'nnode':1000}
)

# Now we apply a ufunc
ci = xr.apply_ufunc(
    calc_ci_lower_array, 
    ds['maxelev'], 
    dask='parallelized', 
    output_dtypes=[float]
)

ci.to_netcdf('ci_lower.nc')

client.close()
cluster.close()
