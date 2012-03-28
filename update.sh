#!/bin/bash

sync

rsync -rtvzchlC --progress --stats --delete-after --rsync-path=/usr/local/bin/rsync  \
   /home/hugo/workspace/www/code/  \
   root@elysion.ubertech.com.ar:/var/www/sites/default/  \
   -e 'ssh -i/home/hugo/.certs/root@elysion.unencrypted'

echo "Update complete"

exit 0
