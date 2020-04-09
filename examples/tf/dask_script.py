from dask.distributed import Client
from dask_jobqueue import SLURMCluster

from mnist_example import train_dense_model

cluster = SLURMCluster(
    n_workers=1,
    cores=1,
    job_cpu=10,
    memory='10GB',
    job_name='dask_mnist_tf_example',
    walltime='1:00:00',
    interface='ib0',
    job_extra=[
        '--gres=gpu:1',
        '--qos=qos_gpu-dev',
        '--distribution=block:block',
        '--hint=nomultithread',
        '--output=%x_%j.out',
    ],
    env_extra=[
        'module purge',
        'module load tensorflow-gpu/py3/2.1.0',
    ],
    extra=['--resources GPU=1'],
)

print(cluster.job_script())

client = Client(cluster)
save = False
futures = client.submit(
    # function to execute
    train_dense_model,
    # *args
    None, False,
    # this function has potential side effects
    pure=not save,
    resources={'GPU': 1},
)
job_result = client.gather(futures)
if job_result:
    print('Job finished without errors')
else:
    print('Job errored out')
print('Shutting down dask workers')
