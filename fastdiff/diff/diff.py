"""The diff module contains everything on single diffractograms."""

import os
from log import LOG
import numpy as np
import pandas as pd
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
