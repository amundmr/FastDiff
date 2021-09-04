"""Handles the command line interface of fastdiff"""

import argparse

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
            help="Plot data with matplotlib",
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

    def __repr__(self):
        return self.args

    def __str__(self):
        return str(self.args)