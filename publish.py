#!/usr/bin/env python2

import os
import sys
import shutil
import json
from docopt import docopt

usage = """Publish.py

Usage:
  publish.py publish
  publish.py build
  publish.py -h | --help
  publish.py --version

"""

class SettingsLoader:

    def load(filename="settings.json"):
        settings_file = open("settings.json")
        settings = json.load(settings_file)
        settings_file.close()
        return settings

if __name__ == '__main__':
    # TODO: accept all settings as arguments
    arguments = docopt(usage, version='Publish.py 0.1')
    settings = SettingsLoader().load()

    source_path = settings["source_path"]
    build_path = settings["build_path"]
    ignore = settings["ignore"]

    if os.path.exists(build_path):
        shutil.rmtree(build_path)
    os.mkdir(build_path)

    for (dirpath, dirnames, filenames) in os.walk(source_path):
        reldirpath = dirpath.replace(source_path, "")
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

            if filename.endswith(".less"):
                target = target.replace(".less", ".css")
                # TODO: use python-less instead of invocating lessc
                os.system("lessc -x {source} {destination}".format(source=absfilepath, destination=target))
            # TODO: process HTML files, using jinja2
            # TODO: process TEX files, converting them into PDFs
            else:
                shutil.copy(absfilepath, target)

    if arguments["publish"]:
        # TODO: search for a pure python rsync lib
        rsync_command = "rsync -rtzchlC --delete-after {build_path} {target_path}"
        rsync_command = rsync_command.format(build_path=build_path, target_path=settings["target_path"])
        os.system(rsync_command)
