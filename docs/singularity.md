# Using a Singularity container on the cluster

You might want to use a container for many reasons: the code you are using a
some super old dependencies (like Caffee) or headless rendering is not
available. Let's see how you can run your code on the cluster using a
container.

The overall steps are the following:

1. Building a container image on your machine (with sudo access)
2. Transferring the container on the JeanZay SINGULARITY_ALLOWED_DIR
3. Running the container

## 1. Building a container image

To build a container image, you want to write first a Singularity description
file, something that looks like a Dockerfile.


### Optional: converting an existing Dockerfile

It is generally easier to start from existing description files. Unfortunately,
the Singularity community is not that large and you might not find a starter
kit fitting your needs.

Good news though, you can start from an existing Dockerfile and convert it to a
Singularity description file:

```bash
# Downloading a random Dockerfile
wget https://github.com/peteanderson80/Matterport3DSimulator/blob/master/Dockerfile
# Converting it to a Singularity description file:
pip install spython
spython recipe Dockerfile > Singularity
```

### Building step

As per the [official Jean-Zay doc](http://www.idris.fr/eng/jean-zay/cpu/jean-zay-utilisation-singularity-eng.html),
you can build a container directly from the cluster but only if the building
operation does not need any sudo rights.

It is generally not the case, so you'll want to build the container on your own
machine:

``` bash
singularity build my_container.sif Singularity 
```

Note that you can also build a Singularity container from a Docker container:

``` bash
# from docker hub
singularity build my_container.sif docker://ubuntu:20.04
# or from a local image:
docker build -t my-awesome-image:latest /path/to/dir/with/Dockerfile
singularity build my_container.sif docker-daemon://my-awesome-image:latest
```

## 2. Transfer

First, we transfer the newly generated container to the cluster:

```bash
scp my_container.sif jeanzay:/my/scratch/folder
```

Then, we register the container:

```bash
idrcontmgr cp my_container.sif 
```

It should appear in `$SINGULARITY_ALLOWED_DIR`. 

In case you have troubles with this environment variable, not being setup, you
can manually fix it:

```bash
export SINGULARITY_ALLOWED_DIR=/gpfsssd/singularity/images/$(whoami)
```

## 3. Running your container

You might want to bind local folders to your container using this script `singularity_start`:

```bash
module load singularity
singularity shell  --nv\
    --bind $WORK:$WORK,$SCRATCH:$SCRATCH,$STORE:$STORE $SINGULARITY_ALLOWED_DIR/$1
```

Remove `--nv` if you don't use a GPU partition.

