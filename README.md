# Why this doc?

We are researchers and engineers in AI (very vague term but oh well ...) who
have managed to get access to Jean Zay and think this can be a very useful
cluster for your AI research.

At the time of writing (end January 2020), the GPU part of Jean Zay is very
much underused and we think a user-contributed documentation could help people
navigating the access procedure and knowing a few necessary tips and tricks to
be productive on such a cluster.

**This is supposed to be a collaborative doc, if you spot errors or things that
could be improved, open an
[issue](https://github.com/jean-zay-users/jean-zay-doc/issues/new) or even
better a [Pull Request (PR)](https://github.com/jean-zay-users/jean-zay-doc/compare)!**

We use gitter for chat, don't hesitate to get involved there and ask questions!

[![Gitter](https://img.shields.io/gitter/room/jean-zay-users/jean-zay-doc.svg)](https://gitter.im/jean-zay-users/jean-zay-doc)

# Content

- [Access procedure](./access-procedure.md). The access procedure for Jean Zay
  will take roughly 3 weeks (add 1-2 monts on top of that if you are not French
  for background security checks). It does seem long but it is definitely worth
  it.
- [Tips and tricks](./tips-and-tricks.md)
- [Limitations](./limitations.md)

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

# Useful links

Jean Zay doc for AI users (French only for now): http://www.idris.fr/ai/

Hardware: http://www.idris.fr/eng/jean-zay/cpu/jean-zay-cpu-hw-eng.html

Doc: http://www.idris.fr/eng/jean-zay/

Doc in French (more accurate sometimes): http://www.idris.fr/jean-zay/

Email for Jean Zay user support: [assist@idris.fr](mailto:assist@idris.fr).

# Generic advice

- There is a big cultural gap between traditional HPC (High Performance
  Computing) users and AI users. For example, most traditional "serious" HPC
  clusters do not have access to the internet, yes you have read this
  correctly, people in traditional HPC do not need internet access to work on
  their problems.
- So far every interaction we have had with Jean Zay user support has been very
  positive. Even if there may be some frustration (on both sides), try to be
  both pedagogical and constructive when you send an email to
  [assist@idris.fr](mailto:assist@idris.fr).
