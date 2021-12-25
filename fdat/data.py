"""Contains main data class"""

from __main__ import LOG


class Data():
    """Main data class"""
    
    def __init__(self, workdir, config):
        """Initialize main data object"""
        import os


        LOG.debug("Initializing main data object")
        self.cfg = config
        self.workdir = workdir

        # Initialize list of diff objects
        self.diffs = []

        # Initialize a list of CIF objects
        self.cifs = []

        # Scan datafolder
        self.filenames = [os.path.join(workdir, x) for x in self.cfg["files"]]
        files_in_datafolder = self.scan_path(os.path.join(workdir, "data"))
        if len(files_in_datafolder) > len(self.filenames):
            LOG.debug("There are {} files in the datafolder, while the user only chose to use {} files in the config.toml".format(len(files_in_datafolder), len(self.filenames)))

        # Scan CIF folder
        self.cifnames = self.scan_path(os.path.join(workdir, "CIF"))


    def scan_path(self, path):
        """Scans the path inserted for supported filetypes and returns as list"""
        import os

        filepaths = []
        last_path_folder = os.path.basename(os.path.normpath(path))
        if last_path_folder == "data":
            identifier = "xye"
        elif last_path_folder == "CIF":
            identifier = "cif"

        for (dirpath, dirnames, filenames) in os.walk(path):
            for file in filenames:
                if file.split(".")[-1] == identifier:
                    filepaths.append(os.path.join(dirpath, file))
                    
        filepaths.sort(key=lambda x: os.path.basename(x))
        #Tell the user about the files found
        LOG.debug("the scan_path() command found the following files in the {} folder:".format(last_path_folder), filenames)
        LOG.info("Found {} files in folder '{}'.".format(len(filepaths), path))

        return filepaths
        
    def load_data(self):
        import os
        from diff import diff

        for filename in self.filenames:
            self.diffs.append(diff(filename))

        if len(self.cifnames) > 0:
            import Dans_Diffraction as dif
            for cifname in self.cifnames:
                crystal = dif.Crystal(cifname)
                LOG.debug("The cif file '{}' was read in successfully with DansDiffraction as: {}".format(cifname, crystal.cif["_chemical_formula_structural"]))
                self.cifs.append(crystal)

    def get_electrochemistry(self):
        

    def plot(self):
        import os
        import sys
        import toml
        import plot
        LOG.warning("Shit! I haven't implemented the data-class plot feature yet!")
        # Loading plot config
        try:
            with open(os.path.join(self.workdir, "plot.toml")) as f:
                self.plotcfg = toml.load(f,)
        except Exception as e:
            LOG.error("Could not read 'plot.toml'! Error message: {}".format(e))
            sys.exit()

        # Starting plot
        plot.plot(self, **self.plotcfg)
        #elif self.args.plot:
        #    plot.plot(self.diffs)
        #sys.exit()


    def calc_temps(self):

        import pandas as pd
        import numpy as np
        """Takes every diffractogram and runs get_pt_info on it. 
        Right now it only ask for the temperature calculated from 2nd degree polynomial peak fitting
        At the end it creates a dataframe with the filenames and temperature"""        

        found = False
        lpa = None
        for i,crystal in enumerate(self.cifs):
            #if self.cfg["internal-standard"] in crystal.cif["_chemical_formula_structural"] or self.cfg["internal-standard"] in crystal.cif["_chemical_name_common"]:
            found = True
            crystal.Scatter._powder_units = "Q"
            #self.standard_peaks = self._simulate_powder(crystal, energy_kev=8)

            #Gives np array with intensity over q-range of powder.
            self.standard_powder_pattern = crystal.Scatter.generate_powder()

            #Gives string with visible peaks: miller index, 2th and intensity
            self.standard_powder_peaks = crystal.Scatter.print_all_reflections()
            LOG.debug("Info on the internal standard chosen:\n{}".format(self.standard_powder_peaks))

            #Plan: Convert string to dataframe, pick out some peaks and choose these peaks to modulate and fit the temperature.

            self.standard_powder_peaks_df = pd.DataFrame(self.standard_powder_peaks, header=2, sep = " ")
            LOG.warning(self.standard_powder_peaks_df.head)

            LOG.debug("Using cif '{}' as internal standard.".format(self.cifnames[i]))
                #break

        if not found:
            LOG.error("You set '{}' as internal standard, but we can not find a cif file for it in the 'CIF' folder.".format(self.cfg["internal-standard"]))



        """data = []
        for diff in self.diffs:
            pt_info = diff.get_pt_info(Temp = True)
            pt_info["Filename"] = diff.name
            data.append(pt_info)

        self.df_temp = pd.DataFrame(data)

        print(self.df_temp)"""

    def _simulate_powder(self, crystal, energy_kev=None, peak_width=0.01, background=0, powder_average=True):
        from Dans_Diffraction import functions_crystallography as fc
        from Dans_Diffraction import functions_general as fg
        from Dans_Diffraction import functions_plotting as fp

        import numpy as np
        import matplotlib.pyplot as plt
        """
        This func was directly stolen from https://github.com/DanPorter/Dans_Diffraction/blob/v1.8.2/Dans_Diffraction/classes_plotting.py#L260
        All credits to Dan Porter
        Generates a powder pattern, plots in a new figure with labels
            see classes_scattering.generate_powder
        """

        if energy_kev is None:
            energy_kev = crystal.Scatter._energy_kev
        
        # Get reflections
        angle_max = crystal.Scatter._scattering_max_twotheta
        q_max = fc.calqmag(angle_max, energy_kev)
        HKL = crystal.Cell.all_hkl(energy_kev, angle_max)
        HKL = crystal.Cell.sort_hkl(HKL) # required for labels
        Qmag = crystal.Cell.Qmag(HKL)

        # Min angle
        angle_min = crystal.Scatter._scattering_min_twotheta
        if angle_min < 0.01: angle_min = 0.01
        q_min = fc.calqmag(angle_min, energy_kev)
        
        # Calculate intensities
        I = crystal.Scatter.intensity(HKL)

        if powder_average:
            # Apply powder averging correction, I0/|Q|**2
            I = I/(Qmag+0.001)**2
        
        # create plotting mesh
        pixels = 2000*q_max # reduce this to make convolution faster
        pixel_size = q_max/(1.0*pixels)
        peak_width_pixels = peak_width/(1.0*pixel_size)
        mesh = np.zeros([int(pixels)])

        if crystal.Scatter._powder_units.lower() in ['tth', 'angle', 'two-theta', 'twotheta', 'theta']:
            xx = crystal.Cell.tth(HKL, energy_kev)
            min_x = angle_min
            max_x = angle_max
            xlab = u'Two-Theta [Deg]'
        elif crystal.Scatter._powder_units.lower() in ['d', 'dspace', 'd-spacing', 'dspacing']:
            xx = crystal.Cell.dspace(HKL)
            min_x = fc.q2dspace(q_max)
            max_x = fc.q2dspace(q_min)
            if max_x > 10: max_x = 10.0
            xlab = u'd-spacing [\u00C5]'
        else:
            xx = Qmag
            min_x = q_min
            max_x = q_max
            xlab = u'Q [\u00C5$^{-1}]$'
        
        # add reflections to background
        # scipy.interpolate.griddata?
        mesh_x = np.linspace(0, max_x, np.int(pixels))
        pixel_coord = xx/ max_x
        pixel_coord = (pixel_coord*(pixels-1)).astype(int)

        ref_n = [0]
        ref_txt = ['']
        ext_n = []
        ext_txt = []
        for n in range(1, len(I)):
            if xx[n] > max_x or xx[n] < min_x:
                continue
            mesh[pixel_coord[n]] = mesh[pixel_coord[n]] + I[n]

            close_ref = np.abs(pixel_coord[n]-pixel_coord) < peak_width_pixels
            close_lab = np.all(np.abs(pixel_coord[n] - np.array(ref_n+ext_n)) > peak_width_pixels)
            
            if np.all(I[n] >= I[close_ref]) and close_lab:
                # generate label if not too close to another reflection
                if I[n] > 0.1:
                    ref_n += [pixel_coord[n]]
                    ref_txt += ['(%1.0f,%1.0f,%1.0f)' % (HKL[n,0],HKL[n,1],HKL[n,2])]
                else:
                    ext_n += [pixel_coord[n]]
                    ext_txt += ['(%1.0f,%1.0f,%1.0f)' % (HKL[n,0],HKL[n,1],HKL[n,2])]
        
        # Convolve with a gaussian (if >0 or not None)
        if peak_width:
            gauss_x = np.arange(-3*peak_width_pixels,3*peak_width_pixels+1) # gaussian width = 2*FWHM
            G = fg.gauss(gauss_x, None, height=1, cen=0, fwhm=peak_width_pixels, bkg=0)
            mesh = np.convolve(mesh,G, mode='same') 
        
        # Add background (if >0 or not None)
        if background:
            bkg = np.random.normal(background,np.sqrt(background), [int(pixels)])
            mesh = mesh+bkg
        
        # create figure
        """plt.figure(figsize=[2*10, 10], dpi=300)
        plt.plot(mesh_x, mesh, 'k-', lw=2)
        maxy = np.max(mesh)
        plt.ylim([background-(maxy*0.05), maxy*1.15])
        plt.xlim([min_x, max_x])
        
        # Reflection labels
        for n in range(len(ref_n)):
            plt.text(mesh_x[ref_n[n]], 1.01 * mesh[ref_n[n]], ref_txt[n],
                     fontname=fp.DEFAULT_FONT, fontsize=18, color='b',
                     rotation='vertical', ha='center', va='bottom')
        # Extinction labels
        ext_y = background + 0.01 * plt.ylim()[1]
        for n in range(len(ext_n)):
            plt.text(mesh_x[ext_n[n]], ext_y, ext_txt[n],
                     fontname=fp.DEFAULT_FONT, fontsize=18, color='r',
                     rotation='vertical', ha='center', va='bottom')
        
        # Plot labels
        ylab = u'Intensity [a. u.]'
        ttl = '%s\nE = %1.3f keV' % (crystal.name, energy_kev)
        fp.labels(ttl, xlab, ylab)"""
        
        return (mesh_x, mesh)
    