""" Implement the readwav command.

"""
import csv

from datetime import datetime
from uuid import uuid4
from pathlib import Path
from guano import GuanoFile
from ..core.logger import logger


def main(wav_dir, output_file) -> str:
    """ Execute the command.

    :param wav_dir: directory containing one more more wav files
    :param output_file: full path to GUANO metadata output file
    """
    logger.debug("executing readwav command")

    guano_strict = {'GUANO|Version': '',
                    'Filter HP': '',
                    'Filter LP': '',
                    'Firmware Version': '',
                    'Hardware Version': '',
                    'Humidity': '',
                    'Length': '',
                    'Loc Accuracy': '',
                    'Loc Elevation': '',
                    'Loc Position': '',
                    'Make': '',
                    'Model': '',
                    'Note': '',
                    'Original Filename': '',
                    'Samplerate': '',
                    'Serial': '',
                    'Species Auto ID': '',
                    'Species Manual ID': '',
                    'Tags': '',
                    'TE': '',
                    'Temperature Ext': '',
                    'Temperature Int': '',
                    'Timestamp': ''}

    combined_metadata = {}
    combined_metadata.update(guano_strict)

    if output_file is None:
        output_file = str(Path(wav_dir[0]).joinpath(datetime.now().strftime('%Y%m%d-%H%M%S'))) + '.csv'

    with open(output_file, 'w', newline='') as metadata_file:
        for file in Path(wav_dir[0]).glob('*.[Ww][Aa][Vv]'):
            try:
                gf = GuanoFile(Path(wav_dir[0]).joinpath(str(file.name)))
            except ValueError:
                logger.warn(file.name + ' is not GUANO compliant')
            else:
                guano_metadata = {key: value for key, value in gf.items()}
                combined_metadata.update(guano_metadata)

                if 'ABCD|uuid' not in guano_metadata.keys():
                    combined_metadata.update({'ABCD|uuid': uuid4()})

                combined_metadata.update({'Original Filename': file.name})

                if metadata_file.tell() == 0:
                    writer = csv.DictWriter(metadata_file, dialect=csv.excel, fieldnames=combined_metadata.keys())
                    writer.writeheader()

                writer.writerow(combined_metadata)

    return 'Output file written to: ' + metadata_file.name
