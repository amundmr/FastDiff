"""Main, this is ran when the user calls fastdiff."""


from fdat.log import LOG


def help(*args):
    help_string = """
    Commands:
        run <folder>    Runs fastdiff with the configuration in the specified folder.
        init <folder>   Initializes working directory in the specified folder
        help, -h        Shows this help screen
        -v, --version   Shows the version number
        --check-deps    Checks to see if all dependencies are correctly installed."""
    LOG.info(help_string)


def init(args):
    """Initializes working directory for fastdiff"""

    import sys
    import os
    import toml
    import shutil

    def _make_workdir(dir, filepaths):
        # Make config templates
        
        try:
            workdir = os.path.join(dir, 'workdir')
            os.mkdir(workdir)
            # Make user folders
            os.mkdir(os.path.join(workdir, "CIF"))
            os.mkdir(os.path.join(workdir, "data"))

            #Write plot.toml file
            with open(os.path.join(workdir,'plot.toml'), 'w') as f:
                toml.dump(plot_kwargs, f)

            #Insert filepaths in analysis kwargs
            basenames_in_datafolder = []
            for filepath in filepaths:
                basenames_in_datafolder.append(os.path.join("data", os.path.basename(filepath)))
            analysis_kwargs["files"] = basenames_in_datafolder

            #Write config.toml file
            with open(os.path.join(workdir,'config.toml'), 'w') as f:
                toml.dump(analysis_kwargs, f)

        except Exception as e:
            LOG.error("Could not create new working directory '{}'. Error message: {}".format(workdir, e))
            sys.exit()

        if filepaths: #Then we'll copy them to the data dir, totally shamelessly
            for filepath in filepaths:
                destination = os.path.join(workdir, 'data', os.path.basename(filepath))
                shutil.copyfile(filepath, destination)

    def scan_path(path):
        """Scans the path inserted for supported filetypes and returns as list"""
        
        # Supported file formats (extensions:)
        supp_exts = ["xye", "brml"]

        filepaths = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            for file in filenames:
                _fn, ext = os.path.splitext(file)
                if ext in supp_exts:
                    filepaths.append(os.path.join(dirpath, file))
                    
        filepaths.sort(key=lambda x: os.path.basename(x))

        #Tell the user about the files found
        LOG.success("the scan_path() command found the following files in the specified folder:", lst = filepaths)
        return filepaths

    def _handle_path(dir):
        filepaths = None
        if os.path.isdir(args[0]):
            #LOG.warning("Folder '{}' already exist. Would you like to overwrite it? [Y/n]".format(args[0]))
            LOG.warning("Folder '{}' already exist. Would you like to scan for data in it and create a 'workdir' folder in it with eventual data? [Y/n]".format(args[0]))
            answer = input()

            if answer in ["", "Y", "y", "Yes", "yes"]:
                """LOG.warning("This will delete everything in that folder!! Are you sure you want to continue? [Y/n]")
                answer2 = input()

                if answer2 in ["", "Y", "y", "Yes", "yes"]:
                    try:
                        shutil.rmtree(args[0])
                    except PermissionError as e:
                        LOG.error("You do not have permission to remove the old directory! Error message: {}. Exiting.".format(e))
                        sys.exit()

                else:
                    LOG.warning("You chose not to delete the old directory. Exiting.")
                    sys.exit()"""
                filepaths = scan_path(args[0])


            else:
                #LOG.warning("You chose not to delete the old directory. Exiting.")
                LOG.warning("You chose not to continue. Exiting.")
                sys.exit()

        return filepaths

    if not args:
        LOG.error("You MUST choose a working directory by typing 'fastdiff init <dirname>'.")
        sys.exit()

    filepaths = _handle_path(args[0])
    _make_workdir(args[0], filepaths)
    LOG.success("Created working directory in folder '{}'.".format(args[0]))

    LOG.debug("Initializing new work environment")


def run(args):

    # Load configuration
    config, workdir = load_config(args)

    # Set debugging mode asap
    if config["debugging-mode"]:
            LOG.set_level("DEBUG")
            LOG.debug("Debug mode active")

    # Initialize total data object
    from fdat.data import Data
    data = Data(workdir,config)
    data.load_data()

    # Act on configuration

    if config["plot"]:
        data.plot()
    
    if config["operando"]:
        data.get_electrochemistry()

    if config["convert-to-dspacing"]:
        LOG.warning("d-spacing conversion not implemented.")

    if config["temp-from-internal-standard"]:
        data.calc_temps()
        LOG.warning("Temperature analysis from internal standard not implemented.")

    if config["calibrate-with-internal-standard"]:
        LOG.warning("internal standard 2theta calibration not implemented.")

    if type(config["internal-standard"]) is str:
        LOG.warning("Internal standard in itself not implemented.")

    if config["plot"]:
        LOG.debug("Running data.plot()")
        data.plot()


def load_config(args):
    import os
    import sys

    ## Create path
    if args[0]:
        workdir = args[0]
        cfgpath = os.path.join(workdir, "config.toml")
    else:
        workdir = "./"
        cfgpath = "./config.toml"
    
    ## Check that it exists
    if not os.path.isfile(cfgpath):
        LOG.error("Cannot find '{}'. Did you initialize a working directory?".format(cfgpath))
        sys.exit()
    else:
        # File exists! Time to load config!
        import toml
        try:
            with open(cfgpath, 'r') as f:
                config = toml.load(f)
        except Exception as e:
            LOG.error("Could not read configuration file '{}'. Error message: \n{}".format(cfgpath, e))
            sys.exit()

        LOG.debug("Found and loaded config file '{}'.".format(cfgpath))
    
    return config, workdir


def version(_):
    LOG.info("Shit! I forgot to make this function! Please ask me to implement it asap :)")


def check_dependencies(_):
    imports = ["os", "sys", "numpy", "pandas", "toml", "PyCifRW"]
    modules = []
    missing_packages = []
    for x in imports:
        try:
            modules.append(__import__(x))
            LOG.debug("Found package: {}".format(x))
        except ImportError:
            LOG.debug("Error importing {}.".format(x))
            missing_packages.append(x)

    
    if len(missing_packages) > 0:
        LOG.error("Could not find the following packages: {}".format(missing_packages))
    else:
        LOG.success("All packages are successfully installed!")


def main():
    """Main function, takes user args and runs eventual commands"""
    import sys
    args = sys.argv
    command_args = None
    if len(args) == 1:
        help()
        sys.exit()
    elif len(args) == 2:
        command = args[1]
        command_args = []
    else:
        command = args[1]
        command_args = args[2:]

    if not command in command_lookup:
        LOG.error(f"Unknown command \"{command}\"")
    
    command_lookup[command](command_args)
        

command_lookup = {
    "run": run,
    "init": init,
    "help": help,
    "-h": help,
    "--help": help,
    "-v": version,
    "--version": version,
    "--check-deps": check_dependencies
}

analysis_kwargs = {
    "files" : ["file.xy", "file1.xye"],
    "convert-to-dspacing" : False,
    "temp-from-internal-standard": False,
    "calibrate-with-internal-standard": False,
    "internal-standard" : "Pt",
    "debugging-mode": False,
    "plot": True,
    "operando" : True,
    "elchemfile" : "operando.mpt",
}

plot_kwargs = {
    "zoom" : [(18.0,19.5), (35.0,40.0)],
    "xlim" : (15, 70),
    "ticks" : ['SRM', 'Fd3m'],
    "d_spacing" : False,
    "savepath": "NOT IMPLEMENTED YET",
}


if __name__ == "__main__":
    main()

    
