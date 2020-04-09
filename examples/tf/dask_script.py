from dask.distributed import Client
from dask_jobqueue import SLURMCluster

from mnist_example import train_dense_model

cluster = SLURMCluster(
    n_workers=1,
    cores=1,
    job_cpu=10,
    memory='10GB',
    job_name='dask_mnist_tf_multi_gpu_example',
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
    ]
)

print(cluster.job_script())

client = Client(cluster)
futures = [client.submit(train_dense_model, (None, False) ]
_ = client.gather(futures)

print('Shutting down dask workers')
