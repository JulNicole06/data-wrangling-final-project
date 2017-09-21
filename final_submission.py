#!/usr/bin/python

from street_suffix import map_street_suffix
from audit import audit_addresses
from update import update_addr
from prepare_for_database import process_map
from create_database import import_table
import sqlite3

osm_file = 'roswell.osm'

# Get list of expected street suffix names as well as map of abbreviations to full names
expected, mapping = map_street_suffix()

#print out values that require further investigation for cleaning
audit_addresses(osm_file, expected)

#convert OSM XML into .csv files while cleaning the audited data
process_map(osm_file, validate=False)

#create and connect to database
connection = sqlite3.connect('roswell.db')
cursor = connection.cursor()

#create tables from .csv files
import_table('roswell.db', 'csv_files/nodes_tags.csv', 'nodes_tags', connection, cursor)
import_table('roswell.db', 'csv_files/nodes.csv', 'nodes', connection, cursor)
import_table('roswell.db', 'csv_files/ways_nodes.csv', 'ways_nodes', connection, cursor)
import_table('roswell.db', 'csv_files/ways_tags.csv', 'ways_tags', connection, cursor)
import_table('roswell.db', 'csv_files/ways.csv', 'ways', connection, cursor)

#delete values found during auditing that do not belong in the dataset
query = "DELETE FROM nodes_tags WHERE id='4287139726'"
cursor.execute(query)
connection.commit()

query = "DELETE FROM nodes WHERE id='4287139726'"
cursor.execute(query)
connection.commit()

connection.close()