"""
This scripts runs ioda-upgrade-v2-to-v3.x on r2d2 archive.
Yaml includes keys r2d2 keys and path to source and output data, 
path to jedi bin directory and ObsSpace.yaml
To run this script on VIIRS data users need to first run 
viirs_fix.py to fix the variable name
"""

import os
import argparse
from solo.configuration import Configuration
from solo.date import date_sequence, JediDate, DateIncrement

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='The input experiment YAML file')
args = parser.parse_args()
input_file = args.input_file

config = Configuration(input_file)
dates = date_sequence(config.start, config.end, config.obs_frequency)

for date in dates:
    date = JediDate(date)
    input_file = f'{config.source_path}/{date}/{config.provider}.obs.{config.obs_type}.{date}.{config.window_length}.nc4'
    if not (os.path.exists(input_file)):
        print(f'{input_file} does not exist')
    else:
        print(f'processing {input_file}')

    output_dir = f'{config.output_path}/{date}'
    if not (os.path.exists(output_dir)):
        print(f'{output_dir} does not exist')
        os.makedirs(output_dir)

    output_file = f'{output_dir}/{config.provider}.obs.{config.obs_type}.{date}.{config.window_length}.nc4'

    os.system(f'{config.jedi_build}/ioda-upgrade-v2-to-v3.x {input_file} {output_file} {config.obsspace_yaml}')
