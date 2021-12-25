"""All conversion functions needed"""
import numpy as np
from fdat.log import LOG

def twotheta2d(tth):
    th = tth/2
    d = 1.54060/(2*np.sin(th * np.pi / 180.))
    return d

def d2twotheta(d):
    th = np.arcsin(1.54060/(2*d)) /np.pi*180
    tth = 2*th
    return tth


"""
if __name__ == "__main__":
    #read_xrd("AMR_6_LNMO_exported.xy")
    files = [   
                #"xy/AMR_6_LNMO_exported.xy",
                #"xy/AMR_7_LNA05MO_exported.xy",
                #"xy/AMR_8_LA05NMO_exported.xy",
                #"xy/AMR_9_A05LNMO_exported.xy",
                #"xy/AMR_10_LNA1MO_exported.xy",
                #"xy/AMR_11_LA1NMO_exported.xy",
                #"xy/AMR_12_A1LNMO_exported.xy",
                "xy/AMR_13_LNA2MO_exported.xy",
                "xy/AMR_14_LA2NMO_exported.xy",
                "xy/AMR_15_A2LNMO_exported.xy",
            ]
    zoom = [(18,19.5), (35,40)]
    xlim = (15, 70)
    ticks = ['SRM', 'Fd3m']
    d_spacing = True

    plot(files, xlim = xlim, ticks = ticks, zoom = zoom)"""