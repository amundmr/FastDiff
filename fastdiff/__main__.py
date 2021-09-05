"""Main"""

from log import LOG

import sys
import os
import pandas as pd

#from cli import args
#import settings #local

# Initialize global settings
#settings.init() 


# Importing submodules
#import diff.diff as diff
#import materials.materials as materials
#import plot.plot as plot

class Mainclass():
    """Main class"""

    def __init__(self, args):
        """Initialize main class"""
        LOG.debug("Initializing Main object")
        self.args = args


        # Initialize list of diff objects
        self.diffs = []


        # Act on input arguments
        if os.path.isdir(self.args.path):
            self.scan_path(self.args.path)
        elif os.path.isfile(self.args.path):
            self.diffs.append(diff.diff(self.args.path))


        if type(self.args.plot) is str:
            import toml
            with open(self.args.plot) as f:
                self.plotkwargs = toml.load(f, _dict=dict)

            plot.plot(self.diffs, **self.plotkwargs)
        elif self.args.plot:
            plot.plot(self.diffs)

        if self.args.calctemp:
            self.calc_temps()


    def scan_path(self, path):
        """Scans the path inserted for supported filetypes and returns as list"""

        dir_files = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            dir_files.extend(filenames)
            

        filenames = []
        for file in dir_files:
            if file.split(".")[-1] == "xye":
                filenames.append(file)
                self.diffs.append(diff.diff(os.path.join(path,file)))
            
        #Tell the user about the files found
        LOG.info("the scan_path() command found the following files in the specified folder: {}".format(filenames))
        

    def calc_temps(self):
        """Takes every diffractogram and runs get_pt_info on it. 
        Right now it only ask for the temperature calculated from 2nd degree polynomial peak fitting
        At the end it creates a dataframe with the filenames and temperature"""        

        data = []
        for diff in self.diffs:
            pt_info = diff.get_pt_info(Temp = True)
            pt_info["Filename"] = diff.name
            data.append(pt_info)

        self.df_temp = pd.DataFrame(data)

        print(self.df_temp)

def help(_):
    print("You can't get help yet")

def init(_):
    print("Initializing")

def run(_):
    print("running masterpiece")

def version(_):
    print("version")

def check_dependencies(_):
    print("Checking dependencies")


command_lookup = {
    "run": run,
    "init": init,
    "help": help,
    "-h": help,
    "--help": help,
    "-v": version,
    "--version": version,
    "--check-dependencies": check_dependencies
}


def main():
    args = sys.argv
    command_args = []
    if len(args) == 1:
        help()
        sys.exit()
    elif len(args) == 2:
        command = args[1]
    else:
        command = args[1]
        command_args = args[2:]

    try:
        try:
            command_lookup[command](command_args)
        except KeyboardInterrupt:
            print(); sys.exit()
    except KeyError:
        LOG.error(f"Unknown command \"{command}\"")



if __name__ == "__main__":
    #Main(args)
    main()

    
