#!/usr/bin/env python2

import os
import sys
import shutil
import json
from docopt import docopt
from jinja2 import Environment, FileSystemLoader

usage = """Publish.py

Usage:
  publish.py publish [--settings=<FILE>]
  publish.py build [--settings=<FILE>]
  publish.py serve [--settings=<FILE>]
  publish.py -h | --help
  publish.py --version

Options:
  --settings=<FILE>    Use a different settings file.

Files staring underscore or period are ignored.
LESS files are compiled to CSS.
HTML files are trated as jinja2-templated files. Ordinary HTML files won't be
affected.
JavaScript files will be compressed.
"""

class SettingsLoader:

    @staticmethod
    def load(settings_filename="settings.json"):
        settings_file = open(settings_filename)
        settings = json.load(settings_file)
        settings_file.close()
        return settings


class Context:

    source_root=None
    target_root=None

    ignore_list=None

    source_file=None

    def __init__(self, source_root, target_root, ignore_list):
        self.source_root = source_root
        self.target_root = target_root
        self.ignore_list = ignore_list

    @property
    def target_path(self):
        return os.path.join(self.target_root, self.source_file)

    @property
    def source_path(self):
        return os.path.join(self.source_root, self.source_file)


###########################
### FILE PROCESSING METHODS

def process_html(context):
    env = Environment(loader=FileSystemLoader(context.source_root))
    template = env.get_template(context.source_file)
    rendered_file = open(context.target_path, "w")
    rendered_file.write(template.render())
    rendered_file.close()

def process_less(context):
    target_file = context.target_path.replace(".less", ".css")
    # TODO: use python-less instead of invocating lessc
    os.system("lessc -x {source} {destination}".format(source=context.source_path, destination=target_file))

def process_js(context):
    os.system('sh -c "jsmin < {} > {}"'.format(context.source_path, context.target_path))

def process_file(context):
    ext = os.path.splitext(context.source_path)[1]
    if len(ext) >= 2:
        fun = "process_{}".format(ext[1:])
        if fun in globals():
            globals()[fun](context)
            return

    shutil.copy(context.source_path, context.target_path)

###########################

if __name__ == '__main__':
    # TODO: accept all settings as arguments
    arguments = docopt(usage, version='Publish.py 0.1')

    if arguments["--settings"]:
        settings = SettingsLoader().load(arguments["--settings"])
    else:
        settings = SettingsLoader().load()

    source_path = settings["source_path"]
    build_path = settings["build_path"]
    ignore = settings["ignore"]

    context = Context(source_path, build_path, ignore)

    # Clean and recreate the target directory
    if os.path.exists(context.target_root):
        shutil.rmtree(context.target_root)
    os.mkdir(context.target_root)

    if arguments["publish"] or arguments["build"] or arguments["serve"]:
        for (dirpath, dirnames, filenames) in os.walk(context.source_root):
            # Path relative to context.source_root
            reldirpath = dirpath.replace(context.source_root, "")

            # Ignore all children if this directory is to be ignored:
            if reldirpath in ignore:
                del dirnames[:]
                del filenames[:]
                continue

            abs_target_path = os.path.join(context.target_root, reldirpath)
            if not os.path.exists(abs_target_path):
                os.mkdir(abs_target_path)

            # TODO: pull git submodules (which might bring in stuff like cv.tex)

            for filename in filenames:
                if filename.startswith("_") or filename.startswith("."):
                    continue
                rel_filename = os.path.join(reldirpath, filename)
                target = os.path.join(context.target_root, rel_filename)

                if rel_filename not in ignore:
                    context.source_file = rel_filename
                    process_file(context)

    if arguments["publish"]:
        # TODO: search for a pure python rsync lib
        rsync_command = "rsync -rtzchlC --delete-after {build_path} {target_path}"
        rsync_command = rsync_command.format(build_path=build_path, target_path=settings["target_path"])
        os.system(rsync_command)

    if arguments["serve"]:
        os.system("darkhttpd build/")
