""" Implement the hello command.

"""
import csv
import sys

from datetime import datetime
from uuid import uuid4
from shutil import copy
from pathlib import Path
from guano import GuanoFile
from ..core.logger import logger


def main(wav_dir, input_file) -> str:
    """ Execute the command.

    :param wav_dir: the directory where wav files are stored
    :param input_file: the full path of the csv input file generated by 'readwav'
    """
    logger.debug("executing hello command")

    try:
        backup_dir = Path(wav_dir[0]).joinpath('guanoctl_out')
    except FileNotFoundError:
        logger.error('The wav directory does not exist!')
        sys.exit()

    try:
        backup_dir.mkdir()
    except FileExistsError:
        logger.error('The working directory already exists.')
        sys.exit()

    for file in Path(wav_dir[0]).glob('*.[Ww][Aa][Vv]'):
        copy(file.as_posix(), backup_dir.as_posix())

    with open(input_file, 'r', newline='') as metadata_file:
        reader = csv.DictReader(metadata_file)

        for row in reader:
            gf = GuanoFile(backup_dir.joinpath(row['Original Filename']).as_posix())

            for key, value in row.items():

                if key == 'Filter HP':
                    # gf[key] = float(value)
                    pass
                elif key == 'Length':
                    # gf[key] = float(value)
                    pass
                elif key == 'Loc Elevation':
                    # gf[key] = float(value)
                    pass
                elif key == 'Loc Accuracy':
                    # gf[key] = int(value)
                    pass
                elif key == 'Samplerate':
                    # gf[key] = int(value)
                    pass
                elif key == 'TE':
                    # gf[key] = int(value)
                    pass
                elif key == 'Loc Position':
                    pass
                elif key == 'Timestamp':
                    pass
                elif key == 'Note':
                    # gf[key] = value.replace('\\n', '\n')
                    pass
                else:
                    gf[key] = value

            gf.write()

    return "Hello"  # TODO: use f-string for Python 3.6+
