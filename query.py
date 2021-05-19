#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib, urllib.request
import json
from xml.dom import minidom
from json2html import *

# query from arxiv, using offical query API: https://arxiv.org/help/api/user-manua
config = json.load(open('config.json'))
query = f"http://export.arxiv.org/api/query?search_query=all:{config['subject']}&id_list=&start=0&sortBy=lastUpdatedDate&sortOrder=descending&max_results=100"
data = urllib.request.urlopen(query).read().decode('utf-8')

# parse fetched results
entries = []
dom = minidom.parseString(data)
for entry_obj in dom.getElementsByTagName('entry'):
  entry = {}
  for field in config['fields']:
    property_list = entry_obj.getElementsByTagName(field)
    entry[field] = ', '.join(map(lambda x: x.childNodes[0].nodeValue, property_list))
    entry['update'] = '*' if entry_obj.getElementsByTagName('updated')[0].childNodes[0].nodeValue != \
      entry_obj.getElementsByTagName('published')[0].childNodes[0].nodeValue else ' '
    entries.append(entry)
 
# print(entries)
table = json2html.convert(json=entries)
print(table)

with open('./arxiv.html', 'w') as f:
  f.write(table)
  
    







