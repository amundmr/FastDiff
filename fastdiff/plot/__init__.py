"""Plot contains all plotting features needed"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from datetime import date
from math import sqrt

from numpy.lib.function_base import _diff_dispatcher
import plot.utils as utils
import plot.conversion as convert
import materials.materials as materials
from log import LOG

def plot(diffObjects, **kwargs):
    fig = plt.figure(figsize=(10,5)) #, tight_layout=True
    fig.suptitle(str(date.today()))

    if 'zoom' in kwargs:
        n_zooms = len(kwargs['zoom'])
        gs = gridspec.GridSpec(2,n_zooms)
        ax = fig.add_subplot(gs[1,:])
        ax.set(
        ylabel = r'Square rooted Intensity [\sqrt{counts}]',
        xlabel = r'TwoTheta [$2\theta$], WL=1.54060'
        )
        
        for i,zoom in enumerate(kwargs['zoom']):
            zoomax = fig.add_subplot(gs[0,i])
            zoomax.set_xlim(zoom)
            #utils.zoom_effect01(zoomax, ax, zoom[0], zoom[1])
            utils.zoom_effect00(zoomax, ax )

    else:
        ax = plt.subplot()

        
    axs = fig.get_axes()

    if 'ticks' in kwargs:
        mats = []
        for mat in kwargs['ticks']: #loop materials in the ticks thing
            if "Fd3m" in mat:
                mats.append(materials.LMNOFd3m)
            elif "SRM" in mat or "Si" in mat:
                mats.append(materials.SRM640d)
        for mat in mats:
            for i in range(len(mat.two_thetas)):
                if i == 0:
                    axs[0].scatter(mat.two_thetas[i], -2, label = mat.label, color = mat.color, marker = "|")
                    axs[0].scatter(mat.two_thetas[i], -4.5, color = mat.color, marker = mat.hkls[i], s=200)
                else:
                    axs[0].scatter(mat.two_thetas[i], -2, color = mat.color, marker = "|")
                    axs[0].scatter(mat.two_thetas[i], -4.5, color = mat.color, marker = mat.hkls[i], s=200)



    for ax in axs:
        ax.tick_params(direction='in', top = 'true', right = 'true')
        for diffObj in diffObjects:
            labelname = diffObj.name
            dat = diffObj.xye

            if 'd_spacing' in kwargs:
                if kwargs['d_spacing'] == True:
                    dat[0] = convert.twotheta2d(dat[0])

            ax.plot(dat[0], dat[1], label = labelname)

    if 'xlim' in kwargs:
        axs[0].set_xlim(kwargs['xlim'])

    if 'd_spacing' in kwargs:
        if kwargs['d_spacing'] == True:
            
            """
            secaxs = []
            for ax in axs:
                secaxs.append(ax.secondary_xaxis('top', functions=(twotheta2d, d2twotheta)))
            """


    axs[0].legend()
    LOG.debug("Showing plot")
    plt.show()
    plt.savefig("PLOT.png")