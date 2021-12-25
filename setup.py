import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name = 'fdat',
    packages = ['fdat'],
    include_package_data = True,
    version = '0.1.0',     # Remember to update on new version
    license='GNU General Public License v3.0',        
    description = 'Fast Diffraction Analysis Tool',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'Amund Raniseth',                   
    author_email = 'amund.raniseth@gmail.com',      
    url = 'https://github.com/amundmr/fdat',   
    download_url = 'https://github.com/amundmr/fdat/archive/refs/tags/v0.1.0.tar.gz',    # Remember to update this with new versions
    keywords = ['diffraction', 'plotter', 'reader', 'analysis', 'x-rays', 'x-ray pattern'],
    install_requires=[
            'matplotlib',
            'numpy',
            'pandas',
            'toml',
            'scipy',
            'PyCifRW',
            'ecdh',
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        "console_scripts": [
            "fdat=fdat.__main__:main",
        ]
    },
)