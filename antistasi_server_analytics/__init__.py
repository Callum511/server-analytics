"""Antistasi Server Analytics"""

from pathlib import Path

__version__ = '0.0.1'

if __package__ is None:
    __app_name__ = THIS_FILE_DIR = Path(__file__).parent.resolve().name
else:
    __app_name__ = str(__package__)

__app_pretty_name__ = __app_name__.replace("_", " ").title()
