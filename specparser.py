from bs4 import BeautifulSoup
import requests
import re
import os

lenses = ["canon","fujifilm","leica","nikon","olympus","panasonic","pentax","samsung","samyang","sigma","sony","tamron","tokina","voigtlander","zeiss"]

listoflinks = []

for company in lenses:
    r = requests.get("https://www.dpreview.com/products/"+company+"/lenses?subcategoryId=lenses")
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    for link in soup.find_all('a'):
        lens = re.findall('.*buy', link.get('href'))
        if lens and 'products' in lens[0]:
            lens = lens[0].replace('buy', 'specifications')
            listoflinks.append(lens)
            if len(listoflinks) in range(0,5000,100):
                print("[!] Processed",len(listoflinks),"lens links...")
                
with open(os.getcwd()+'/lenses.txt', 'w') as f:
    for i in listoflinks:
        f.write(i+'\n')
print("[!] Finished writing",len(listoflinks)," lenses to",os.getcwd()+'/lenses.txt')