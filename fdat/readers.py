"""
Author: Amund M. Raniseth
Date: 25.12.2021

Reads the varoius types of diffraction data
"""

import os 
from fdat.log import LOG
import numpy as np

def read(filename):
    _fn, ext = os.path.splitext(filename)
    if ext == ".xye":
        xye_t = read_xye(filename)
    elif ext == ".brml":
        xye_t = read_brml(filename)
    return xye_t
        

def read_xye(filename):
    try:
        with open(filename, 'r') as f:
            raw = f.readlines()
    except Exception as e:
        LOG.warning("Error occurred while opening the file {}: {}".format(filename, e))


    
    xye = np.zeros((len(raw),3)) # creates 3dim numpy array with x(2theta), y(intensity) and e(error)
        
    for i,line in enumerate(raw):
        xye[i] = np.array(list(map(float, line.split())))

    # Transpose array is easier to plot
    xye_t = np.transpose(xye)

    return xye_t



"""
Made by Rasmus Vester Thøgersen, NAFUMA, Dept. of Chemistry, University of Oslo 2021
Modified by Amund Raniseth 25.12.2021
"""
def read_brml(filename):
    
    import pandas as pd
    import zipfile
    import xml.etree.ElementTree as ET
    import shutil

    if not os.path.isdir("./temp"):
        os.mkdir("./temp")

    # Extract the RawData0.xml file from the brml-file
    with zipfile.ZipFile(filename, 'r') as brml:
        for info in brml.infolist():
            if "RawData" in info.filename:
                brml.extract(info.filename, "./temp")



    # Parse the RawData0.xml file
    path = os.path.join("./temp", 'Experiment0/RawData0.xml')

    tree = ET.parse(path)
    root = tree.getroot()

    shutil.rmtree("./temp")

    diffractogram = []

    for chain in root.findall('./DataRoutes/DataRoute'):

        for scantype in chain.findall('ScanInformation/ScanMode'):
            if scantype.text == 'StillScan':

                if chain.get('Description') == 'Originally measured data.':
                    for data in chain.findall('Datum'):
                        data = data.text.split(',')
                        data = [float(i) for i in data]
                        twotheta, intensity = float(data[2]), float(data[3])

        
            else:
                if chain.get('Description') == 'Originally measured data.':
                    for data in chain.findall('Datum'):
                        data = data.text.split(',')
                        twotheta, intensity = float(data[2]), float(data[3])
                        
                        if twotheta > 0:
                            diffractogram.append({'2th': twotheta, 'I': intensity})

    diffractogram = pd.DataFrame(diffractogram)
    print(diffractogram.head)

    xye = np.zeros((len(10),3))
    xye_t = np.transpose(xye)
    return diffractogram