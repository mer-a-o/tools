"""
This script changes variable name aerosol_optical_depth_4 
to aerosol_optical_depth_4 for viirs files on r2d2 archive.
Yaml includes r2d2 keys such as start, end, window_length
obs_frequency, provider, obs_type, and source_path
"""

import argparse
from solo.configuration import Configuration
from solo.date import date_sequence, JediDate, DateIncrement
import h5py


def copy_to(h5obj: h5py.Group, source: str, target: str):
    if source in h5obj:
        if target in h5obj:
            del h5obj[target]
        return h5obj.copy(source, target)


parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='The input experiment YAML file')
args = parser.parse_args()
input_file = args.input_file

config = Configuration(input_file)
dates = date_sequence(config.start, config.end, config.obs_frequency)
obs_types = config.obs_types
keys_to_fix = ['ObsValue', 'ObsError', 'PreQC']

for date in dates:
    date = JediDate(date)
    for obs_type in obs_types:
        obs_name = f'{config.source_path}/{date}/{config.provider}.obs.{config.obs_type}.{date}.{config.window_length}.nc4'
        try:
            with h5py.File(obs_name, 'r+') as dst:
                for key in keys_to_fix:
                    if f"/{key}/aerosol_optical_depth_4" in dst.keys():
                        copy_to(h5obj=dst,
                                source=f"/{key}/aerosol_optical_depth_4",
                                target=f"/{key}/aerosol_optical_depth")
                        del dst[f"{key}/aerosol_optical_depth_4"]
        except FileNotFoundError:
            print(f'{obs_name} does not exist')
