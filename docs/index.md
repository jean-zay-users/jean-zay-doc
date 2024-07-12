# Jean Zay users
## Collaborative documentation
---
[![Gitter](https://img.shields.io/gitter/room/jean-zay-users/jean-zay-doc.svg)](https://gitter.im/jean-zay-users/jean-zay-doc)
[![Docs](https://readthedocs.org/projects/jean-zay-doc/badge/?version=latest)](https://jean-zay-doc.readthedocs.io/en/latest/?badge=latest)


## Why this doc?

We are researchers and engineers in AI (very vague term but oh well ...) who
have managed to get access to Jean Zay and think this can be a very useful
cluster for your AI research.

At the time of writing (November 2020), the GPU part of Jean Zay is very much
underused and we think a user-contributed documentation could help people
navigating the access procedure and knowing a few necessary tips and tricks to
be productive on such a cluster.

**This is supposed to be a collaborative doc, if you spot errors or things that
could be improved, open an
[issue](https://github.com/jean-zay-users/jean-zay-doc/issues/new) or even
better a [Pull Request (PR)](https://github.com/jean-zay-users/jean-zay-doc/compare)!**

We use gitter for chat, don't hesitate to get involved
[there](https://gitter.im/jean-zay-users/jean-zay-doc) and ask questions!


## Content

- [Jean-Zay administrative procedures](./access-procedure.md). The most
  important one is the access procedure. It will take roughly 3 weeks (add 1-2
  months on top of that if you have to go through additional security
  background checks). It does seem long but it is definitely worth it.
- [Tips and tricks](./tips-and-tricks.md)
- [Limitations](./limitations.md)
- Example scripts: [PyTorch examples](./examples/pytorch), [Tensorflow
  examples](./examples/tf), [Tensorflow MPI distributed examples](.examples/tf_mpi/).
- Example scripts for [pretraining/finetuning/inference of LLMs](https://gitlab.inria.fr/synalp/plm4all) on Jean Zay

In the medium term, more material could be added to discuss tips and tricks,
limitations, work-arounds, etc ... on Jean Zay. In particular, feel free to
share tutorials, tools and scripts to help users have a more productive use of
the Jean Zay cluster, e.g.:

- how to make your code use checkpointing to be able to get long running
  processing despite the 20 hour wall time limit;
- how to make sure your code can leverage the hardware optimally (e.g. with
  mixed precision and tensorcores);
- how to make sure that your processing is not limited by suboptimal data
  access patterns on the disks or inefficient pre-processing on the CPUs;
- how to do efficient hyper-parameter tuning at scale;
- how to synchronize you code between local computer and the cluster.

## Useful links

- [Jean Zay doc targeted towards AI users](http://www.idris.fr/eng/ia/index.htm)

- [Hardware](http://www.idris.fr/eng/jean-zay/cpu/jean-zay-cpu-hw-eng.html)

- [Official Doc](http://www.idris.fr/eng/jean-zay/)

- [Official Doc in French (more accurate sometimes)](http://www.idris.fr/eng/jean-zay/)

- [Cheatsheet Idris](http://www.idris.fr/media/su/idrismemento1.pdf)

- [Gitter chat](https://gitter.im/jean-zay-users/jean-zay-doc)

## Generic advice

- There are big differences in the way of working between traditional HPC (High
  Performance Computing) users and AI users. For example, most traditional
  "serious" HPC clusters do not have access to the internet, yes you have read
  this correctly, people in traditional HPC do not need internet access to work
  on their problems.
- So far every interaction we have had with Jean Zay user support has been very
  positive. Even if there may be some frustration (on both sides), try to be
  both pedagogical and constructive when you send an email to
  [assist@idris.fr](mailto:assist@idris.fr).
