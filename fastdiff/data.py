"""Contains main data class"""

from log import LOG

class Data():
    """Main data class"""

    def __init__(self, workdir, config):
        """Initialize main data object"""
        import os
        import sys
        import toml


        LOG.debug("Initializing main data object")
        self.cfg = config
        self.workdir = workdir

        # Initialize list of diff objects
        self.diffs = []

        # Scan datafolder
        self.filenames = self.scan_path(os.path.join(workdir, "/data/"))


    def scan_path(self, path):
        """Scans the path inserted for supported filetypes and returns as list"""
        import os

        dir_files = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            dir_files.extend(filenames)
            

        filenames = []
        for file in dir_files:
            if file.split(".")[-1] == "xye":
                filenames.append(file)
            
        #Tell the user about the files found
        LOG.debug("the scan_path() command found the following files in the specified folder: {}".format(filenames))
        LOG.info("Found {} files in folder '{}'.".format(len(filenames), path))

        return filenames
        

    def plot(self):
        LOG.warning("Shit! I haven't implemented the data-class plot feature yet!")
        # Loading plot config
        #with open(os.path.join(self.workdir, "plot.toml")) as f:
        #    self.plotcfg = toml.load(f,)

        # Starting plot
        #plot.plot(self.diffs, **self.plotkwargs)
        #elif self.args.plot:
        #    plot.plot(self.diffs)
        #sys.exit()


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