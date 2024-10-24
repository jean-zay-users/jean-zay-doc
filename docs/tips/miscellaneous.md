# Miscellaneous

## Managing your data and the storage spaces

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

## Requesting extra inodes or extra storage space

1. Create a password for the extranet from the command line program `passextranet`.
2. Connect to the extranet (`https://extranet.idris.fr`) from an approved machine with your Jean-Zay username and this above password.
3. Grant your request.

!!! warning
    The number of inodes seem to be a bottleneck for Jean-Zay platform. Do not expect a too high number of obtained requests.

## Changing the default file permission sets to make collaboration easier

By default, users have a umask value (i.e. the default file permission set for newly created files and folders) of 0027, which in symbolic notation translates to `u=rwx,g=rx,o=`. That means if you have colleagues assigned to the same project/group, they won't have write permissions on the files and directories you create, which can be annoying if you want to collaborate in a common disk space such as `$ALL_CCFRWORK`. To add group-write permissions by default, you can execute `umask 007` which will change the umask value for the current shell session; or to make it permanent, add the line `umask 007` at the beginning of your `~/.bash_profile`.

## Using available datasets

Common datatsets are available on `$DSDIR`. When a dataset is zipped, like COCO,
you can unzip it in `$SCRATCH` with `unzip -DD` or `tar -m` to use the dates from archive
extraction time rather than (the default) to use the dates of the original files when the archive was created.
This will prevent the wipe of your freshly unzipped dataset.
If raw data is directly available such as for the ImageNet dataset, you can read datasets from `$DSDIR` directly without the need to copy the dataset to `$SCRATCH`.

## Connect seamlessly from your local machine

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

## Automatic synchronization with your local machine

The following script allows you to automatically synchronize a local directory and have an exact copy of it on jean-zay.
For the script to run smoothly, make sure the directory is lightweight, e.g. a directory containing code. On your local machine, create a file `sync_jz.sh` with

```bash
#!/bin/bash

source_path="/your/local/directory"
target_path="jz-username@jean-zay.idris.fr:/your/jean-zay/directory"

while inotifywait -r -e modify,create,delete $source_path
do
    rsync -azh $source_path $target_path \
          --progress \
          --delete --force \
          --exclude=".git"
done
```

Execute the following commands locally to install inotify, make the script executable and run the script.
```
sudo apt install inotify-tools
chmod +x sync_jz.sh
./sync_jz.sh
```
The script has to be run in a terminal session on your local machine, you can put it in a `tmux` or `screen` terminal. To stop the sync, just stop the process. The sync will terminate with the terminal session and needs to be launched after restarting your local machine.

The synchronization is unidirectional, which means that all of the edits should be made on the local directory. Each time `inotify` detects an edit, `rsync` runs to update the remote directory.
Any manual change of the remote directory will be overwritten so that the remote directory matches the local one.
`.git` is excluded from synchronization as git history directories can be heavy and are usually not necessary to run code on the cluster.

## Clone git repo

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


## Tensorboard

Tensorboard is a nice tool to monitor the progress of your trainings.
Currently there are 3 (known) ways to use it in Jean Zay:

### Run sshfs + Tensorboard locally

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
tensorboard --logdir=/your/local/tensorboard/log/folder
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

### Use Tensorboard dev

!!! warning "Disclaimer"
    TensorBoard.dev has been shut down as of January 1, 2024

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

### Use `idrjup` command (Legacy)

The way recommended by the official doc but probably the least convenient is to:

- launch a Jupyter notebook server with `idrjup` on Jean-Zay
- use the Tensorboard Jupyter extension inside the Jupyter notebook

This is described in full details in the [official
docs](http://www.idris.fr/jean-zay/pre-post/jean-zay-jupyter-notebook.html).


## gitlab-runner

CI's workflows are not currently supported on Jean Zay (soon?).

!!! warning "Disclaimer"
    Setting a runner on Jean Zay for your gitlab project could deduct some
    calculation time on your hours account, depending on the job it executes.
    Please be aware that anyone pushing on your repo may trigger a
    time-consuming job on Jean Zay.  For more information, please visit [gitlab
    branch
    protection](https://docs.gitlab.com/ee/user/project/protected_branches.html).

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

!!! note
    * You may use the registration token provided in Settings->CI/CD->runners
      of your gitlab project in the .toml config file.
    * `$WORK` directory will be used to store CI builds, reports and outputs.
    * Check periodically your that your tmux session is still alive (usually killed on
      tuesdays).

### config.toml example
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
