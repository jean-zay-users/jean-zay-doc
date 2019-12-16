# Why this doc?

In total the procedure to access Jean Zay could be up to 3 weeks roughly. The
goal of this simple doc is to make the whole access process a bit shorter and
smoother for others.

**This is supposed to be a collaborative doc, if you spot errors or things that
could be improved, open a Pull Request (PR)!**

In the medium term, more material could be added to discuss tips and tricks,
limitations, work-arounds, etc ... on Jean Zay. In particular, feel free to
share tutorials, tools and scripts to help users have a more productive use of
the cluster, e.g.:

- how to make your code use checkpointing to be able to get long running
  processing despite the 20 hour wall time limit;
- how to make sure your code can leverage the hardware optimally (e.g. with
  mixed precision and tensorcores);
- how to make sure that your processing is not limited by suboptimal data
  access patterns on the disks or inefficient pre-processing on the CPUs;
- how to do efficient hyper-parameter tuning at scale;
- how to synchronize you code between local computer and the cluster.

# Access procedure for Jean Zay

## Overview

There are two different types of procedure if you want to access JZ
super-computer, depending on the usage that you are planning to do. The
first one is intended to users developing AI algorithms (mostly GPU
partition). The second one to people performing high performance computing 
(typically a mixed usage of CPUs and GPUs). These guidelines are focused on the
first case (developing AI algorithms).

- Create an [EDARI account](https://www.edari.fr/user/register) (simple
  personal details).
- Once on your new user space, go to the "Intelligence Artificielle" section
  and fill a form about your project ("Déclaration de dossier"). Hardest part
  is to figure out who your "Directeur de la structure de recherche" is and to
  have the form signed by him/her. You also need to write a few lines about
  your project.
