""" Implement the readwav command.

"""
import csv
from datetime import datetime
from pathlib import Path
from guano import GuanoFile
from ..core.logger import logger


def main(wav_dir, output_file) -> str:
    """ Execute the command.

    :param wav_dir: directory containing one more more wav files
    :param output_file: full path to GUANO metadata output file
    """
    logger.debug("executing readwav command")

    guano_strict = {'GUANO|Version': None,
                    'Filter HP': None,
                    'Filter LP': None,
                    'Firmware Version': None,
                    'Hardware Version': None,
                    'Humidity': None,
                    'Length': None,
                    'Loc Accuracy': None,
                    'Loc Elevation': None,
                    'Loc Position': None,
                    'Make': None,
                    'Model': None,
                    'Note': None,
                    'Original Filename': None,
                    'Samplerate': None,
                    'Serial': None,
                    'Species Auto ID': None,
                    'Species Manual ID': None,
                    'Tags': None,
                    'TE': None,
                    'Temperature Ext': None,
                    'Temperature Int': None,
                    'Timestamp': None}

    combined_metadata = {}
    combined_metadata.update(guano_strict)

    if output_file is None:
        output_file = str(Path(wav_dir[0]).joinpath(datetime.now().strftime('%Y%m%d-%H%M%S'))) + '.csv'

    try:
        metadata_file = open(output_file, 'w', newline='')
    except OSError:
        logger.error(metadata_file.name + ' could not be opened!')
    else:
        with metadata_file:
            for file in Path(wav_dir[0]).glob('*.[Ww][Aa][Vv]'):
                try:
                    gf = GuanoFile(Path(wav_dir[0]).joinpath(str(file.name)))
                except ValueError:
                    logger.warn(file.name + ' is not GUANO compliant')
                else:
                    guano_metadata = {key: value for key, value in gf.items()}
                    combined_metadata.update(guano_metadata)

                    # if 'ABCD|uuid' not in guano_metadata.keys():
                    #     combined_metadata.update({'ABCD|uuid': uuid4()})

                    combined_metadata.update({'Original Filename': file.name})

                    if metadata_file.tell() == 0:
                        writer = csv.DictWriter(metadata_file, dialect=csv.excel, fieldnames=combined_metadata.keys())
                        writer.writeheader()

                    writer.writerow(combined_metadata)

    return 'Output file written to: ' + metadata_file.name
