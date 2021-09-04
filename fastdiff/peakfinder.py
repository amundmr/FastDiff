# Finds Platinum D-spacing based on the top of peaks 111, 200 and 400 (with WL=0.62231A: 15.5-16(1 1 1), 17.8 - 18.3(2 0 0), 36.5-37(4 0 0)
# USAGE: intensityratiofinder.py ./testdata

import numpy as np
import pandas as pd
import os
import sys

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

def read(folder):   #This func finds all files in the input folder and puts them in a list

    dir_files = []
    for (dirpath, dirnames, filenames) in os.walk(folder):
        dir_files.extend(filenames)
        

    filenames = []
    for file in dir_files:
        if file.split(".")[-1] == "xye":
            filenames.append(file)
		
    #Tell the user about the files found
    print("the read() command found the following files in the specified folder: ")
    print(filenames)
    return filenames


def find_peakpos(dirname,filename, df):
    """Takes a file and finds the lattice parameter, std dev and beamline temp and returns it as a pd Series"""
    ## First open, read and close file
    filename = os.path.abspath(dirname + "/" + filename)    #Make the path absolute, just in case. Cross platform compatible
    f = open(filename, 'r')                 #Open file
    f.readline()                            #Read two first line in case there is explanatory text, dont need these datapoints anyways
    f.readline()
    data = f.readlines()                    #Put the rest of the data in data as list
    f.close()

    #Get beamline temp from filename
    fn = os.path.basename(filename).split("_t")[-1]
    bl_temp = int(fn[:3])

    ## Accumulate data as floats in array
    x = np.zeros(len(data))
    intensity = np.zeros(len(data))
    for i, line in enumerate(data):
        #print(line)
        split = line.split()
        x[i] = eval(split[0])
        intensity[i] = eval(split[1])

    

    #plot_xrd(x, intensity)
    
    a_lst = []
    a_curve_lst = []
    curve_lst = []
    peak_info = []
    ## Scan the intervals for the twotheta value with maximum intensity
    for peak in PEAK_INTERVALS:
        # First find indexes which match the scannable area
        index1 = np.where(x == (min(x, key=lambda y:abs(y-peak[0]))))[0][0]
        index2 = np.where(x == (min(x, key=lambda y:abs(y-peak[1]))))[0][0]
        # Then find the index for the maximum intensity value
        index_max = index1 + np.argmax(intensity[index1:index2])
        # Get 2Theta at this index
        twotheta = x[index_max]
        # Calculate d_spacing
        d = d_spacing(twotheta)
        # Calculate lattice constant alpha
        a = lattice_const(d, peak[2])
        a_lst.append(a)

        xcurve, ycurve, twoth_max = curve_fit(x[index_max-2:index_max+3], intensity[index_max-2:index_max+3])
        curve_lst.append((xcurve, ycurve))
        # Calculate d_spacing
        d_curve = d_spacing(twoth_max)
        # Calculate lattice constant alpha
        a_curve = lattice_const(d_curve, peak[2])
        a_curve_lst.append(a_curve)
        #peak_info.append(peak[2], twotheta, d, a)
        #print("{} Peak Max found on 2Theta {:.4f}. d-spacing: {:.4f} Å, lattice param: {:.4f} Å".format(peak[2], twotheta, d, a))

    avg_a = sum(a_lst)/len(a_lst)
    std_a = np.std(a_lst)

    avg_a_curve = sum(a_curve_lst)/len(a_curve_lst)
    std_a_curve = np.std(a_curve_lst)
    file_info = [os.path.basename(filename), avg_a, std_a, bl_temp, avg_a_curve, std_a_curve, tempfunc_platina(avg_a)]

    #plot_xrd(x, intensity, curve_lst)

    return pd.Series(file_info, index = df.columns)



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


def plot_xrd(x,intensity, curvefit = None):
    """This func can be used within the find_peakpos func in order to plot XRDiffractograms"""

    import matplotlib.pyplot as plt
    plt.plot(x,intensity)

    for peak in PEAK_INTERVALS:
        plt.axvline(peak[0])
        plt.axvline(peak[1])

    if curvefit:
        for curve in curvefit:
            plt.plot(curve[0], curve[1])

    plt.show()

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
    return f(lpa)

# Running this script
def run_all(list_of_filenames, df):
    pdseries = find_peakpos(datafolder, list_of_filenames[0], df)
    for file in list_of_filenames:
        pdseries = find_peakpos(datafolder, file, df)
        df = df.append(pdseries, ignore_index=True)

    import matplotlib.pyplot as plt
    #plt.scatter(df["Beamline temp"], df["Lattice param Å"])
    plt.errorbar(df["Beamline temp"], df["Lattice param Å"], yerr=df["Lattice param std dev"], fmt='o')
    plt.errorbar(df["Beamline temp"], df["a curve"], yerr=df["a stdev curve"], fmt='o')
    plt.show()
    #df.plot(x="Beamline temp", y="Lattice param Å")
    print(df)

def run_first(list_of_filenames, df):
    pdseries = find_peakpos(datafolder, list_of_filenames[0], df)


if __name__ == "__main__":                          #Only run if main app
    datafolder = sys.argv[1]                        #Pull folder from CLI
    list_of_filenames = read(datafolder)            #Get all filenames in folder

    # Create the pandas DataFrame
    df = pd.DataFrame(columns = ['Filename', "Lattice param Å", "Lattice param std dev", "Beamline temp", "a curve", "a stdev curve", "calc temp"]) #'111Peak_2T deg', '200Peak_2T deg', '400Peak_2T deg', 'd-spacing Å', 'lattice-param Å'
    

    run_all(list_of_filenames, df)
    #run_first(list_of_filenames, df)


    


