from imgMS import MSData
from imgMS import MSEval
from imgMS import MSStats
from imgMS.side_functions import *

import os

files = os.listdir('./Data')
files = [f for f in files if f.endswith('.xlsx')]

print (f'proccesing files: {files}')

for file in files:
    matrices = pd.ExcelFile(f'./Data/{file}') 
    d = MSData.MSData()
    d.isotope_names = matrices.sheet_names
    for el in d.isotope_names:
        d.isotopes[el] = MSData.Isotope(el)
        d.isotopes[el].elmap = MSData.ElementalMap()
    d.import_matrices(matrices)
    
    elem = input('Enter isotope for processing: ')
    v = input('Enter vmax: ')
    
    IA = MSStats.InteractiveAverage(d)
    
    if elem is not None:
        IA.switch_elem(elem)
    if v and v.isdigit:
        vmax = int(v)
    else:
        vmax = None
         
    IA(vmax=vmax)
    name = os.path.splitext(file)[0]
    IA.export_stats(f'./stats/Stats_{name}.xlsx')
