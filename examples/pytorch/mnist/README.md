# Pytorch example script

To run this script you will need to clone the jean-zay repo in your `$WORK`
dir, then:
```
cd $WORK &&\
git clone https://github.com/jean-zay-users/jean-zay-doc.git
```

After that, you can launch the batch job (single GPU version) via:
```
sbatch jean-zay-doc/examples/pytorch/pytorch_example_script.sh
```

Alternatively, a multi GPU version is available. It launches the training with
10 different values for a single parameter. In SLURM language this is called a
*job array*.  
This script implements a kind of parallelism (when data is not shared between
different jobs). It can be useful to optimize the values of the hyperparameters
during the training:
```
sbatch jean-zay-doc/examples/pytorch/pytorch_example_script_multigpu.sh
```