- Fill a form about to get a computing account ("Déclaration de compte
  calcul"). Hardest part is to figure out who your "Responsable Sécurité
  informatique" is and have the form signed by him/her as well as the
  "Directeur de la structure de recherche". You also need to declare one (or
  more) IP address(es) that will be able to use to connect to Jean Zay.
- After roughly a week, you'll get an email from IDRIS giving you your login,
  password and instructions to connect to Jean Zay.
- After roughly 2 days, you should be able to connect to Jean Zay.


## EDARI account (administrative account)

*Estimate of the time needed: 5 minutes*

To create an EDARI account: https://www.edari.fr/user/register

In case something goes wrong:
- Contact for EDARI account: https://www.edari.fr/contact
- EDARI FAQ: https://www.edari.fr/faq

Important details:
- When filling your phone number, use a real one. Yes, you may get a call to
  have a better idea what you want to do ...

## "Déclaration de dossier" (project description)

*Estimate of the time needed: 15 minutes (fill the form) + 1-2 days (figure out
the right person to sign the form and get him/her to sign it)*

Important details:
- "Directeur de la structure de recherche" : Head of the lab, head of the
  department, head of the institute, do what is easier for you. 
- Project description : no need to spend too much time on this, 5 lines should
  be plenty enough. Some people decided to write a more serious proposal,
  thinking that it would be easier to ask for a renewal, do what makes more
  sense to you.
- As long as you ask for <= 10000 GPU hours (~400 days on a single GPU) and
  less than 48 GPUs simultaneously (4 GPUs on 12 nodes) it should go through
  easily (see https://www.edari.fr/voirlappel56).
- Note that in principle once your 10000 GPU hours are exhausted you can ask for
  a renewal through a similar "lightweight" procedure.

TODO: there is something where you need to make sure that you have selected the
right category (develop algorithms for AI). Otherwise, you'll end up in the
traditional HPC process and it may be a lot harder (think months) to get an
account validated.

## "Déclaration de compte calcul" (computing account creation for Jean Zay)

*Estimate of the time needed: 15 minutes (fill the form) + 1-2 days (figure out
the right person to sign the form and get him/her to sign it).*

Important details:
- "Responsable sécurité informatique", this is someone that should be able to
  turn deny you access to Jean Zay, in case there is any issue with your
  account activity. He/She must be able to certify that you respect the IT
  charter in your host lab/institution. 
- IP addresses to connect to Jean Zay. Make sure they are static IP addresses
  (e.g. not your IP address from you home). In most cases: your desktop in your
  lab will have a static IP address, but best confirm with your local IT
  people. Note that the form is helping you with some suggestion which were
  correct when filling it from a fixed desktop in our institute.

## IDRIS email with login and password

In principle, you should receive a "Ouverture de votre compte" email from IDRIS
roughly one week after having completed the previous step. Contact:
assist@idris.fr if you have not received email within a week.

- Quite a long email with detailed instructions. One the first connection your
  password is the concatenation of the first password in "Déclaration de compte
  calcul" and the password in the email. You are then asked to chose a new
  password.
- Count 2-3 days after the email to actually be able to access Jean Zay. Some
  time is needed for the IP address to be added to Jean Zay.

## How to write a project proposal (request a lot of computing time)

*Estimate of the time needed: 1h (write a project) + a few days/weeks
for approval (depending on the request).* 

Useful when you have used most of your
computing time and want to fill a "Demande de ressources au fil de l'eau"
(request more hours on the fly), and you would like to ask for more than 10k
hours.

- Describe the scientific project for which you need to perform experiments. Be
  specific about the team you work in, why do you need such computing
  ressources
- Estimate the number of hours you will need. To provide an estimate you can
  estimate your daily/weekly computing time `C` you need and multiply by the
  number of months `M` you want to work on Jean-Zay for this project to get
  `T = C * M`.
- Describe a typical experiment. How much computing ressources do you need: do
  you use 1 GPU per experiment or 10 GPUs, if 10 why, can be useful to justify
  your daily need of computation `C`. Be specific about the algorithms you are
  using, the data type (image, text, audio, video ...), the model you use (cnn,
  lstm, kernels, ...) and what your model is used for (predicting image labels,
  pose estimation, robot movements, ...)
- Include references to back up your project. If you already have published, it
  is definitely a plus.

Depending on your request, this proposal can be reviewed by 1 to 10 people.

# Tips and Tricks

## Useful links

Hardware: http://www.idris.fr/eng/jean-zay/cpu/jean-zay-cpu-hw-eng.html

Doc: http://www.idris.fr/eng/jean-zay/

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

It is worth noting that `$WORK` and `$SCRATCH` consist of a farm of SSD storage
devices and they provide the best performance in reading/writing operations.
`$SCRATCH` is "cleaned" every 30 days, so you **risk to lose your data if your
keep it there**. Privilege the use of `$WORK` to avoid this problem.

If you need to send data to Jean-Zay a good idea is to use `rsync`. E.g.:

```
rsync -avz -e ssh --progress  user@jeanzay:/gpfsscratch/your/remote/dir/ /your/local/database/
```

## How to use interactive mode

Interactive mode using SLURM  can be done by using two commands:
`salloc` and `srun`.  First, you need to reserve the  
ressources you want ot use. For example, if you need a node with 4 GPUs during 1
hour, you can type:

``` 
salloc --ntasks=1 --cpus-per-task=40 --gres=gpu:4 --hint=nomultithread --time=01:00:00
```

Then, you can launch an interactive shell using the allocated ressources:

``` 
srun --pty bash -i 
```

Now, you have a fresh new shell where you can try your scripts interactivly for
1h. 


## Generic advice

- Find people that have accessed IDRIS clusters around you. If you have no idea
  who they may be, IT may know, ask them. They may save you a lot of time, for
  example they very likely know who the "Directeur de la structure de
  recherche" and "Responsable Sécurité informatique" are.
- There is a big cultural gap between HPC sys-admins and IA users. For example,
  most traditional "serious" HPC clusters do not have access to the internet,
  yes you have read this correctly, people in traditional HPC do not need
  internet access to work on their problems.
- So far every interaction we have had with Jean Zay sys-admins has been very
  positive. Even if there may be some frustration (on both sides), remember to
  keep your comments constructive.
