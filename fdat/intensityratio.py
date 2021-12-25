# Finds Platinum D-spacing based on the top of peaks 111, 200 and 400 (with WL=0.62231Å: 15.5-16(1 1 1), 17.8 - 18.3(2 0 0), 36.5-37(4 0 0)

# USAGE: intensityratiofinder.py ./testdata

from numpy import trapz
import os
import sys
from fdat.log import LOG

def read(folder):   #This func finds all files in the input folder and puts them in a list

    dir_files = []
    for (dirpath, dirnames, filenames) in os.walk(folder):
        dir_files.extend(filenames)
        break

	filenames = []
	for file in dir_files:
		if file.split(".")[-1] == "cbf":
		filenames.append(file)
		
    #Tell the user about the files found
    print("the read() command found the following files in the specified folder: ")
    print(filenames)
    return filenames

def findIntensityRatio(filename):
    filename = os.path.abspath(filename)    #Make the path absolute, just in case. Cross platform compatible
    f = open(filename, 'r')                 #Open file
    f.readline()                            #Read two first line in case there is explanatory text, dont need these datapoints anyways
    f.readline()
    data = f.readlines()                    #Put the rest of the data in data as list
    f.close()

    #Defining peaks data
    Data311 = []
    Data400 = []
    i=-1
    for line in data:
        i+=1
        x = float(line.split()[0])
        y = float(line.split()[1])
        if x > 36 and x < 37:
            Data311.append(y)
        if x > 44 and x < 45:
            Data400.append(y)
   
    #Finding max peak intensity and creating ratio
    intensityratio = max(Data311)/max(Data400)

    #Finding area of peak ratio
    dx = float(data[1].split()[0]) - float(data[0].split()[0])
    area311 = float(trapz(Data311, dx=dx))
    area400 = float(trapz(Data400, dx=dx))
    arearatio = area311/area400


    return intensityratio, arearatio

# Running this script
if __name__ == "__main__":                          #Only run if main app
    datafolder = sys.argv[1]                        #Pull folder from CLI
    list_of_filenames = read(datafolder)            #Get all filenames in folder
    #datfile = str(datafolder+list_of_filenames[0])  #Get path relative to script folder
    #print("Filename \t\t\tMax intensity ratio \tPeak area ratio")
    #Loop over all files
    #for f in list_of_filenames:
    #    filepath = str(datafolder + f)
    #    inten, area = findIntensityRatio(filepath)
    #    print(f + "\t" + str(inten) + "\t" + str(area))

