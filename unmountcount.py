#!/usr/bin/python

from sys import exit
from swift.common.constraints import check_mount
from swift.common.utils import whataremyips
from swift.common.ring import Ring

try:
    ring = Ring('/etc/swift/object.ring.gz')
except IOError:
    exit()

my_ips = whataremyips()
mounted = 0
drivecount = 0

for dev in ring.devs:
    try:
        if dev['ip'] in my_ips and float(dev['weight']) > 0:
            drivecount += 1
            if check_mount('/srv/node', dev['device']):
                mounted += 1
    except TypeError:
        pass

unmounted = drivecount - mounted
if unmounted > 0:
    print unmounted

