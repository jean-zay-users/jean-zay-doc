# Tips and Tricks

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

```
rsync -avz /your/local/database/ your-jean-zay-login@jean-zay:/gpfsscratch/your/remote/dir/ 
```

## How to use interactive mode

Interactive mode using SLURM can be done by using the command
`srun`.

For example, if you want to use a node with 4 GPUs during 1
hour, you can type:
``` 
srun --ntasks=1 --gres=gpu:4 --time=01:00:00 --pty bash -i 
```

Now, you have a brand new shell on a compute node where you can run your scripts interactively
during 1h. 
