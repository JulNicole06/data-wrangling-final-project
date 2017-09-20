#!/usr/bin/python
import xml.etree.cElementTree as ET
import re
import csv
import codecs
import cerberus
from schema import SCHEMA
import update
from street_suffix import map_street_suffix

expected, mapping = map_street_suffix()


NODES_PATH = "csv_files/nodes.csv"
NODE_TAGS_PATH = "csv_files/nodes_tags.csv"
WAYS_PATH = "csv_files/ways.csv"
WAY_NODES_PATH = "csv_files/ways_nodes.csv"
WAY_TAGS_PATH = "csv_files/ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

def get_tags(element, element_id, problem_chars=PROBLEMCHARS, default_tag_type='regular'):
	tags = []
	for tag in element.iter('tag'):
		tags_dict = {}
		key = tag.get('k')
		if re.search(problem_chars, key) is None:
			tags_dict["id"] = element_id
			if ":" in key:
				key = key.split(":", 1)
				tags_dict['key']=str(key[1])
				tags_dict['type']=str(key[0])
			else:
				tags_dict['key']=str(key)
				tags_dict['type']=default_tag_type
			if tags_dict['type'] == 'addr' or tags_dict['type'] == 'tiger':
				value = tag.get('v')
				tags_dict['value'] = update.update_addr(tags_dict['key'], value, mapping, expected)
			else:
				tags_dict['value']=tag.get('v')
			tags.append(tags_dict)
	return tags
		
def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS):
	"""Clean and shape node or way XML element to Python dict"""

	node_attribs = {}
	way_attribs = {}
	way_nodes = []

	if element.tag == "node":
		for each in node_attr_fields:
			attribute = element.get(each)
			node_attribs[each] = attribute
		node_id = node_attribs['id']
		tags = get_tags(element, node_id)
		return {'node': node_attribs, 'node_tags': tags}

	elif element.tag == 'way':
		for each in way_attr_fields:
			attribute = element.get(each)
			way_attribs[each] = attribute
		way_id = way_attribs['id']
		tags = get_tags(element, way_id)
		i = 0
		for node in element.iter('nd'):
			nodes_dict = {}
			nodes_dict['id'] = way_id
			nodes_dict['node_id'] = node.get('ref')
			nodes_dict['position'] = i
			way_nodes.append(nodes_dict)
			i +=1
		return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}



	# ================================================== #
	#               Helper Functions                     #
	# ================================================== #
def get_element(osm_file, tags):
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


class UnicodeDictWriter(csv.DictWriter, object):
	"""Extend csv.DictWriter to handle Unicode input"""

	def writerow(self, row):
		super(UnicodeDictWriter, self).writerow({
			k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
		})

	def writerows(self, rows):
		for row in rows:
			self.writerow(row)


	# ================================================== #
	#               Main Function                        #
	# ================================================== #
def process_map(file_in, validate):
	"""Iteratively process each XML element and write to csv(s)"""

	with codecs.open(NODES_PATH, 'w') as nodes_file, \
		codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
		codecs.open(WAYS_PATH, 'w') as ways_file, \
		codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
		codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

		nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
		node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
		ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
		way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
		way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

		nodes_writer.writeheader()
		node_tags_writer.writeheader()
		ways_writer.writeheader()
		way_nodes_writer.writeheader()
		way_tags_writer.writeheader()

		validator = cerberus.Validator()
		i = 0
		for element in get_element(file_in, tags=('node', 'way')):
			el = shape_element(element)
			if (i % 10000) == 0:
				print "check in: " + str(i)
			if el:
					
				if validate is True:
					validate_element(el, validator)

				if element.tag == 'node':
					nodes_writer.writerow(el['node'])
					node_tags_writer.writerows(el['node_tags'])
				elif element.tag == 'way':
					ways_writer.writerow(el['way'])
					way_nodes_writer.writerows(el['way_nodes'])
					way_tags_writer.writerows(el['way_tags'])
				i += 1

