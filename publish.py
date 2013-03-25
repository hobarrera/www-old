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
"""

class SettingsLoader:

    @staticmethod
    def load(settings_filename="settings.json"):
        settings_file = open(settings_filename)
        settings = json.load(settings_file)
        settings_file.close()
        return settings

class FileProcessor:

    @staticmethod
    def process_file(source_file, target_file):
        cwd = os.path.dirname(source_file)
        os.chdir(cwd)

        if relfilepath.endswith(".less"):
            target_file = target_file.replace(".less", ".css")
            # TODO: use python-less instead of invocating lessc
            os.system("lessc -x {source} {destination}".format(source=absfilepath, destination=target_file))
        elif relfilepath.endswith(".html"):
            env = Environment(loader=FileSystemLoader(cwd))
            template = env.get_template(os.path.basename(source_file))
            rendered_file = open(target_file, "w")
            rendered_file.write(template.render())
            rendered_file.close()
        elif relfilepath.endswith(".tex"):
            pass
        # TODO: process TEX files, converting them into PDFs
        else:
            shutil.copy(absfilepath, target_file)

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

    if os.path.exists(build_path):
        shutil.rmtree(build_path)
    os.mkdir(build_path)

    for (dirpath, dirnames, filenames) in os.walk(source_path):
        reldirpath = dirpath.replace(source_path, "")

        # Ignore all children if this directory is to be ignored:
        if reldirpath in ignore:
            del dirnames[:]
            del filenames[:]
            continue

        absdirpath = os.path.join(build_path, reldirpath)
        if not os.path.exists(absdirpath):
            os.mkdir(absdirpath)

        # TODO: pull git submodules (which might bring in stuff like cv.tex)

        for filename in filenames:
            relfilepath = os.path.join(reldirpath, filename)
            absfilepath = os.path.join(source_path, relfilepath)

            if relfilepath in ignore:
                continue

            target = os.path.join(build_path, relfilepath)

            FileProcessor().process_file(absfilepath, target)

    if arguments["publish"]:
        # TODO: search for a pure python rsync lib
        rsync_command = "rsync -rtzchlC --delete-after {build_path} {target_path}"
        rsync_command = rsync_command.format(build_path=build_path, target_path=settings["target_path"])
        os.system(rsync_command)
