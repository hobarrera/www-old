#!/usr/bin/env python2

import os

local_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"source/")
remote_path = "/var/www/https/ar.com.hugoosvaldobarrera/"

rsync_command = """\
rsync -rtvzchlC --progress --stats --rsync-path=/usr/local/bin/rsync  \
   {} root@elysion.ubertech.com.ar:{}  \
""".format(local_path, remote_path)
# use --delete-after to delete files that don't exist locally

# TODO: rebuild CV from tex (submodule) and push that. gitignore the pdf
os.system(rsync_command)
