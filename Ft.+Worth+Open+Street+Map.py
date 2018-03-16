
# coding: utf-8

# In[1]:

import xml.etree.cElementTree as ET
import pprint

from collections import defaultdict
import re
filename = 'FTWORTH.xml'


# In[2]:


def count_tags(filename):
    tag_count = {}
    for event, element in ET.iterparse(filename, events=("start",)):
        add_tag(element.tag, tag_count)
    return tag_count

def add_tag(tag, tag_count):
    if tag in tag_count:
        tag_count[tag] += 1
    else:
        tag_count[tag] = 1


def test():

    tags = count_tags(filename)
    pprint.pprint(tags)
    assert tags == {
        'bounds': 1,
        'member': 9228,
        'meta': 1,
        'nd': 346342,
        'node': 307175,
        'note': 1,
        'osm': 1,
        'relation': 109,
        'tag': 133992,
        'way': 35600}


    
if __name__ == "__main__":
    test()


# In[3]:

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        key = element.attrib["k"]
        if lower.search(key):
            keys['lower'] += 1
            ###            
        elif lower_colon.search(key):
            keys['lower_colon'] += 1
            ###
        elif problemchars.search(key):
            keys["problemchars"] += 1
            ###
        else:
            keys['other'] += 1
            ###
    return keys




def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertion below will be incorrect then.
    # Note as well that the test function here is only used in the Test Run;
    # when you submit, your code will be checked against a different dataset.
    keys = process_map(filename)
    pprint.pprint(keys)
    assert keys == {'lower': 48048, 'lower_colon': 85236, 'other': 708, 'problemchars': 0}


if __name__ == "__main__":
    test()


# In[22]:

#Street Types Auditing 


street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_types[street_type] += 1

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print("%s: %d" % (k, v))
   #Finding the street abbreviations      
def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

        
def audit():
    for event, elem in ET.iterparse(filename):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])    
    print_sorted_dict(street_types)    


if __name__ == '__main__':
    audit()


# In[23]:

OSMFILE = "FTWORTH.xml"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

#Words  included that did not need corrections
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Terrace", "West","Way","South", "Run","Plaza", "North",
            "Levee","Highway", "Gipson", "Freeway", "East", "Drive", "Circle","A","B","C","D","E","G",
           "H","I", "J", "K", "L", "M", "N", "O", "P", "201"]

# Abbreviations that need to be fixed  
mapping = { "St": "Street",
            "Ave" : "Avenue",
            "Blvd": "Boulevard",
            "Dr" : "Drive"
            }

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r", encoding='utf-8')
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

# updating the abbreviations 
def update_name(name, mapping):
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        better_type = street_type
        for problem_type in mapping:
            if street_type == problem_type:
                better_type = mapping[problem_type]
                
        better_name = name.replace(street_type, better_type)
        return better_name
        

    

    return name

def st_test():
    st_types = audit(OSMFILE)

    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.items():
        for name in ways:
            better_name = update_name(name, mapping)
            print(name, "=>", better_name)
            
if __name__ == '__main__':
    st_test()


# In[35]:



#Auditing the Cuisine Type
cuisine_type_re = re.compile(r'\S+\.?$',re.IGNORECASE)
cuisine_types = defaultdict(int)

def audit_cuisine_type(cuisine_types, cuisine_name):
    m = cuisine_type_re.search(cuisine_name)
    if m:
        cuisine_type = m.group()
        cuisine_types[cuisine_type] += 1
        
        
 #Finding all the differnt categories for Cusine        
def is_cuisine_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "cuisine")
        

def audit_cuisine():
    for event, elem in ET.iterparse(filename):
        if is_cuisine_name(elem):
            audit_cuisine_type(cuisine_types, elem.attrib['v'])    
    print_sorted_dict(cuisine_types)    


if __name__ == '__main__':
    audit_cuisine()
    


# ## Deleting Coffee_Shop as a Cuisine

# In[37]:

#Words  included that did not need corrections
expected = ["american", "barbecue", "burger", "chicken", "italian", "mexican", "mixed", "sandwich","steak_house"] 
# Incorrect Cuisine that needs to be deleted  
mapping = { "coffee_shop": " "}




def audit_cuisine_type(cuisine_types, cuisine_name):
    n = cuisine_type_re.search(cuisine_name)
    if n:
        cuisine_type = n.group()
        if cuisine_type not in expected:
            cuisine_types[cuisine_type].add(cuisine_name)


