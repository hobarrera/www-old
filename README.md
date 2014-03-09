My Website
==========

This repository contains my personal website, https://hugo.barrera.io/.

There's a small publication script included (which is still WIP), which pre-processes some file types before publishing.
Hopefully, someone will find some use for this (rather simple) script.

These are some features already implemented:

 * Process HTML file so as to use jinja2 templating.
 * Process [LESS](http://lesscss.org/) files into CSS.
 * Use rsync to publish changes.

These are some pending features for when I get the time:

 * Pull submodules using git (for example, cv.pdf should be pulled from it's own repo).
 * Tidy up the code (this was a rather quick - and ugly - hack).
 * Process TEX files and just publish the resulting PDF files (but don't version them!).

Licensing
---------
You are free to reuse parts of this website and use it as a reference so long
as you do not try to imitate it, or personify anybody related to it.