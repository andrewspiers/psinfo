#!/usr/bin/python
"""NRPE check that examines the percentage of physical memory used by the
tomcat process (RSS) against the system physical memory.

Generates a warning state if the memory exceeds -w (default 50%), and a
critical state if the memory exceeds -c (default 80%).
"""

import tomcatinfo  # this relies on psutil

import argparse
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-w",
        type=int,
        default=50,
        choices=range(0, 100),
        help='warning level',
        )
    parser.add_argument(
        "-c",
        type=int,
        default=80,
        choices=range(0, 100),
        help='critical level',
        )
    args = parser.parse_args()
    toms = tomcatinfo.findtomcat()
    if len(toms) < 1:
        print ('UNKNOWN: No tomcat process found')
        sys.exit(3)
    if len(toms) > 1:
        print ('UNKNOWN: More than one tomcat process found.')
        sys.exit(3)
    tom = toms[0]
    mp = tom.get_memory_percent()
    if args.w >= args.c:
        print ('UNKNOWN: critical level must exceed warning level')
        sys.exit(3)
    if mp < args.w:
        print ("OK - %#.2F%% of physical memory used." % mp)
        sys.exit(0)
    elif mp < args.c:
        print ("WARNING - %#.2F%% of physical memory used." % mp)
        sys.exit(1)
    elif mp > args.c:
        print ("CRITICAL - %#.2F%% of physical memory used." % mp)
        sys.exit(2)
    else:
        print ("UNKNOWN - %#.2F%% of physical memory used. Something is awry."
                % mp)
        sys.exit(3)
