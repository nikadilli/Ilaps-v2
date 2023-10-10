### INTERACTIVE MEAN

This module is intended for statistical processing of images created by Ilaps. In the future, 
it will be a part of Ilaps. For now, it can be run as a separate skript in order to allow 
Ilaps users to work with it.

This module offers interactive area selection in the image of elemental composition and 
returns basic statistical values (mean, std, sum, min, max, med) of the values in selected 
area for every isotope. At the beginning, the user can select which isotope is shown for the 
area selection and set vmax (define the range of values that the colormap covers). If there 
is no input from user, the first isotope is used and the range is not limited. After the 
selection of the desired area, the stats are printed in the comand line. It is possible to 
repeat the selection, until satisfied. When the image window is closed, the last selection
is exported in excel file with all stats and an image of the selection. If there are multiple 
maps in the data folder, they will be processed one by one.

For simpler use, there is a start file for windows, which will automatically setup the 
environment and run the skript. To use start file, first edit the path to venv in it. 
