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
            data.append(newlens)
            
df = pd.DataFrame(data)

#lensmounts = ['Pentax KAF', 'Canon EF', 'Samsung NX', 'Four Thirds', 'Sony/Minolta Alpha', 'Nikon F (FX)', 'Leica M', 'Micro Four Thirds', 'Pentax KAF3', 'Sony E', 'Nikon 1', 'Fujifilm G', 'Canon EF-S', 'Nikon F (DX)', 'Sony FE', 'Canon EF-M', 'Pentax KAF2', 'Sony/Minolta Alpha DT', 'Fujifilm X', 'Leica TL', 'Pentax Q', 'Pentax 645AF2', 'Samsung NX-M']
# top 10:
lensmounts = ['Canon EF','Nikon F (FX)','Sony/Minolta Alpha','Micro Four Thirds','Pentax KAF','Nikon F (DX)','Canon EF-S','Leica M','Sony E','Four Thirds']

df = df[df['Lens mount'].isin(lensmounts)]
# TODO remove teleconverters

figure2,axes2 = p.subplots(nrows=2, ncols=1, figsize=(12,8))
# https://pandas.pydata.org/pandas-docs/stable/visualization.html#plotting-with-error-bars
# https://stackoverflow.com/questions/34917727/stacked-bar-plot-by-grouped-data-with-pandas
df[df['Weight'].notnull()].groupby('Lens mount')['Weight'].plot(kind='density', legend=True, grid=True, xlim=(0,2500), title='Lens weight (g) by mount',ax=axes2[0])
df[df['Volume'].notnull()].groupby('Lens mount')['Volume'].plot(kind='density', legend=True, grid=True, xlim=(0,2500), title='Lens size (volume cm^3) by mount',ax=axes2[1])
axes2[0].grid(which='major', alpha=0.5)
axes2[1].grid(which='major', alpha=0.5)
figure2.tight_layout()
figure2.savefig('multiplot_weight_vol')

figure, axes = p.subplots(nrows=2, ncols=1, figsize=(8,9))
ax1 = axes[0]
ax = axes[1]

overview = df['Lens mount'].value_counts().plot(kind='bar', legend=True, grid=True, title='Lens count by lens mount', ax=ax1, rot=60)
for x in overview.patches:
  overview.annotate(str(x.get_height()), (x.get_x(), x.get_height()))
ax1.xaxis.grid(False)
#p.subplots_adjust(bottom=0.30)

# scatterplot for number of elements/groups 'Groups' 'Elements' and the relation to lens weight
elementsdf = df[df['Elements'].notnull()].sort_values('Elements')[['Elements', 'Groups','Weight']]
fedf = elementsdf[elementsdf[elementsdf['Weight'].notnull()] < 5000]

xmajor_ticks = [5,10,15,20,25]
xminor_ticks = list(range(3,26))
ymajor_ticks = [5,10,15,20]
yminor_ticks = list(range(3,21))

fedfplot = fedf.plot(kind='scatter',x='Elements', y='Groups', c='Weight', cmap='plasma', s=fedf['Elements'].value_counts(), legend=True, grid=True, ax=ax)
# should also add a legend for the size of the dots but it's a lot of work
# https://datasciencelab.wordpress.com/2013/12/21/beautiful-plots-with-pandas-and-matplotlib/
                
ax.set_xticks(xmajor_ticks)
ax.set_xticks(xminor_ticks, minor=True)
ax.set_yticks(ymajor_ticks)
ax.set_yticks(yminor_ticks, minor=True)

ax.grid(which='both')
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)

figure.tight_layout()
figure.savefig('multiplot_overview_elem')

figure3, axes3 = p.subplots(nrows=1, ncols=1, figsize=(12,8))
typeplot = df[df['Lens type'] != 'Teleconverter'].groupby(['Lens mount','Lens type']).size().unstack().plot(kind='bar', rot=60, title='Types of lenses by mount',ax=axes3, grid=True)
for x in typeplot.patches:
  typeplot.annotate(str(x.get_height()), (x.get_x(), x.get_height()))
axes3.xaxis.grid(False)
figure3.tight_layout()
figure3.savefig('types_by_mount')
p.show()

# graph for Number of diaphragm blades (not too exciting, most are between 7 and 10)
# graph for type of lens (zoom or prime) and weight

'''
left our ridiculous stuff like https://www.dpreview.com/articles/8268122124/sigma250500

heaviest 20 lenses
df[df['Weight'].notnull()].sort_values('Weight')[['Weight','Model']].tail(20)

>>> df[df['Volume'].notnull()].sort_values('Volume')[['Volume','Model','Lens mount']].tail(20)
       Volume                                    Model    Lens mount
110    6412.0          Canon EF 500mm f/4.0L IS II USM      Canon EF
388    6479.0             Canon EF 500mm f/4.0L IS USM      Canon EF
605    7077.0  Nikon AF-S Nikkor 400mm f/2.8D ED-IF II  Nikon F (FX)
215    7157.0          Canon EF 400mm f/2.8L IS II USM      Canon EF
252    7198.0  Nikon AF-S Nikkor 400mm f/2.8E FL ED VR  Nikon F (FX)
630    7282.0             Canon EF 400mm f/2.8L IS USM      Canon EF
242    7399.0  Nikon AF-S Nikkor 400mm f/2.8G ED VR II  Nikon F (FX)
149    9269.0  Nikon AF-S Nikkor 800mm f/5.6E FL ED VR  Nikon F (FX)
140    9349.0     Nikon AF-S Nikkor 600mm F4E FL ED VR  Nikon F (FX)
286    9620.0             Canon EF 800mm f/5.6L IS USM      Canon EF
60     9631.0       Nikon AF-S Nikkor 600mm f/4G ED VR  Nikon F (FX)
588    9847.0    Nikon AF-S Nikkor 600mm f/4D ED-IF II  Nikon F (FX)
540    9953.0          Canon EF 600mm f/4.0L IS II USM      Canon EF
1278  10086.0               Sigma 800mm F5.6 EX DG HSM      Canon EF
1279  10086.0               Sigma 800mm F5.6 EX DG HSM  Nikon F (FX)
646   10108.0             Canon EF 600mm f/4.0L IS USM      Canon EF
1292  10531.0           Sigma 300-800mm F5.6 EX DG HSM  Nikon F (FX)
1291  10531.0           Sigma 300-800mm F5.6 EX DG HSM      Canon EF
1145  32027.0               Sigma 200-500mm F2.8 EX DG      Canon EF
1146  32027.0               Sigma 200-500mm F2.8 EX DG  Nikon F (FX)
'''