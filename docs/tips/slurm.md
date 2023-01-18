# SLURM

## How to launch an interactive job

Your can use `srun` to launch an interactive job.

For example, if you want to use a node with 4 GPUs during 1 hour, you can type:

```bash
srun --ntasks=1 --cpus-per-task=40 --gres=gpu:4 --time=01:00:00 \
     --qos=qos_gpu-dev --pty bash -i
```

Now, you have a brand new shell on a compute node where you can run your scripts interactively
during 1h.

## Overview of cluster usage

```bash
sinfo -p gpu_p1,gpu_p2 -o"%P %.16F"
```

Output is something like this:

```bash
PARTITION   NODES(A/I/O/T)
gpu_p1      258/0/2/260
gpu_p2       15/16/0/31
```

A = allocated, I = idle, O = other, T = total

## How to connect to the node of a launched GPU job

This can be useful to do lightweight monitoring of your job, for example to
look at `nvidia-smi` output while your job is running.

You can directly connect to a node used by one of your jobs with SSH:

```bash
ssh node-name
```
You can get the `node-name` information from the `squeue -u $USER` command. For example, `r7in10`
or `jean-zay-ia816` are valid node names.

If you don't have a job running on the node you will get an error like this:

```
Access denied by pam_slurm_adopt: you have no active jobs on this node
Connection closed by 10.148.8.45 port 22
```

Caveat (September 2020) : if you have multiple jobs running on the same node it
is not possible to specify which job you want to connect to.

Have a look at the [official doc](
http://www.idris.fr/eng/jean-zay/jean-zay-connexion_ssh_noeud_calcul-eng.html)
about this as well.

## Auto Requeue on timeouts

Sometimes you want your script to run longer than the maximum walltime of a
particular Slurm queue, for example if you want to train a model for more than
1 day on the `gpu_p1` queue or more than 5 days on the `gpu_p2` queue.  One
work-around for this use case is to take a snapshot of your model regularly and
automatically relaunch a job (and start from this snapshot) once it reaches the
maximum walltime limit.

It is possible to ask Slurm to send a signal before the job timeouts, handle it
in Python and automatically requeue a similar job.

You need to add the following to your Slurm submission script:

```bash
# asks SLURM to send the USR1 signal 20 seconds before the end of the time limit
#SBATCH --signal=USR1@20
```

And handle the signal in Python:

```python
import os
import socket
import signal
import sys
import logging

from pathlib import Path

logger = logging.getLogger(__name__)

def sig_handler(signum, frame):
    logger.warning("Signal handler called with signal " + str(signum))
    prod_id = int(os.environ['SLURM_PROCID'])
    logger.warning("Host: %s - Global rank: %i" % (socket.gethostname(), prod_id))
    if prod_id == 0:
        logger.warning("Requeuing job " + os.environ['SLURM_JOB_ID'])
        os.system('scontrol requeue ' + os.environ['SLURM_JOB_ID'])
    else:
        logger.warning("Not the master process, no need to requeue.")
    sys.exit(-1)


def init_signal_handler():
    """
    Handle signals sent by SLURM for time limit.
    """
    signal.signal(signal.SIGUSR1, sig_handler)
    logger.warning("Signal handler installed.")

...
# In main

# Makes sure that we start from where we ended in the previous job
checkpoint = Path("my_job.pt")
if checkpoint.exists():
    load(checkpoint)

init_signal_handler()

for _ in range(epochs):
    ...
    save(checkpoint)

```

!!! warning
    Remember to also add a serialization logic to your objects to make sure
    your new job start from where your previous job ended. In the above case,
    we will restart from the previous epoch checkpoint.