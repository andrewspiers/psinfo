#!/usr/bin/python
"""Return some information about the tomcat process.

Usage: 
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
    parser = argparse.ArgumentParser(description = __doc__ )
    parser.add_argument(
        "--pid",
        action='store_true',
        help = "return the pid of the process."
        )
    parser.add_argument(
        "--threads",
        action='store_true',
        help = "return the number of threads of the process."
        )
    parser.add_argument(
        "--memper",
        action='store_true',
        help = "return the percentage the processes's RSS as a percentage of system memory."
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
    #if not args.attribute:
    #    print 'tomcat pid is ' + str(tom.pid)
    #    print 'thread count :',tom.get_num_threads()
    #    print 'rss / physical mem :',tom.get_memory_percent()
    if args.pid:
        print tom.pid
    if args.threads:
        print tom.get_num_threads()
    if args.memper:
        print tom.get_memory_percent()
