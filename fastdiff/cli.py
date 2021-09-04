"""Handles the command line interface of fastdiff"""

import argparse
import logging
import settings #local


class args():
    """Keeps all our cli arguments"""

    def __init__(self):
        """Initiates input arguments parser"""
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
            "--initplot", 
            help="Calculates the experiment temperature from an internal platina standard",
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

        self.args = parser.parse_args()

        if self.args.debug:
            settings.LOGLEVEL = logging.DEBUG
        elif self.args.verbose:
            settings.LOGLEVEL = logging.INFO
        else:
            settings.LOGLEVEL = logging.WARNING

        if self.args.initplot:
            import toml

            kwargs = {
                "files" : [   
                    "relative/path/to/file.xy",
                    "relative/path/to/another-file.xy",],
                "zoom" : [(18.0,19.5), (35.0,40.0)],
                "xlim" : (15, 70),
                "ticks" : ['SRM', 'Fd3m'],
                "d_spacing" : True,
            }

            with open('plotconfig.toml', 'w') as f:
                text = toml.dump(kwargs, f)


    def __repr__(self):
        return self.args

    def __str__(self):
        return str(self.args)