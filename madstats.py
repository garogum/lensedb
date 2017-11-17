import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as p
import json
from functools import reduce
import pandas as pd
import glob
import os

# read all the json files into one all.json file and load that data
if os.path.isdir(os.getcwd()+'/lens_specs'):
    read_files = glob.glob("lens_specs/*.json")
else:
    print("[!] /lens_specs doesn't exist so you might have skipped some steps...\nExiting")
    quit()
with open("all.json", "w") as outfile:
    outfile.write('[{}]'.format(','.join([open(f, "r").read() for f in read_files])))
with open("all.json") as data_file:
    data = json.load(data_file)

# a lot of cleaning up before throwing it in a dataframe
        
for lens in data:
    if 'Weight' in lens:
        lens['Weight'] = int(lens['Weight'].split("g")[0].strip())
    if 'Diameter' in lens:
        lens['Diameter'] = int(lens['Diameter'].split("mm")[0].strip())
        # compute area from diameter piR^2
        aux = 3.1415 * pow((lens['Diameter'])/2,2) # in mm square
    if 'Length' in lens:
        lens['Length'] = int(lens['Length'].split("mm")[0].strip())
        vol = aux * lens['Length'] # in mm cube
        lens['Volume'] = round(vol/1000) # in cm cube
    if 'Number of diaphragm blades' in lens:
        lens['Number of diaphragm blades'] = int(lens['Number of diaphragm blades'])
    if all(x in lens for x in ['Elements', 'Groups']):
        lens['Elements'] = int(lens['Elements'])
        lens['Groups'] = int(lens['Groups'])

for lens in data:
    if 'Lens mount' not in lens:
        data.remove(lens)
        
for lens in data:
    mounts = [x.strip() for x in lens['Lens mount'].split(",")]
    if len(mounts) > 1 :
        lens['Lens mount'] = mounts

for lens in reversed(data):
    if type(lens['Lens mount']) == list:
        data.remove(lens)
        for mount in lens['Lens mount']:
            newlens = lens.copy()
            newlens['Lens mount'] = mount
            #print(newlens['Lens mount'])
            data.append(newlens)
            
df = pd.DataFrame(data)

lensmounts = ['Pentax KAF', 'Canon EF', 'Samsung NX', 'Four Thirds', 'Sony/Minolta Alpha', 'Nikon F (FX)', 'Leica M', 'Micro Four Thirds', 'Pentax KAF3', 'Sony E', 'Nikon 1', 'Fujifilm G', 'Canon EF-S', 'Nikon F (DX)', 'Sony FE', 'Leica SL', 'Canon EF-M', 'Pentax KAF2', 'Sony/Minolta Alpha DT', 'Fujifilm X', 'Leica TL', 'Pentax Q', 'Pentax 645AF2', 'Samsung NX-M']

df.groupby('Lens mount')['Weight'].plot(kind='density')