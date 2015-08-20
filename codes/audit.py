# -*- coding: utf-8 -*-  

"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint



class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)



OSMFILE = "/Users/steven/projects/Data-Wrangle-OpenStreetMaps-Data/taipei_taiwan.osm"
street_type_re = re.compile(u'路|街|巷|道', re.IGNORECASE)


expected = [u"路", u"街", u"巷", u"道"]

def audit_street_type(street_types, street_name,do_not_match_street_types):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
    else:
        do_not_match_street_types.add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    do_not_match_street_types = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    # print(tag.attrib['v'])
                    audit_street_type(street_types, tag.attrib['v'],do_not_match_street_types)

    return street_types,do_not_match_street_types

if __name__ == '__main__':
    st_types,no_match_types = audit(OSMFILE)
    MyPrettyPrinter().pprint(dict(st_types)) 

    print "do not match:"
    MyPrettyPrinter().pprint(no_match_types)



"""
result:

do not match:
set(['87',
     'Alley 1, Ln. 325, Jie Shou Rd. Sec. 2',
     'Alley 1-1, Ln. 325, Jie Shou Rd. Sec. 2',
     "Alley 10, Long'an Ln.",
     "Alley 18, Long'an Ln.",
     'Alley 19-1, Ln. 361, Sec. 2, Jieshou Rd.',
     'Alley 19-3, Ln. 361, Sec. 2, Jieshou Rd.',
     'Alley 19-5, Ln. 361, Sec. 2, Jieshou Rd.',
     "Alley 2, Long'an Ln.",
     'Alley 3-2, Ln. 325, Jie Shou Rd. Sec. 2',
     'Alley 3-3, Ln. 325, Jie Shou Rd. Sec. 2',
     'Alley 33, Ln. 361, Sec. 2, Jieshou Rd.',
     'Alley 43, Ln. 361, Jieshou Rd. Sec. 2',
     'Alley 43-33, Ln. 361, Jieshou Rd. Sec. 2',
     'Alley 43-41, Ln. 361, Jieshou Rd. Sec. 2',
     'Alley 53, Ln. 361, Sec. 2, Jieshou Rd.',
     'Alley 63, Ln. 361, Sec. 2, Jieshou Rd.',
     'Ln. 325, Jieshou Rd. Sec. 2',
     "Long'an Ln.",
     'Shia-Guei-Rou-Shan',
     三界公坑,
     二坪,
     南山里乾坑,
     圳頭坑,
     埔心村,
     新北市坪林區漁光里楣子寮,
     桃園縣新屋鄉東明村2鄰東勢,
     石門區德茂里下員坑,
     萬里加投,
     訊塘村5鄰訊塘埔,
     金鋒,
     錫板里海尾,
     雙興1鄰7-8號,
     霞雲])


""" 