#!/usr/bin/env python

import argparse
from bioblend.galaxy import GalaxyInstance
import yaml

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-G', '--galaxy-instance',
                            default='embassy',
                            help='Galaxy server instance name')
arg_parser.add_argument('-C', '--conf',
                            required=True,
                            help='A yaml file describing the galaxy credentials')
args = arg_parser.parse_args()

def get_instance(conf, name='__default'):
    with open(conf, "r") as yp:
        data=yaml.safe_load(yp)
    assert name in data, 'unknown instance'
    entry = data[name]
    if isinstance(entry, dict):
        return entry
    else:
        return data[entry]

ins = get_instance(args.conf, name=args.galaxy_instance)
gi = GalaxyInstance(ins['url'], key=ins['key'])

for dt in gi.datatypes.get_datatypes():
    print(dt)
