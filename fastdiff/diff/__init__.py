"""diff class contains data and functions for handling single diffractograms"""

import os
from log import LOG
import numpy as np
import pandas as pd
import scipy
import sys
import settings

class diff():
    """Diffractogram class. Instantiates object from filename.
    Functions:
    """

    def __init__(self, filepath):
        """Initializes diff object by reading in data and creating data arrays."""
        LOG.debug('Initializing diff object {}'.format(filepath))

        self.name = os.path.basename(filepath)
        self.wavelength = settings.WAVELENGTH # TODO replace this with reader for capturing this data

        # Open file
        try:
            with open(filepath, 'r') as f:
                self.raw = f.readlines()

            # Interpret data
            self._create_arrays()

        except Exception as e:
            LOG.warning("Could not load datafile '{}'. Error: {}".format(filepath, e))


    def _create_arrays(self):
        """Takes self.raw and creates a self.xye containing a numpy array with the data"""
        
        self.xye = np.zeros((len(self.raw),3)) # creates 3dim numpy array with x(2theta), y(intensity) and e(error)
        
        for i,line in enumerate(self.raw): #This takes time
            self.xye[i] = np.array(list(map(float, line.split())))

        # Transpose array is easier to plot
        self.xye = np.transpose(self.xye)


    def __repr__(self) -> str:
        return "diff Object: {}".format(self.name)

    def __str__(self) -> str:
        return "diff Object: {}".format(self.name)


    def get_pt_info(self, **kwargs):
        """Runs find_peakpos and gets data from an internal Pt standard."""
        self.PtCalibInfo = self.find_peakpos()
        wanted_info = {}

        def _check_kwargs(kwarg, kwargs):
            if kwarg in kwargs:
                if kwargs[kwarg]:
                    return True
            else:
                return False


        if _check_kwargs("Temp", kwargs):
            wanted_info["Temp"] = self.PtCalibInfo["Calc_Temp"]
        if _check_kwargs("lpa", kwargs):
            wanted_info["pt_lpa"] = self.PtCalibInfo["a"]

        return wanted_info

    def find_peakpos(self):
        """Takes a file and finds the lattice parameter, std dev and beamline temp and returns it as a pd Series"""

        #Get beamline temp from filename
        try:
            fn = self.name.split("_t")[-1]
            bl_temp = int(fn[:3])
        except Exception as e:
            LOG.debug("The file {} did not have a recognizable temperature in its filename.".format(self.name))
            bl_temp = 0

        a_lst = []
        a_curve_lst = []
        curve_lst = []
        peak_info = []

        ## Scan the intervals for the twotheta value with maximum intensity
        for peak in PEAK_INTERVALS:
            # First find indexes which match the scannable area
            index1 = (np.abs(self.xye_t[0]-peak[0])).argmin()
            index2 = (np.abs(self.xye_t[0]-peak[1])).argmin()
            # Then find the index for the maximum intensity value
            index_max = index1 + np.argmax(self.xye_t[1][index1:index2])
            # Get 2Theta at this index
            twotheta = self.xye_t[0][index_max]
            # Calculate d_spacing
            d = d_spacing(twotheta)
            # Calculate lattice constant alpha
            a = lattice_const(d, peak[2])
            a_lst.append(a)

            xcurve, ycurve, twoth_max = curve_fit(self.xye_t[0][index_max-2:index_max+3], self.xye_t[1][index_max-2:index_max+3])
            curve_lst.append((xcurve, ycurve))
            # Calculate d_spacing
            d_curve = d_spacing(twoth_max)
            # Calculate lattice constant alpha
            a_curve = lattice_const(d_curve, peak[2])
            a_curve_lst.append(a_curve)
            #peak_info.append(peak[2], twotheta, d, a)
            #LOG.debug("{} Peak Max found on 2Theta {:.4f}. d-spacing: {:.4f} Å, lattice param: {:.4f} Å".format(peak[2], twotheta, d, a))

        avg_a = sum(a_lst)/len(a_lst)
        std_a = np.std(a_lst)

        avg_a_curve = sum(a_curve_lst)/len(a_curve_lst)
        std_a_curve = np.std(a_curve_lst)
        file_info = {   "a": avg_a_curve, 
                        "std_a": std_a_curve, 
                        "Beamline_Temp": bl_temp, 
                        "Calc_Temp": tempfunc_platina(avg_a)
        }

        #plot_xrd(x, intensity, curve_lst)

        return file_info