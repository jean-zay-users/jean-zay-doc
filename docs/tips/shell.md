# Shell configuration

## Bash config

The `.bashrc` file is only executed when opening interactive shells on the cluster, while the `.bash_profile` file is only executed when logging in.
To make sure the `.bashrc` is run when logging in, modify your `~/.bash_profile` so that it contains the following lines:

```bash
#
# Source ~/.bashrc from ~/.bash_profile
#
[[ -f ~/.bashrc ]] && . ~/.bashrc