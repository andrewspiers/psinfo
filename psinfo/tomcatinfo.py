#!/usr/bin/python
"""Return the pid, number of threads, or percentage of physical memory used
by any tomcat process running on the system.

"""

import psutil

import argparse
import sys


def findtomcat():
    """return a list of the tomcat processes"""
    processes = psutil.process_iter()
    tomcats = []
    for i in processes:
        if i.name == "java":
            for j in i.cmdline:
                if j.find('tomcat7/bin/bootstrap.jar') > -1:
                    tomcats.append(i)
    return tomcats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "attribute",
        choices=['threads', 'pid', 'memper'],
        )
    args = parser.parse_args()
    toms = findtomcat()
    if len(toms) < 1:
        sys.stderr.write('No tomcat process found')
        raise IndexError
    if len(toms) > 1:
        sys.stderr.write('More than one tomcat process found.')
        raise IndexError
    tom = toms[0]
    if args.attribute == "pid":
        print tom.pid
    if args.attribute == "threads":
        print tom.get_num_threads()
    if args.attribute == "memper":
        print tom.get_memory_percent()
