"""Keeps all global variables"""

import logging

def init():
    global LOGLEVEL
    global WAVELENGTH

    LOGLEVEL = logging.WARNING
    WAVELENGTH = 0.62231 # default wavelength in Angstrom