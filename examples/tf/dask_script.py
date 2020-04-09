import click
from dask.distributed import Client
from dask_jobqueue import SLURMCluster

from mnist_example import train_dense_model


@click.command()
@click.option(
    'n_gpus',
    '-n',
    default=1,
    help='The number of GPUs on which to run the mnist examples in parallel. Defaults to 1.',
    type=int,
)
@click.option(
    'save',
    '-s',
    '--save',
    is_flag=True,
    help='Whether you want to save the models or not',
)
def launch_dask_tasks(n_gpus, save):
    assert 0 < n_gpus < 5, 'You need to request between 1 and 4 GPUs.'

    cluster = SLURMCluster(
        n_workers=4,
        cores=4,
        job_cpu=10,
        memory='10GB',
        job_name='dask_mnist_tf_example',
        walltime='1:00:00',
        interface='ib0',
        job_extra=[
            '--gres=gpu:{n_gpus}',
            '--qos=qos_gpu-dev',
            '--distribution=block:block',
            '--hint=nomultithread',
            '--output=%x_%j.out',
        ],
        env_extra=[
            'module purge',
            'module load tensorflow-gpu/py3/2.1.0',
        ],
        extra=['--resources GPU=4'],
    )

    print(cluster.job_script())

    client = Client(cluster)
    futures = [client.submit(
        # function to execute
        train_dense_model,
        # *args
        None, save,
        # this function has potential side effects
        pure=not save,
        resources={'GPU': 1},
    ) for _ in range(n_gpus)]
    job_result = client.gather(futures)
    if all(job_result):
        print('All jobs finished without errors')
    else:
        print('One job errored out')
    print('Shutting down dask workers')


if __name__ == '__main__':
    launch_dask_tasks()
