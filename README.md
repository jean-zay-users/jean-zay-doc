# Why this doc?

In total the procedure has taken us 3 weeks roughly. The goal of this simple
doc is to make the whole process a bit shorter and smoother for others.

**This is supposed to be a collaborative doc, if you spot errors or things that
could be improved, open a Pull Request (PR)!**

In particular, feel free to share tutorials, tools and scripts to help users
have a more productive use of the cluster, e.g.:

- how to make your code use checkpointing to be able to get long running processing
  despite the 20 hour wall time limit;
- how to make sure your code can leverage the hardware optimally (e.g. with mixed
  precision and tensorcores);
- how to make sure that your processing is not limited by suboptimal data access patterns
  on the disks or inefficient pre-processing on the CPUs;
- how to do efficient hyper-parameter tuning at scale;
- how to synchronize you code between local computer and the cluster.

# Access procedure for Jean Zay

## Overview

- create an EDARI account (simple personal details)
- fill a form about your project ("Déclaration de dossier"). Hardest part is to
  figure out who your "Directeur de la structure de recherche" is and to have
  the form signed by him/her. You also need to write a few lines about your
  project.
- fill a form about to get a computing account ("Déclaration de compte
  calcul"). Hardest part is to figure out who your "Responsable Sécurité
  informatique" is and have the form signed by him/her as well as the
  "Directeur de la structure de recherche". You also need to declare one (or
  more) IP address(es) that will be able to use to connect to Jean Zay.
- After roughly a week, you'll get an email from IDRIS giving you your login,
  password and instructions to connect to Jean Zay.
- After roughly 2 days, you should be able to connect to Jean Zay.


## EDARI account (administrative account)

Estimate of the time needed: 5 minutes

To create an EDARI account: https://www.edari.fr/user/register

In case something goes wrong:
- contact for EDARI account: https://www.edari.fr/contact
- EDARI FAQ: https://www.edari.fr/faq

Important details:
- when filling your phone number, use a real one. Yes, you may get a call to
  have a better idea what you want to do ...

## "Déclaration de dossier" (project description)

Estimate of the time needed: 15 minutes (fill the form) + 1-2 days (figure out
the right person to sign the form and get him/her to sign it)

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

Estimate of the time needed: 15 minutes (fill the form) + 1-2 days (figure out
the right person to sign the form and get him/her to sign it).

Important details:
- "Responsable sécurité informatique", this is someone that should be able to
  turn deny you acess to Jean Zay, in case there is any issue with your account
  activity. more details
- IP addresses to connect to Jean Zay. Make sure they are static IP addresses
  (e.g. not your IP address from you home). In most cases: your desktop in your
  lab will have a static IP address, but best confirm with your local IT
  people. Note that the form is helping you with some suggestion which were
  correct when filling it from a fixed desktop in our institute.

## IDRIS email with login and password

In principle, you should receive a "Ouverture de votre compte" email from IDRIS
roughly one week after having completed the previous step. Contact:
assist@idris.fr if you have not received email within a week.

- quite a long email with detailed instructions. One the first connection your
  password is the concatenation of the first password in "Déclaration de compte
  calcul" and the password in the email. You are then asked to chose a new
  password.
- Count 2-3 days after the email to actually be able to access Jean Zay. Some
  time is needed for the IP address to be added to Jean Zay.

# Tips and Tricks

## Useful links

Hardware: http://www.idris.fr/eng/jean-zay/cpu/jean-zay-cpu-hw-eng.html

Doc: http://www.idris.fr/eng/jean-zay/

## Generic advice

- find people that have accessed IDRIS clusters around you. If you have no idea
  who they may be, IT may know, ask them. They may save you a lot of time, for
  example they very likely know who the "Directeur de la structure de
  recherche" and "Responsable Sécurité informatique" are.
- there is a big cultural gap between HPC sys-admins and IA users. For example,
  most traditional "serious" HPC clusters do not have access to the internet,
  yes you have read this correctly, people in traditional HPC do not need
  internet access to work on their problems.
- So far every interaction we have had with Jean Zay sys-admins has been very
  positive. Even if there may be some frustration (on both sides), remember to
  keep your comments constructive.
