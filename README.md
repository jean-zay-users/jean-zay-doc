# Collaborative documentation for Jean Zay users

[![Gitter](https://img.shields.io/gitter/room/jean-zay-users/jean-zay-doc.svg)](https://gitter.im/jean-zay-users/jean-zay-doc)
[![Documentation Status](https://readthedocs.org/projects/jean-zay-doc/badge/?version=latest)](https://jean-zay-doc.readthedocs.io)

**The documentation is now available here:
https://jean-zay-doc.readthedocs.io/en/latest/**

# Why this doc?

We are researchers and engineers in AI (very vague term but oh well ...) who
have managed to get access to Jean Zay and think this can be a very useful
cluster for your AI research.

At the time of writing (end November 2020), the GPU part of Jean Zay is still
underused and we think a user-contributed documentation could help people
navigating the access procedure and knowing a few necessary tips and tricks to
be productive on such a cluster.

**This is a collaborative doc, if you spot errors or things that
could be improved, open an
[issue](https://github.com/jean-zay-users/jean-zay-doc/issues/new) or even
better a [Pull Request (PR)](https://github.com/jean-zay-users/jean-zay-doc/compare)!**

We use gitter for chat, don't hesitate to get involved
[there](https://gitter.im/jean-zay-users/jean-zay-doc) and ask questions!

# See the generated doc in a PR

You can see the generated doc in a PR at the bottom of the PR page. This allows
you to double-check that the rendered HTML looks the way you intended.

It will look like the screenshot below. To view the generated doc you can click
on the "Details" link:
![](https://user-images.githubusercontent.com/1680079/146903507-d56addb6-c038-4d01-a151-933a8f261af2.png)

You can also generate the doc locally, see [this](#generating-the-doc-locally)
for instructions.

# Generating the doc locally

The documentation is using [mkdocs](https://www.mkdocs.org/) with a few
plugins. To install them:
```
pip install -e requirements.txt
```

To run `mkdocs` in development mode:
```
mkdocs serve
```

This launches a local server so that you can view the generated docs in your
browser. One very convenient feature to work on the doc is that the rendered
HTML is updated automatically when you change a `.md` file, so you can quickly
see the impact of your changes. The URL of the local server will be shown in
the output of the `mkdocs serve` command, for example:
```
INFO     -  [15:07:11] Serving on http://127.0.0.1:8000/
```
