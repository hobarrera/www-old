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

def process_html(source_file, target_file):
    env = Environment(loader=FileSystemLoader(os.path.dirname(source_file)))
    template = env.get_template(os.path.basename(source_file))
    rendered_file = open(target_file, "w")
    rendered_file.write(template.render())
    rendered_file.close()

def process_less(source_file, target_file):
    target_file = target_file.replace(".less", ".css")
    # TODO: use python-less instead of invocating lessc
    os.system("lessc -x {source} {destination}".format(source=source_file, destination=target_file))

def process_js(source_file, target_file):
    os.system('sh -c "jsmin < {} > {}"'.format(source_file, target_file))

def process_file(source_file, target_file):
    ext = os.path.splitext(source_file)[1]
    if len(ext) >= 2:
        fun = "process_{}".format(ext[1:])
        if fun in globals():
            globals()[fun](source_file, target_file)
            return

    shutil.copy(source_file, os.path.dirname(target_file))

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

    # Clean and recreate the target directory
    if os.path.exists(build_path):
        shutil.rmtree(build_path)
    os.mkdir(build_path)

    if arguments["publish"] or arguments["build"]:
        for (dirpath, dirnames, filenames) in os.walk(source_path):
            # Path relative to source_path
            reldirpath = dirpath.replace(source_path, "")

            # Ignore all children if this directory is to be ignored:
            if reldirpath in ignore:
                del dirnames[:]
                del filenames[:]
                continue

            abs_target_path = os.path.join(build_path, reldirpath)
            if not os.path.exists(abs_target_path):
                os.mkdir(abs_target_path)

            # TODO: pull git submodules (which might bring in stuff like cv.tex)

            for filename in filenames:
                if filename.startswith("_") or filename.startswith("."):
                    continue
                rel_filename = os.path.join(reldirpath, filename)
                target = os.path.join(build_path, rel_filename)

                if rel_filename not in ignore:
                    process_file(os.path.join(source_path, rel_filename), target)

    if arguments["publish"]:
        # TODO: search for a pure python rsync lib
        rsync_command = "rsync -rtzchlC --delete-after {build_path} {target_path}"
        rsync_command = rsync_command.format(build_path=build_path, target_path=settings["target_path"])
        os.system(rsync_command)
