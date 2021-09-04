"""Main"""

import log
import sys
import os

import diff.diff as diff
import materials.materials as materials
import plot.plot as plot
import cli #local module
import settings #local




def scan_path(path):
    """Scans the path inserted for supported filetypes and returns as list"""

    dir_files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        dir_files.extend(filenames)
        

    filenames = []
    for file in dir_files:
        if file.split(".")[-1] == "xye":
            filenames.append(file)
		
    #Tell the user about the files found
    logger.info("the scan_path() command found the following files in the specified folder: {}".format(filenames))
    print("wow")
    return filenames

if __name__ == "__main__":
    # Initialize global settings
    settings.init() 

    # Capture input arguments
    args = cli.args().args

    # Initialize logger
    logger = log.setup_custom_logger('root')
    logger.debug('Message from main')

    # Handle input arguments

    if os.path.isdir(args.path):
        scan_path(args.path)

    

    if args.plot == True:
        print("Plotting")
    else:
        print("not potting")
