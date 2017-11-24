import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as p
import json
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
    if 'Maximum aperture' in lens: 
        lens['Maximum aperture'] = lens['Maximum aperture'].encode('utf-8').replace(b'\xe2\x80\x93',b'-').decode('utf-8')
        lens['Maximum aperture'] = float(lens['Maximum aperture'].split('-')[0].split('F')[1])

for lens in data:
    if 'Lens mount' not in lens:
        data.remove(lens)
    elif 'Pentax KAF' in lens['Lens mount']:
        lens['Lens mount'] = 'Pentax KAF(1-3)'
# Pentax KAF, KAF2, KAF3 are all compatible and roughly the same
# so it makes sense to combine them in one category Pentax KAF(1-3)         
  
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



#lensmounts = ['Pentax KAF', 'Canon EF', 'Samsung NX', 'Four Thirds', 'Sony/Minolta Alpha', 'Nikon F (FX)', 'Leica M', 'Micro Four Thirds', 'Pentax KAF3', 'Sony E', 'Nikon 1', 'Fujifilm G', 'Canon EF-S', 'Nikon F (DX)', 'Sony FE', 'Canon EF-M', 'Pentax KAF2', 'Sony/Minolta Alpha DT', 'Fujifilm X', 'Leica TL', 'Pentax Q', 'Pentax 645AF2', 'Samsung NX-M']
# top 10:
#lensmounts = ['Canon EF','Nikon F (FX)','Sony/Minolta Alpha','Micro Four Thirds','Pentax KAF','Nikon F (DX)','Canon EF-S','Leica M','Sony E','Four Thirds']
lensmounts = ['Canon EF','Nikon F (FX)','Sony/Minolta Alpha','Micro Four Thirds','Pentax KAF(1-3)','Nikon F (DX)','Canon EF-S','Leica M','Sony E','Fujifilm X']

df = pd.DataFrame(data)
df = df[df['Lens mount'].isin(lensmounts)]
df = df[df['Lens type'] != 'Teleconverter']


figure, axes = p.subplots(nrows=2, ncols=1, figsize=(8,9))
ax1 = axes[0]
ax = axes[1]

overview = df['Lens mount'].value_counts().plot(kind='bar', legend=True, grid=True, title='Lens count by lens mount', ax=ax1, rot=60)
for x in overview.patches:
  overview.annotate(str(x.get_height()), (x.get_x(), x.get_height()))
ax1.xaxis.grid(False)

# scatterplot for number of elements/groups 'Groups' 'Elements' and the relation to lens weight
df = df[df['Elements'].notnull()].sort_values('Elements')
fedf = df[df[df['Weight'].notnull()] < 5000]

ele_major_ticks = [5,10,15,20,25]
ele_minor_ticks = list(range(3,26))
ymajor_ticks = [5,10,15,20]
yminor_ticks = list(range(3,21))

fedfplot = fedf.plot(kind='scatter',x='Elements', y='Groups', c='Weight', cmap='plasma', s=fedf['Elements'].value_counts(), legend=True, grid=True, ax=ax)
# should also add a legend for the size of the dots but it's a lot of work
# https://datasciencelab.wordpress.com/2013/12/21/beautiful-plots-with-pandas-and-matplotlib/
                
ax.set_xticks(ele_major_ticks)
ax.set_xticks(ele_minor_ticks, minor=True)
ax.set_yticks(ymajor_ticks)
ax.set_yticks(yminor_ticks, minor=True)

ax.grid(which='both')
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)

figure.tight_layout()
figure.savefig('multiplot_overview_elem')

figure2,axes2 = p.subplots(nrows=2, ncols=1, figsize=(12,8))

df[df['Weight'].notnull()].groupby('Lens mount')['Weight'].plot(kind='density', legend=True, grid=True, xlim=(0,2500), title='Lens weight (g) by mount',ax=axes2[0])
df[df['Volume'].notnull()].groupby('Lens mount')['Volume'].plot(kind='density', legend=True, grid=True, xlim=(0,2500), title='Lens size (volume cm^3) by mount',ax=axes2[1])

weight_ticks = list(range(0,2501,100))
volume_ticks = list(range(0,2501,100))

axes2[0].grid(which='minor', alpha=0.3)
axes2[0].grid(which='major', alpha=0.5)
axes2[0].set_xlabel('Weight (g)')
axes2[0].set_xticks(weight_ticks)
axes2[0].annotate('Sony E 16-50mm F3.5-5.6 kitlens ~= 116 g\nNikon 18-55mm F3.5-5.6G kitlens ~= 205 g', xy=(1000,0.0030))
axes2[1].grid(which='minor', alpha=0.3)
axes2[1].grid(which='major', alpha=0.5)
axes2[1].set_xlabel('Volume (cm^3)')
axes2[1].set_xticks(volume_ticks)
axes2[1].annotate('Sony E 16-50mm F3.5-5.6 kitlens ~= 100 cm^3\nNikon 18-55mm F3.5-5.6G kitlens ~= 209 cm^3', xy=(1000,0.004))

figure2.tight_layout()
figure2.savefig('multiplot_weight_vol')

figure3, axes3 = p.subplots(nrows=2, ncols=1, figsize=(12,10))
typeplot = df[df['Lens type'] != 'Teleconverter'].groupby(['Lens mount','Lens type']).size().unstack().plot(kind='bar', rot=45, title='Types of lenses by mount',ax=axes3[0], grid=True)
for x in typeplot.patches:
  typeplot.annotate(str(x.get_height()), (x.get_x(), x.get_height()))
axes3[0].xaxis.grid(False)

# plot elements and weight, grouped by lens type
groups = fedf.groupby('Lens type')
for name, group in groups:
  axes3[1].plot(group.Elements, group.Weight, marker='.', linestyle='', label=name)

ymajor_ticks = list(range(0,5001,1000))
yminor_ticks = list(range(0,5001,500))

axes3[1].set_xticks(ele_major_ticks)
axes3[1].set_xticks(ele_minor_ticks, minor=True)
axes3[1].set_yticks(yminor_ticks, minor=True)
axes3[1].set_yticks(ymajor_ticks)
axes3[1].grid(which='minor', alpha=0.3)
axes3[1].grid(which='major', alpha=0.5)
axes3[1].set_xlabel('Number of elements')
axes3[1].set_ylabel('Weight (g)')
axes3[1].set_title('Number of lens elements relative to weight')
axes3[1].legend()
#axes3[1].title('Lens weight & number of elements, by type')
  
figure3.tight_layout()
figure3.savefig('types_by_mount_elements_by_type')


figure4, axes4 = p.subplots(nrows=1, ncols=1, figsize=(9,7))

groups = fedf[fedf['Maximum aperture'] < 8.1].groupby('Lens type')
for name, group in groups:
    axes4.plot(group['Maximum aperture'], group['Elements'], marker='.', linestyle='', label=name)
  
ap_major_ticks = [1.4,2,2.8,3.5,4,5,5.6,6.3,7,8]
ap_minor_ticks = list(range(0,9,1))

axes4.legend()
axes4.set_xlabel('Maximum aperture')
axes4.set_ylabel('Number of elements')
axes4.set_yticks(ele_major_ticks)
axes4.set_yticks(ele_minor_ticks, minor=True)

axes4.set_xticks(ap_major_ticks)
axes4.set_xticks(ap_minor_ticks, minor=True)

axes4.grid(which='minor', alpha=0.3)
axes4.grid(which='major', alpha=0.5)

axes4.set_title('Number of lens elements relative to maximum aperture')

figure4.savefig('aperture_elements_type')
p.show()

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