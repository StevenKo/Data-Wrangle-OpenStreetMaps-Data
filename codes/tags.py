#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
Before you process the data and add it into MongoDB, you should
check the "k" value for each "<tag>" and see if they can be valid keys in MongoDB,
as well as see if there are any other potential problems.

We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data model
and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with problematic characters.
Please complete the function 'key_type'.
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys, others):

    if element.tag == "tag":
        key = element.attrib['k']
        if re.match(lower, key) != None:
            keys['lower'] += 1
        elif re.match(lower_colon, key) != None:
            keys['lower_colon'] += 1
        elif re.match(problemchars, key) != None:
            keys['problemchars'] += 1
        else:
            keys['other'] += 1
            others.add(key)
        
    return keys



def process_map(filename):
    others = set()
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys, others)

    return keys, others

if __name__ == "__main__":
    keys,others = process_map('taipei_taiwan.osm')
    pprint.pprint(keys)
    pprint.pprint(others)


""" 
rusult: 

{'lower': 363632, 'lower_colon': 72959, 'other': 7340, 'problemchars': 0}
set(['1-9F',
     'FIXME',
     'Fixme',
     'GNS:ADM1',
     'GNS:DISPLAY',
     'GNS:DSG',
     'GNS:FC',
     'GNS:GENERIC',
     'GNS:JOG',
     'GNS:LC',
     'GNS:MGRS',
     'GNS:MODIFY_DAT',
     'GNS:NT',
     'GNS:RC',
     'GNS:UFI',
     'GNS:UNI',
     'GNS:dsg_cod',
     'GNS:dsg_code',
     'GNS:dsg_string',
     'GNS:id',
     'IFR',
     'ISO3166-1',
     'ISO3166-1:alpha2',
     'ISO3166-1:alpha3',
     'ISO3166-1:numeric',
     'ISO3166-2',
     'addr:city:en',
     'addr:city:zh',
     'addr:city_1',
     'addr:district:en',
     'addr:full:en',
     'addr:full:ja',
     'addr:full:zh',
     'addr:housenumber_1',
     'addr:street:en',
     'addr:street:zh',
     'addr:street:zh-simplified',
     'addr:street_1',
     'aerialway:summer:access',
     'alt_name2',
     'alt_name3',
     'alt_name:zh-classical',
     'alt_name:zh-simplified',
     'alt_name:zh-traditional',
     'alt_name_1',
     'alt_name_2',
     'building:levels:underground',
     'capacity:motorcycle:disabled',
     'cold water',
     'construction:building:level',
     'construction:building:level:underground',
     'disused:motor_vehicle:conditional',
     'fuel:1_25',
     'fuel:e3',
     'fuel:octane_91',
     'fuel:octane_92',
     'fuel:octane_95',
     'fuel:octane_98',
     'generator:output:electricity',
     'hot water',
     'hour_off_1',
     'hour_on_1',
     'is_in:iso_3166_2',
     'lanes:backward:conditional',
     'mtb:scale:imba',
     'name:be-x-old',
     'name:en1',
     'name:fiu-vro',
     'name:zh-classical',
     'name:zh-min-nan',
     'name:zh-py',
     'name:zh-simplified',
     'name:zh-tradition',
     'name:zh-traditional',
     'name:zh-yue',
     'name:zh_TW',
     'name_1',
     'name_2',
     'naptan:AtcoCode',
     'naptan:Bearing',
     'old_addr:full:en',
     'old_addr:full:ja',
     'old_addr:full:zh',
     'old_addr:street:zh-simplified',
     'old_name2',
     'old_name:zh-py',
     'old_name_02',
     'old_ref1',
     'old_ref2',
     'operator_1',
     'operator_2',
     'operator_3',
     'parking:condition:right',
     'parking:lane:both',
     'parking:lane:left',
     'parking:lane:right',
     'phone2',
     'phone_1',
     'railway_1',
     'ref.en',
     'ref.zh',
     'ref:ruian:addr',
     'ref_1',
     'roof:type:height',
     'seamark:light:1:character',
     'seamark:light:1:colour',
     'seamark:light:1:group',
     'seamark:light:1:height',
     'seamark:light:1:period',
     'seamark:light:1:range',
     'seamark:light:1:sector_end',
     'seamark:light:1:sector_start',
     'seamark:light:1:sequence',
     'seamark:light:category',
     'seamark:light:character',
     'seamark:light:colour',
     'seamark:light:height',
     'seamark:light:period',
     'seamark:light:range',
     'seamark:light:reference',
     'seamark:light:sequence',
     'seamark:light_major:height',
     'seamark:light_minor:height',
     'seamark:radar_transponder:category',
     'seamark:radar_transponder:group',
     'seamark:radar_transponder:period',
     'short_name2',
     'source:name:en',
     'source_1',
     'species:zh-hant',
     'sport_1',
     'sport_2',
     'sport_3',
     'surface.material',
     'warm water',
     'warn water',
     'website_1',
     u'\u5099\u8a3b',
     u'\u5fe0\u5b5d\u8def142\u865f',
     u'\u7403\u985e',
     u'\u7db2\u5740'])

"""