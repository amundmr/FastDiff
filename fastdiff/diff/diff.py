"""The diff module contains everything on single diffractograms."""
import os
import logging
import numpy as np
import sys

class diff():
    """Diffractogram class. Instantiates object from filename.
    Functions:
    """
    def __init__(self, filename):

        # Open file
        try:
            with open(filename, 'r') as f:
                self.raw = f.readlines()
        except Exception as e:
            logging.exception("Error occurred while opening the file {}".format(filename))

        # Interpret data
        self._create_arrays()


    def _create_arrays(self):
        """Takes self.raw and creates a self.xye containing a numpy array with the data"""
        
        self.xye = np.zeros((len(self.raw),3)) # creates 3dim numpy array with x(2theta), y(intensity) and e(error)
        
        for i,line in enumerate(self.raw):
            self.xye[i] = np.array(list(map(float, line.split())))

        # Transpose array is easier to plot
        self.xye_t = np.transpose(self.xye)
        print(self.xye_t)


if __name__ == "__main__":
    filename = sys.argv[1]
    diff = diff(filename)
