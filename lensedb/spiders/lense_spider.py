import scrapy
import os
import subprocess
import json

class LensSpider(scrapy.Spider):
    name = "lensedb"

    def start_requests(self):
        # specparser.py will make a "lenses" file listing all url's to all lenses to be parsed
        file = 'lenses.txt'
        with open(file) as f:
            urls = [url.strip() for url in f.readlines()]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        lens={}
        values=[]
        labels=[]
        os.makedirs("lensdata", exist_ok=True)
        os.makedirs("lens_specs", exist_ok=True)
        page = response.url.split("/")[-2]
        # Write the HTML response to a file
        # These can be used later without having to bombard dpreview.com again
        filename = os.getcwd()+'/lensdata/'+'lenses-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        
        lens_name = response.xpath('//h1[@itemprop="name"]/text()').extract()[0]
        self.log('##### Processing lens %s #####' % lens_name)
        lens['Model'] = lens_name

        # get the field keys
        for i in response.xpath('//div[@class="specificationsPage"]/table[contains(@class,"specsTable")]/tbody/tr/th/text()').extract():
            labels.append(i.strip())
            
        # get the values for the previously fetched keys in the specs table
        fieldvalues=[]
        for item in response.xpath('//div[@class="specificationsPage"]/table[contains(@class,"specsTable")]/tbody/tr/td'):
            fieldvalues.append(item.xpath('.//text()').extract())
        for fieldvalue in fieldvalues:
            values.append(' '.join(fieldvalue).strip())
        
        for label, value in zip(labels, values):
            #print(label,"-",value)
            lens[label] = value
            
        specs_file = os.getcwd()+'/lens_specs/'+'%s_specs.json' % page
        with open(specs_file, 'w') as file:
            json.dump(lens, file)
            print("##### Wrote "+ lens_name +" specs to "+ specs_file +" #####")