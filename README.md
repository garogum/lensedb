Similar collection of scripts as for [cameradb](https://github.com/garogum/cameradb) but for camera lenses

![2 plot figure](/multiplot.png?raw=true "Overview and elements/groups plots")

![distribution multiplot](/multiplot_weight_vol.png "Weight and Size distribution")


# Notes
Data was filtered to only include the top 10 most represented lens mounts from the set, which are:  
`lensmounts = ['Canon EF','Nikon F (FX)','Sony/Minolta Alpha','Micro Four Thirds','Pentax KAF','Nikon F (DX)','Canon EF-S','Leica M','Sony E','Four Thirds']`  
The scatterplot data was filtered to only include lenses of non-null weight < 5000 (g, so 5kg), which filters out 8 lenses (see aux info section for details).  
The larger the dots, the more lenses with that number of elements in them

# Usage
1. Run specparser.py to fetch the links for camera spec pages of all vendors listed at https://www.dpreview.com/products/. This will create a lenses.txt file which will be used as input for the scrapy crawler
2. Run `scrapy crawl lensedb`, which will fetch all pages, saving them to /lensdata, and extracting relevant info into individual JSON files under /lens_specs
3. Run madstats.py to aggregate all individual JSON files into a single all.json which will be used by pandas and matplotlib to generate plots.

# Aux info
All mounts and respective number of lenses in scraped data:

| Mount | Count |
| ------ | ------ |
| Canon EF           | 226 |
| Nikon F (FX)       | 201 |
| Sony/Minolta Alpha | 130 |
| Micro Four Thirds  |  93 |
| Pentax KAF         |  88 |
| Nikon F (DX)       |  85 |
| Canon EF-S         |  71 |
| Leica M            |  56 |
| Sony E             |  53 |
| Four Thirds        |  42 |
| Pentax KAF3        |  41 |
| Fujifilm X         |  38 |
| Sony FE            |  36 |
| Samsung NX         |  28 |
| Canon EF-M         |  17 |
| Pentax KAF2           | 15 |
| Nikon 1               | 13 |
| Sony/Minolta Alpha DT | 12 |
| Pentax Q              |  8 |
| Fujifilm G            |  6 |
| Pentax 645AF2         |  5 |
| Leica TL              |  5 |
| Samsung NX-M          |  3 |

Lenses heavier than 5kg:

| Weight (g) | Model | Lens mount |
| ----- | ----- | ----- |
| 5060.0  |    Nikon AF-S Nikkor 600mm f/4G ED VR  | Nikon F (FX) |
| 5360.0  |          Canon EF 600mm f/4.0L IS USM  |     Canon EF |
| 5370.0  |          Canon EF 400mm f/2.8L IS USM  |     Canon EF |
| 5880.0  |        Sigma 300-800mm F5.6 EX DG HSM  |     Canon EF |
| 5880.0  |        Sigma 300-800mm F5.6 EX DG HSM  | Nikon F (FX) |
| 5900.0  | Nikon AF-S Nikkor 600mm f/4D ED-IF II  | Nikon F (FX) |
| 15700.0 |             Sigma 200-500mm F2.8 EX DG |      Canon EF |
| 15700.0 |             Sigma 200-500mm F2.8 EX DG |  Nikon F (FX) |
