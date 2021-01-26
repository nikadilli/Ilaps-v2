[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 


# Ilaps-v2
**python data reduction and imaging application for LA-ICP-MS**

## About Ilaps
LA-ICP-MS is an extremely powerful analytical technique for spatially resolved analysis of solid samples. It produces complex, time-dependent signals which require different approach than signals produced by solution sample introduction. 

Ilaps (**I**maging of **L**aser **a**blation **p**lasma **s**pectrometry) is a python based software tool specifically developed for data procesing of laser ablation inductively coupled plasma mass spectrometry (LA-ICP-MS). So far it is possible to directly import data in different formats (.csv, .xlsx, .asc) from Agilent and Element2 instruments, however as an open source software it is simple to add protocols for other formats or instruments, if necessary. ILAPS offers **bulk analysis** as well as **elemental imaging** from a continuous time dependant data acquired in a single file. This is where ILAPS differs from most of the other accesible softwares, it uses .iolite file from Laser Ablation system to find start of each ablation and automatically segments the datastream into sections of signal and background.

ILAPS also contains background correction as well as internal standard normalisation and total sum normalisation. Data can be visualised in different colormaps. Semi-interactive graph embeded directly in the user interface ensures proper controll over the final appearance of the output image. Moreover, it is possible to scale, smooth, interpolate and quantify the data with instant response in the image. 

Even though ILAPS is optimised for LA-ICP-MS, it can easily handle data from other instruments, such as laser induced breakdown spectroscopy (LIBS), just by a simple conversion of raw data to fit the importing format. This allows an easy comparison of elemental imaging by different methods.

## Version 2
Ilaps-v2 uses python package [imgMS](https://github.com/nikadilli/imgMS) for all data reduction tasks and imaging. The documentation of all functions can be found at [ReadTheDocs](https://imgms.readthedocs.io/en/latest/). 

## Run from code 
To run the application, all necessary dependences must be installed. Ilaps is a python desktop aplication, therefore it is necessary to install python and required libraries before the first time the app is started.

1. Python 3 is necessary to run the code. Download [here](https://www.python.org/downloads/) and follow the instalation.
2. Dowload or clone this repository.
3. Open terminal/cmd and navigate to the Ilaps folder.
  * `cd path/to/folder/Ilaps`
4. Create virtual enviroment. 
  * `python -m venv venvname`
5. Activate virtual enviroment. 
  * Windows `call venvname/Scripts/activate.bat`
  * Linux/Mac `source venvname/bin/activate`
6. Instal python libraries required for Ilaps.
  * `pip install -r requirements.txt`
7. Run Ilaps from python.
  * `python GUI.py`

If everything is already installed, follow only steps 3., 5. and 7. to run Ilaps. 
After each major release it is recomended to download the new version of Ilaps.
