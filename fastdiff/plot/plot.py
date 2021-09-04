"""Plot contains all plotting features needed"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from datetime import date
from math import sqrt


def plot_xrd(files, **kwargs):
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
                mats.append(utils.LMNOFd3m)
            elif "SRM" in mat or "Si" in mat:
                mats.append(utils.SRM640d)
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
        for f in files:
            labelname = f[4:].strip("_exported.xy")
            dat = read_xrd(f)

            if 'd_spacing' in kwargs:
                if kwargs['d_spacing'] == True:
                    dat[0] = twotheta2d(dat[0])

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

    plt.show()

def twotheta2d(tth):
    th = tth/2
    d = 1.54060/(2*np.sin(th * np.pi / 180.))
    return d

def d2twotheta(d):
    th = np.arcsin(1.54060/(2*d)) /np.pi*180
    tth = 2*th
    return tth



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
#
    plot_xrd(files, xlim = xlim, ticks = ticks, zoom = zoom)