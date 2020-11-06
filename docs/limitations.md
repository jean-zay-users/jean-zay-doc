If you have some additional info or a work-around about any of the limitations,
please open an [issue](https://github.com/jean-zay-users/jean-zay-doc/issues/new) or even better
a [Pull Request](https://github.com/jean-zay-users/jean-zay-doc/compare)!

# Limitations

## docker image usage

There is currently no way of using a docker image on Jean Zay. They are working
on it but at the time of writing (end January 2020) it is likely to take
between 3 and 6 months so be ready for some time between May and August 2020.

Last time we heard (February 2020) from this effort, `singularity` would be the
tool available on Jean Zay to run docker images.

## SSH port forwarding disabled

SSH port forwarding is disabled by Jean Zay sys-admin for security reasons. I
([Loïc](https://github.com/lesteve)) have a work-around, if you are interested
contact me!

<img src="../img/ssh-port-forwarding-info.jpg"/>

SSH port forwarding is also called SSH tunneling sometimes (maybe a less accurate term). This
the kind of command you run when you are using SSH port forwarding:
```
base ❯ ssh -N your-jean-zay-login@jean-zay3.idris.fr -L 12345:jean-zay3.idris.fr:12345  # jean-zay
```

If you are trying to use it on Jean Zay you will get this kind of errors (in
the console you run the `ssh -L` command when you try to access the local port):
```
channel 2: open failed: administratively prohibited: open failed
```

One use case for SSH port-forwarding is to start a Jupyter notebook server on a
remote machine and open it locally in your web browser using a URL like this:
`http://localhost:8888`. For this Jupyter notebook use case, Jean Zay provides
their own solution, see
[this](http://www.idris.fr/eng/jean-zay/pre-post/jean-zay-jupyter-notebook-eng.html)
for more details.
