# Shell configuration

## Bash config

The `.bashrc` file is only executed when opening interactive shells on the cluster, while the `.bash_profile` file is only executed when logging in.
To make sure the `.bashrc` is run when logging in, modify your `~/.bash_profile` so that it contains the following lines:

```bash
#
# Source ~/.bashrc from ~/.bash_profile
#
[[ -f ~/.bashrc ]] && . ~/.bashrc
```

## Other shells (csh, zsh, tcsh, fish, etc)

Other shells different of Bourne Again Shell (bash) are [not officially supported in Jean Zay](http://www.idris.fr/jean-zay/cpu/jean-zay-cpu-connexion-et-shells.html). 
However, [people discuss frequently how to short-cut this constraint](https://github.com/jean-zay-users/jean-zay-doc/issues/18).