"""Handles the command line interface of fastdiff"""

import argparse
import settings #local
from log import LOG



parser = argparse.ArgumentParser()

parser.add_argument(
    "path", 
    help="Folder path or File path of the data you want to use"
    )

parser.add_argument(
    "-p", 
    "--plot", 
    type = str,
    nargs = '?',
    help="Plot data with matplotlib",
    const=True
    )


parser.add_argument(
    "--init", 
    help="Initializes working directory",
    action="store_true"
    )

parser.add_argument(
    "--calctemp", 
    help="Calculates the experiment temperature from an internal platina standard",
    action="store_true"
    )

parser.add_argument(
    "-v", 
    "--verbose", 
    help="Switches the logging level to INFO",
    action="store_true"
    )

parser.add_argument(
    "--debug", 
    help="Switches the logging level to DEBUG",
    action="store_true"
    )

args = parser.parse_args()


# Handle verbosity
if args.debug:
    LOG.set_level("DEBUG")
elif args.verbose:
    LOG.set_level("INFO")
else:
    LOG.set_level("SUCCESS")


if args.init:

    LOG.debug("Initializing workfolder")
    import toml
    import os

    # Make user folders
    os.mkdir("./CIF")
    os.mkdir("./data")

    # Make config templates
    kwargs = {
        "zoom" : [(18.0,19.5), (35.0,40.0)],
        "xlim" : (15, 70),
        "ticks" : ['SRM', 'Fd3m'],
        "d_spacing" : True,
    }

    with open('plot.toml', 'w') as f:
        toml.dump(kwargs, f)