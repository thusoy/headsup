#!/usr/bin/env python

# landscape-sysinfo-mini.py -- a trivial re-implementation of the
# sysinfo printout shown on debian at boot time. No twisted, no reactor, just /proc.
# 
# Loosly based on https://github.com/jnweiger/landscape-sysinfo-mini which in turn was 
# inspired by ubuntu 14.10 /etc/update-motd.d/50-landscape-sysinfo

from __future__ import division

import os
import re
import subprocess
import time


def main():
    load_average = get_system_load_average()
    processes = get_number_of_running_processes()
    defaultdev = get_default_net_device()
    root_usage, root_size_in_gb = get_root_fs_stats()
    ipaddr = get_device_address(defaultdev)
    num_users = get_number_of_logged_in_users()
    memory_usage, swap_usage = get_memory_stats()

    # For percentages, direct percentage formatting with '{:.2%}'.format(val)
    # could also have been used, but was found to be significantly slower than the
    # equivalent %-style formatting.
    print "  System information as of %s\n" % time.asctime()
    print "  System load:  %.1f%%              Processes:        %d" % (load_average*100, processes)
    print "  Usage of /:   %.1f%% of %.2fGB   Users logged in:  %d" % (root_usage*100, root_size_in_gb, num_users)
    print "  Memory usage: %.1f%%              IP address for %s: %s" % (memory_usage*100, defaultdev, ipaddr)
    print "  Swap usage:   %s" % (".1f%%" % swap_usage*100 if swap_usage else '---')


def get_memory_stats():
    memory_info = get_meminfo()
    memory_usage = 1 - memory_info['MemFree:']/(memory_info['MemTotal:'] or 1)
    swap_total = memory_info['SwapTotal:']
    if swap_total == 0:
        swap_usage = None
    else:
        swap_usage = 1 - memory_info['SwapFree:']/(swap_total)
    return memory_usage, swap_usage


def get_system_load_average():
    with open('/proc/loadavg') as fh:
        one_min_avg, five_min_avg, fifteen_min_avg, _ = fh.read().split(None, 3)
        return float(five_min_avg)


def get_number_of_running_processes():
    number_re = re.compile('^[0-9]*$')
    processes = filter(lambda e: number_re.match(e), os.listdir('/proc'))
    return len(processes)


def get_root_fs_stats():
    statfs = os.statvfs('/')
    root_usage = 1 - statfs.f_bavail/statfs.f_blocks
    root_size_in_gb = statfs.f_bsize*statfs.f_blocks/2**30
    return (root_usage, root_size_in_gb)


def get_device_address(device):
    """ find the local ip address on the given device """
    if device is None:
        return None
    command = ['ip', 'route', 'list', 'dev', device]
    ip_routes = subprocess.check_output(command).strip()
    for line in ip_routes.split('\n'):
        seen = ''
        for a in line.split():
            if seen == 'src':
                return a
            seen = a
    return None


def get_default_net_device():
    """ Find the device where the default route is. """
    with open('/proc/net/route') as fh:
        for line in fh:
            iface, dest, _ = line.split(None, 2)
            if dest == '00000000':
                return iface
    return None


def get_number_of_logged_in_users():
    logged_in_users = subprocess.check_output(['who']).strip()
    return len(logged_in_users.split('\n'))


def get_meminfo():
    items = {}
    with open('/proc/meminfo') as fh:
        for line in fh:
            line_items = line.split()
            if len(line_items) == 3:
                key, value, unit = line_items
            else:
                key, value = line_items
            items[key] = int(value)
    return items


if __name__ == '__main__':
    main()
