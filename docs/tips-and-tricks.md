# Tips and Tricks

## Bash config

By default, the `.bashrc` is not executed when connecting on the cluster.
To make sure it is run, add a file `~/.bash_profile` with

```bash
#
# ~/.bash_profile
#

[[ -f ~/.bashrc ]] && . ~/.bashrc
```

## Python

### Install miniconda (recommended solution if you are already familiar with conda)

Install `miniconda` in `$WORK/miniconda3`:

```bash
# download Miniconda installer
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    -O miniconda.sh
# install Miniconda
MINICONDA_PATH=$WORK/miniconda3
chmod +x miniconda.sh && ./miniconda.sh -b -p $MINICONDA_PATH
# make sure conda is up-to-date
source $MINICONDA_PATH/etc/profile.d/conda.sh
conda update --yes conda
# Update your .bashrc to initialise your conda base environment on each login
conda init
```

If you run out of space or inodes on `$WORK` (`irdquota -w` can help you
figuring out whether you are close to the limit) you can send an email to
[assist@idris.fr](mailto:assist@idris.fr) and ask for an increase. Try
something between 5x-10x with some small justification and that should go
through without too much problem (if that's not the case, open an
[issue](https://github.com/jean-zay-users/jean-zay-doc/issues/new) to improve
this doc!).

## SLURM

### How to launch an interactive job

Your can use `srun` to launch an interactive job.

For example, if you want to use a node with 4 GPUs during 1 hour, you can type:

```bash
srun --ntasks=1 --cpus-per-task=40 --gres=gpu:4 --time=01:00:00 \
     --qos=qos_gpu-dev --pty bash -i
```

Now, you have a brand new shell on a compute node where you can run your scripts interactively
during 1h.

### Overview of cluster usage

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

### How to connect to the node of a launched GPU job

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

### Auto Requeue on timeouts

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

## Miscellaneous

### Managing your data and the storage spaces

Be careful about the place where you put your data on the JZ super-computer,
since there are quotas for each project, depending on the storage space and the
number of files (inodes) that you use. Additionally, some spaces are temporary.

There is a detailed description of the storage spaces [here](http://www.idris.fr/jean-zay/cpu/jean-zay-cpu-calculateurs-disques.html).

Briefly:

- `$HOME` (3Gb) -> for config files.
- `$WORK` (limited on inodes) -> for code, (small) databases.
- `$SCRATCH` (very large limits, temporary) -> output data, large databases
- `$STORE` (large space, occasional consultation)  -> permanent large databases.
- `$DSDIR` (popular databases on demand).

It is worth noting that `$SCRATCH` consists of a farm of SSD storage
devices and it provides the best performance in reading/writing operations.
You must also be aware that `$SCRATCH` is regularly "cleaned": files that
have not been accessed (i.e. at least read) for 30 days are definitely
removed. So you **risk to lose your data** if your keep it there without using it.

You can consult your disk quota anytime with the command `idrquota` (see
`idrquota -h`). If you need more space or inodes on your personal spaces
(`$WORK` or `$STORE`), just ask the support team at
[assist@idris.fr](mailto:assist@idris.fr).

If you need to send data to Jean-Zay a good idea is to use `rsync`. E.g.:

```bash
rsync -avz /your/local/database/ \
    your-jean-zay-login@jean-zay:/gpfsscratch/your/remote/dir/
```

### Using available datasets

Common datatsets are available on `$DSDIR`. When a dataset is zipped, like COCO,
you can unzip it in `$SCRATCH` with `unzip -DD` or `tar -m` to use the dates from archive
extraction time rather than (the default) to use the dates of the original files when the archive was created.
This will prevent the wipe of your freshly unzipped dataset.
If raw data is directly available such as for the ImageNet dataset, you can read datasets from `$DSDIR` directly without the need to copy the dataset to `$SCRATCH`.

### Connect seamlessly from your local machine

Add local your public ssh key to the `~/.ssh/authorized_keys` of your account on the jean-zay cluster.
Your local public ssh key can be found in `~/.ssh/id_rsa.pub`.

In your local ssh configuration, found in `~/.ssh/config`, you can also add the following:

```bash
Host jz
hostname jean-zay.idris.fr
user <user-name>
```

To connect to the jean-zay cluster you will then just need to do `ssh jz`.

For good practices about SSH keys you can have a look at:
http://www.idris.fr/faqs/ssh_keys.html

### Clone git repo

SSH from Jean Zay going to the outside is very restricted. That means that if
you are used to do

```bash
git clone git@my-institute-gitlab.fr:/my-organisation/my-repo.git
```
it will not work on Jean Zay (very likely it will time out after some time).

Instead you should use HTTPS instead i.e. something like:

```bash
git clone https://my-institute-gitlab.fr:/my-organisation/my-repo.git
```

In order to avoid having to type your password too often (on each `git push`)
you can set up password caching like this:

```bash
git config --global credential.helper cache
# by default password is cached for 15 minutes
# the next line increases it to 1 hour
git config --global credential.helper "cache --timeout=3600"
```

If for some reason, you do absolutely need SSH access from Jean Zay to an
outside server, you need to fill out this form:
http://www.idris.fr/media/data/formulaires/fgc.pdf, mostly the section "Ajout,
modification ou suppression de machines".


### Tensorboard

Tensorboard is a nice tool to monitor the progress of your trainings.
Currently there are 3 (known) ways to use it in Jean Zay:

#### Run sshfs + Tensorboard locally

The idea is to:

- use your local machine (i.e. the machine you are typing on) which is outside
  of Jean-Zay
- use `sshfs` so that your Tensorboard logs (that are on Jean-Zay) are visible
  on your local machine
- run Tensorboard locally on your logs mounted with `sshfs`

For example if your Tensorboard logs are in `/your/jean-zay/tensorboard/log/folder/`

1. Mount the folder locally:
```
sshfs \
  -o reconnect,ServerAliveInterval=15,ServerAliveCountMax=3,follow_symlinks \
  jean-zay:/your/jean-zay/tensorboard/log/folder \
  /your/local/tensorboard/log/folder
```

2. Install Tensorboard on your local machine for example with pip:
```
pip install tensorboard
```

3. Launch Tensorboard on your local machine
```
tensorboard --logdir=$HOME/jeanzay/logs
```

This will open a new tab in your local browser and show the progress of your training.

!!! note
    the `sshfs` command, in particular the `jean-zay:/your/jean-zay/...` may
    need to be adapted depending on configuration details in your
    `~/.ssh/config`

!!! tip
    The obscure parameters in the `sshfs` command i.e.
    `reconnect,ServerAliveInterval=15,ServerAliveCountMax=3` are here to
    prevent being automatically disconnected.

    It can probably still happen that you get disconnected e.g. because of
    CPU time limit on the login nodes or maintenances. In general, this can be
    resolved by unmounting your local log folder with:
    ```
    fusermount -u /your/local/tensorboard/log/folder`
    ```

    and mounting your folder again with the `sshfs` command given above.

    If you have better advice to prevent or recover from disconnections, please
    improve this doc!

#### Use Tensorboard dev

[Tensorboard dev](https://tensorboard.dev/) is a tool allowing you to upload your
Tensorboard events on the cloud and read them online using Google OAuth.
You will find the main Tensorboard tabs, and many others are in development.

Practically on Jean Zay, you will need to:
1. install Tensorboard: `pip install tensorboard`
2. create a screen: `screen -S tensorboard-dev` (or a tmux if you prefer)
3. launch Tensorboard dev: `tensorboard dev upload --logdir /path/to/logs`
4. copy the url (for example https://tensorboard.dev/experiment/EDZb7XgKSBKo6Gznh3i8hg/#scalars) and detach from the screen session

Afterwards, you can keep monitoring your training with the same address, as the
events will be uploaded on-the-fly.

!!! warning
    since your process is running on a login node, it will be killed after 30
    minutes of CPU time, which roughly translates to 11 hours for Tensorboard
    dev in our experience.

#### Use `idrjup` command

The way recommended by the official doc but probably the least convenient is to:

- launch a Jupyter notebook server with `idrjup` on Jean-Zay
- use the Tensorboard Jupyter extension inside the Jupyter notebook

This is described in full details in the [official
docs](http://www.idris.fr/jean-zay/pre-post/jean-zay-jupyter-notebook.html).


### gitlab-runner

CI's workflows are not currently supported on Jean Zay (soon?).

* Disclaimer : Setting a runner on Jean Zay for your gitlab project could
deduct some calculation time on your hours account, depending on the job it executes.
Please be aware that anyone pushing on your repo may trigger a time-consuming job on Jean Zay.
For more information, please visit [gitlab branch protection](https://docs.gitlab.com/ee/user/project/protected_branches.html).

Here is a procedure to run a gitlab-runner in user mode on your account:
1. launch a conda env
2. get gitlab-runner from anaconda repo : `conda install -c conda-forge gitlab-runner`
3. open a tmux session : `tmux`
4. register a new runner : `gitlab-runner register` as described [here](https://docs.gitlab.com/runner/register/#linux)
5. launch user-mode gitlab-runner :
   `gitlab-runner run --working-directory <path to >/CI-Outputs --config <path to>/.gitlab-runner/config.toml --service gitlab-runner &`

6. detach from tmux session : Ctrl + B and D
7. check your runner status in the Settings->CI/CD->runners tab of your gitlab repo.
8. create your .gitlab-ci.yml file as described [here](https://docs.gitlab.com/ee/ci/yaml/gitlab_ci_yaml.html)

* You may use the registration token provided in Settings->CI/CD->runners of your gitlab project in the .toml config file.
* working directory will be used to store CI builds, reports and outputs.
* often check your that your tmux session is still alive (usually killed on tuesdays)

#### config.toml example
```
concurrent = 1
check_interval = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "Jean-Zay_runner"
  url = "https://gitlab.inria.fr/"
  token = "<Gitlab project registration Token>"
  executor = "shell"
  [runners.custom_build_dir]
  [runners.cache]
    [runners.cache.s3]
    [runners.cache.gcs]
  [runners.custom]
    run_exec = ""

```
