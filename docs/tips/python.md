# Python

## Install miniconda (recommended solution if you are already familiar with conda)

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

If you run out of space or inodes on `$WORK` (`idrquota -w` can help you
figuring out whether you are close to the limit) you can send an email to
[assist@idris.fr](mailto:assist@idris.fr) and ask for an increase. Try
something between 5x-10x with some small justification and that should go
through without too much problem (if that's not the case, open an
[issue](https://github.com/jean-zay-users/jean-zay-doc/issues/new) to improve
this doc!).