"""The diff module contains everything on single diffractograms."""

import os
import numpy as np
import pandas as pd
from log import LOG
import scipy
import sys
import settings



## Definition of peak intervals with Miller indices
PEAK_INTERVALS = [  (15.5, 16, (1,1,1)),     # 111 plane distance peak
                    (17.8, 18.3, (2,0,0)),   # 200 plane distance peak
                    (36.5, 37, (4,0,0))]     # 400 plane distance peak

#temp (K) and lp_a (nm) from https://www.technology.matthey.com/article/41/1/12-21/
PLATINA_TEMP = [
[0, 10, 20, 30,40,50,60,70,80,90,100,110,120,130,140,150,160,180,200,220,240,260,280,293.15,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2041.3],
[0.39160,0.39160,0.39160,0.39161,0.39161,0.39163,0.39164,0.39166,0.39168,0.39171,0.39173,0.39176,0.39179,0.39182,0.39185,0.39188,0.39191,0.39198,0.39204,0.39211,0.39218,0.39224,0.39231,0.39236,0.39238,0.39274,0.39311,0.39349,0.39387,0.39427,0.39468,0.39510,0.39553,0.39597,0.39643,0.39691,0.39740,0.39790,0.39842,0.39896,0.39953,0.40013,0.40039]
]
PLATINA_TEMP[1] = [x * 10 for x in PLATINA_TEMP[1]]




class diff():
    """Diffractogram class. Instantiates object from filename.
    Functions:
    """

    def __init__(self, filename):
        
        LOG.debug('Initializing diff object {}'.format(filename))

        self.name = os.path.basename(filename)
        self.wavelength = 0.6 # TODO replace this with reader for capturing this data

        # Open file
        try:
            with open(filename, 'r') as f:
                self.raw = f.readlines()

            # Interpret data
            self._create_arrays()

        except Exception as e:
            LOG.warning("Error occurred while opening the file {}: {}".format(filename, e))


    def _create_arrays(self):
        """Takes self.raw and creates a self.xye containing a numpy array with the data"""
    
        self.xye = np.zeros((len(self.raw),3)) # creates 3dim numpy array with x(2theta), y(intensity) and e(error)
        
        for i,line in enumerate(self.raw):
            self.xye[i] = np.array(list(map(float, line.split())))

        # Transpose array is easier to plot
        self.xye_t = np.transpose(self.xye)
        LOG.debug("Data array: {}".format(self.xye_t))

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


def d_spacing(twotheta):
    """Takes twotheta in degrees, returns d spacing"""
    wl = 0.62231 # wavelength in Angstrom
    n = 1 # order of reflection

    theta_radians = (twotheta/2)*(np.pi/180)

    d = n*wl/(2*np.sin(theta_radians))

    return d

def lattice_const(d, hkl):
    """Takes d spacing and miller indices, returns lattice parameter alpha assuming a cubic structure"""
    h = hkl[0]
    k = hkl[1]
    l = hkl[2]

    a = d * np.sqrt(h*h + k*k + l*l)
    return a


def curve_fit(twoth, intens):
    """Takes a list of 5 datapoints and fits a 2nd degree polynomial peak to it, which is returned with 100 datapoints"""
    from scipy.optimize import curve_fit
    import matplotlib.pyplot as plt
    def _quadratic_function(x,a,b,c):
        return a*x*x + b*x + c
    
    pars, cov = curve_fit(f=_quadratic_function, xdata = twoth, ydata = intens)

    xvals = np.linspace(min(twoth), max(twoth), 100)
    yvals = _quadratic_function(xvals, *pars)

    twoth_max = xvals[np.argmax(yvals)]

    return xvals, yvals, twoth_max

def tempfunc_platina(lpa):
    """ Takes lattice parameter and returns temperature based on the hardcoded PLATINA_TEMP data"""

    from scipy.interpolate import interp1d
    # Do zero-smoothing interpolation
    f = interp1d(PLATINA_TEMP[1], PLATINA_TEMP[0])
    
    #import matplotlib.pyplot as plt
    #plt.plot(PLATINA_TEMP[1], PLATINA_TEMP[0])
    #plt.scatter(0.395, f(0.395))
    #plt.plot(PLATINA_TEMP[1],f(PLATINA_TEMP[1]))
    #plt.show()
    return float(f(lpa))


if __name__ == "__main__":
    filename = sys.argv[1]
    diff = diff(filename)
