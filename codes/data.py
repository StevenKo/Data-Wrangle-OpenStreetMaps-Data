#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

street_type_re = re.compile(u'路|街|巷|道', re.IGNORECASE)
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        node["type"] = element.tag
        node["created"] = {}
        for key in element.attrib.keys():
            val = element.attrib[key]
            if key in CREATED:
                node['created'][key] = val
            elif key == 'lat' or key == 'lon':
                node['pos']=[float(element.attrib['lat']),float(element.attrib['lon'])]
            else:
                node[key] = val
            
            
            for tag in element.iter("tag"):
                
                if is_street_name(tag):
                    if street_type_re.search(tag.attrib['v']) is None:
                        continue



                key = tag.attrib['k']
                val = tag.attrib['v']
                
                if problemchars.match(key):
                    continue
                elif key.startswith('addr:'):
                    if 'address' not in node.keys():
                        node["address"] = {}
                    if (len(key.split(':'))!=2):
                        continue
                    new_key = key[5:] # addr:
                    node["address"][new_key] = val
                else:
                    node[key] = val
                    
            if element.tag == "way":
                node['node_refs'] = []
                for nd in element.iter('nd'):
                    node['node_refs'].append(nd.attrib['ref'])
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('/Users/steven/projects/Data-Wrangle-OpenStreetMaps-Data/taipei_taiwan.osm', True)
    #pprint.pprint(data)


if __name__ == "__main__":
    test()