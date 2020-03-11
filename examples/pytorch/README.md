# Pytorch example script

To run this script you will need to clone the jean-zay repo in your `$WORK`
dir, then:
```
cd $WORK &&\
git clone https://github.com/jean-zay-users/jean-zay-doc.git
```

After that, you can just launch the batch job (single GPU) via:
```
sbatch jean-zay-doc/examples/pytorch/pytorch_example_script.sh
```

A multi GPU version is also available, it launches the same training with
several values for a single parameter in multiples GPU (parallelism without sharing
data). Classical case for simple hyperparameters search:
```
sbatch jean-zay-doc/examples/pytorch/pytorch_example_script_multigpu.sh
```

