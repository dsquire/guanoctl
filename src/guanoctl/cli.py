""" Implementation of the command line interface.

"""
# import os
from argparse import ArgumentParser
from inspect import getfullargspec

from . import __version__
from .api import hello
from .api import readwav
from .api import writewav
from .core.config import config
from .core.logger import logger

__all__ = "main",


def main(argv=None) -> int:
    """ Execute the application CLI.

    :param argv: argument list to parse (sys.argv by default)
    :return: exit status
    """
    args = _args(argv)
    logger.start(args.warn or "DEBUG")  # can't use default from config yet
    logger.debug("starting execution")
    config.load(args.config)
    config.core.config = args.config
    if args.warn:
        config.core.logging = args.warn
    logger.stop()  # clear handlers to prevent duplicate records
    logger.start(config.core.logging)
    command = args.command
    args = vars(args)
    spec = getfullargspec(command)
    if not spec.varkw:
        # No kwargs, remove unexpected arguments.
        args = {key: args[key] for key in args if key in spec.args}
    try:
        command(**args)
    except RuntimeError as err:
        logger.critical(err)
        return 1
    logger.debug("successful completion")
    return 0


def _args(argv):
    """ Parse command line arguments.

    :param argv: argument list to parse
    """
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", action="append",
                        help="config file [etc/config.yml]")
    parser.add_argument("-v", "--version", action="version",
                        version="guanoctl {:s}".format(__version__),
                        help="print version and exit")
    parser.add_argument("-w", "--warn", default="WARN",
                        help="logger warning level [WARN]")
    common = ArgumentParser(add_help=False)  # common subcommand arguments
    # common.add_argument('wav_dir')
    # common.add_argument("--name", "-n", default="World", help="greeting name")
    subparsers = parser.add_subparsers(title="subcommands")
    _hello(subparsers, common)
    _readwav(subparsers, common)
    _writewav(subparsers, common)
    args = parser.parse_args(argv)
    if not args.config:
        # Don't specify this as an argument default or else it will always be
        # included in the list.
        args.config = "etc/config.yml"
    return args


def _hello(subparsers, common):
    """ CLI adaptor for the api.hello command.

    :param subparsers: subcommand parsers
    :param common: parser for common subcommand arguments
    """
    parser = subparsers.add_parser("hello", parents=[common])
    parser.set_defaults(command=hello)
    return


def _readwav(subparsers, common):
    """CLI adapter for the api.readwav command.

    :param subparsers: subcommand parsers
    :param common: parser for common subcommand arguments
    """
    parser = subparsers.add_parser('readwav', parents=[common])
    parser.add_argument('wav_dir', nargs=1, help='Full path of a directory containing one or more sound files.')
    parser.add_argument('-o', '--output_file', type=str)  # , default=os.path.join(os.getcwd(), 'guano_metadata.csv')
    parser.set_defaults(command=readwav)
    return


def _writewav(subparsers, common):
    """ CLI adaptor for the api.writewav command.

    :param subparsers: subcommand parsers
    :param common: parser for common subcommand arguments
    """
    parser = subparsers.add_parser('writewav', parents=[common])
    parser.add_argument('wav_dir', nargs=1, help='Full path of a directory containing one or more sound files.')
    parser.add_argument('-i', '--input_file', type=str)  # , default=os.path.join(os.getcwd(), 'guano_metadata.csv')
    parser.set_defaults(command=writewav)
    return


# Make the module executable.

if __name__ == "__main__":
    try:
        status = main()
    except Exception:  # 'Exception' added by DS
        logger.critical("shutting down due to fatal error")
        raise  # print stack trace
    else:
        raise SystemExit(status)