def is_cuisine_name(elem):
    return (elem.attrib['k'] == "cuisine")


def audit_cuisine(osmfile):
    osm_file = open(osmfile, "r", encoding='utf-8')
    cuisine_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_cuisine_name(tag):
                    audit_cuisine_type(cuisine_types, tag.attrib['v'])
    osm_file.close()
    return cuisine_types

# updating the abbreviations 
def update_cuisine_name(cuisine_name, mapping):
    n = cuisine_type_re.search(cuisine_name)
    if n:
        cuisine_type = n.group()
        better_cuisine_type = cuisine_type
        for problem_cuisine_type in mapping:
            if cuisine_type == problem_cuisine_type:
                better_cuisine_type = mapping[problem_cuisine_type]
                
        better_cuisine_name = cuisine_name.replace(cuisine_type, better_cuisine_type)
        return better_cuisine_name
        

    

    return cuisine_name

def cuisine_test():
    cuisine_types = audit_cuisine(OSMFILE)

    pprint.pprint(dict(cuisine_types))

    for cuisine_type, ways in cuisine_types.items():
        for cuisine_name in ways:
            better_cuisine_name = update_cuisine_name(cuisine_name, mapping)
            print(cuisine_name, "=>", better_cuisine_name)
            
if __name__ == '__main__':
    cuisine_test()




# In[38]:

#Auditing for Further Improvements with Parking lots
amenity_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
amenity_types = defaultdict(int)

def audit_amenity_type(amenity_types, amenity_name):
    m = amenity_type_re.search(amenity_name)
    if m:
        amenity_type = m.group()
        amenity_types[amenity_type] += 1
        
        
#Finding the different Amenity types:        
def is_amenity_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "amenity")
        

def audit_amenity():
    for event, elem in ET.iterparse(filename):
        if is_amenity_name(elem):
            audit_amenity_type(amenity_types, elem.attrib['v'])    
    print_sorted_dict(amenity_types)    


if __name__ == '__main__':
    audit_amenity()
    
 


# In[ ]:

#Database Setup 
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

OSM_PATH = "FTWORTH.xml"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def load_new_tag(element, secondary, default_tag_type):
    """
    Load a new tag dict to go into the list of dicts for way_tags, node_tags
    """
    new = {}
    new['id'] = element.attrib['id']
    if ":" not in secondary.attrib['k']:
        new['key'] = secondary.attrib['k']
        new['type'] = default_tag_type
    else:
        post_colon = secondary.attrib['k'].index(":") + 1
        new['key'] = secondary.attrib['k'][post_colon:]
        new['type'] = secondary.attrib['k'][:post_colon - 1]
    new['value'] = secondary.attrib['v']
    #print "!23123"
    #print secondary.attrib['v']
    #print"!2312"
    return new


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    if element.tag == 'node':
        for attrib, value in element.attrib.items():
            if attrib in node_attr_fields:
                node_attribs[attrib] = value
        
        # for elements within the top element
        for secondary in element.iter():
            if secondary.tag == 'tag':
                if problem_chars.match(secondary.attrib['k']) is not None:
                    continue
                else:
                    new = load_new_tag(element, secondary, default_tag_type)
                    tags.append(new)
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        for attrib, value in element.attrib.items():
            if attrib in way_attr_fields:
                way_attribs[attrib] = value
                
        counter = 0
        for secondary in element.iter():
            if secondary.tag == 'tag':
                if problem_chars.match(secondary.attrib['k']) is  None:
                    
                
                    new = load_new_tag(element, secondary, default_tag_type)
                    tags.append(new)
            if secondary.tag == 'nd':
                newnd = {}
                newnd['id'] = element.attrib['id']
                newnd['node_id'] = secondary.attrib['ref']
                newnd['position'] = counter
                counter += 1
                way_nodes.append(newnd)
        
        # print {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))



# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w', encoding="utf-8") as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w', encoding="utf-8") as nodes_tags_file,          codecs.open(WAYS_PATH, 'w',encoding="utf-8") as ways_file,          codecs.open(WAY_NODES_PATH, 'w',encoding="utf-8") as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w', encoding="utf-8") as way_tags_file:

        nodes_writer = csv.DictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = csv.DictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = csv.DictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = csv.DictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = csv.DictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
#                if validate is True:
#                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)

