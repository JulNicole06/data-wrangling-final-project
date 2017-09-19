#!/usr/bin/python

import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import csv

def audit_street_type(street_types, street_name, expected_list):
	''' INPUT: 
		street_types: initial empty dict variable to input values
		street_name: street name value to evaluate
		expected_list: list of expected street names

		OUTPUT: 
		dictionary of street names that are not found in the expected list '''

	street_name_split = street_name.split()
	street_type = street_name_split[-1]
	if street_type not in expected_list:
		street_types[street_type].add(street_name)
	return street_types

def audit_addresses(filename, expected_list):
	'''
	INPUT: filename: file name of file to audit 
		   expected_list: list of expected street names

	OUTPUT: printout of suspicious values found in file
	'''
	with open(filename, "r") as f:
		street_types = defaultdict(set)
		states = []
		postcodes = []
		irregular_postcodes = []
		tags = []
		tiger_tags = []
		for event, elem in ET.iterparse(f, events=("start",)):
			if elem.tag == "node" or elem.tag == "way":
				location_id = elem.get('id')
				for tag in elem.iter("tag"):
					if tag.attrib['k'] == "addr:street" or "tiger:name_type" in tag.attrib['k']:
						street_types = audit_street_type(street_types, tag.attrib['v'], expected_list)
					elif tag.attrib['k'] == "addr:state" and tag.attrib['v'] not in states:
						states.append(tag.attrib['v'])
					elif (tag.attrib['k'] == "addr:postcode" or "tiger:zip" in tag.attrib['k']) and \
						tag.attrib['v'] not in postcodes:
						postcodes.append(tag.attrib['v'])
					for each in postcodes:
						if (len(each)<5 or len(each)>5) and each not in irregular_postcodes:
							irregular_postcodes.append(each)
						
		print "Street Types: "
		pprint.pprint(dict(street_types))
		print "-------------------------"  
		print "States Represented: "
		print states
		print "-------------------------"  
		print "Irregular Postcodes: "
		print irregular_postcodes
		print "-------------------------"   