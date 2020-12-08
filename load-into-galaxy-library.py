#!/usr/bin/env python

import argparse
from bioblend.galaxy import GalaxyInstance
from library import *
import yaml
import logging

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-l","--lib-def", help="Path to YAML library definition")
arg_parser.add_argument('-G', '--galaxy-instance',
                            default='embassy',
                            help='Galaxy server instance name')
arg_parser.add_argument('-C', '--conf',
                            required=True,
                            help='A yaml file describing the galaxy credentials')
args = arg_parser.parse_args()

logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(message)s',
        datefmt='%d-%m-%y %H:%M:%S')

def get_instance(conf, name='__default'):
    with open(conf, "r") as yp:
        data=yaml.safe_load(yp)
    assert name in data, 'unknown instance'
    entry = data[name]
    if isinstance(entry, dict):
        return entry
    else:
        return data[entry]

logging.info("Reading file system library definition...")
fs_libs = FileSystemLibrary.read_from_yaml(args.lib_def)

ins = get_instance(args.conf, name=args.galaxy_instance)
gi = GalaxyInstance(ins['url'], key=ins['key'])

for fs_lib in fs_libs:
    logging.info(f"Processing library {fs_lib.name}")
    lgl = LibraryGalaxyLoader(gi, fs_lib)
    lgl.populate_galaxy_lib()
