""" Application commands common to all interfaces.

"""
from .hello import main as hello
from .readwav import main as readwav


__all__ = "hello", "readwav"
