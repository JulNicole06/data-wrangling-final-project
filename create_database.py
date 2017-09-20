#!/usr/bin/python

import sqlite3
import csv
from pprint import pprint


def import_table(database, csv_file, table_name, connection, cursor):
	'''
		INPUT: 
			database: desired database filename
			csv_file: file with data for import
			table_name: desired table name for SQL database
			connection: SQL connection
			cursor: cursor object

		OUTPUT:
			database file with newly created tables

	'''	
	if table_name == 'nodes_tags':
		cursor.execute('''
			CREATE TABLE nodes_tags(id INTEGER, key TEXT, value TEXT, type TEXT)
			''')
		connection.commit()

		with open(csv_file, 'rb') as file_in:
			reader = csv.DictReader(file_in)
			to_sql = []
			for row in reader:
				to_sql.append([row['id'].decode("utf-8"), 
								row['key'].decode("utf-8"),
								row['value'].decode("utf-8"), 
								row['type'].decode("utf-8")])

		cursor.executemany("INSERT INTO nodes_tags(id, key, value, type) VALUES (?, ?, ?, ?);", to_sql)
		connection.commit()


	elif table_name == 'ways_tags':
		cursor.execute('''
			CREATE TABLE ways_tags(id INTEGER, key TEXT, value TEXT, type TEXT)
			''')
		connection.commit()

		with open(csv_file, 'rb') as file_in:
			reader = csv.DictReader(file_in)
			to_sql = []
			for row in reader:
				to_sql.append([row['id'].decode("utf-8"), 
								row['key'].decode("utf-8"),
								row['value'].decode("utf-8"), 
								row['type'].decode("utf-8")])

		cursor.executemany("INSERT INTO ways_tags(id, key, value, type) VALUES (?, ?, ?, ?);", to_sql)
		connection.commit()


	elif table_name == 'nodes':
		cursor.execute('''
			CREATE TABLE nodes(id INTEGER, lat FLOAT, lon FLOAT, user TEXT, uid INTEGER, \
									version TEXT, changeset INTEGER, timestamp TEXT)
			''')
		connection.commit()

		with open(csv_file, 'rb') as file_in:
			reader = csv.DictReader(file_in)
			to_sql = []
			for row in reader:
				to_sql.append([row['id'].decode("utf-8"), 
								row['lat'].decode("utf-8"),
								row['lon'].decode("utf-8"),
								row['user'].decode("utf-8"), 
								row['uid'].decode("utf-8"), 
								row['version'].decode("utf-8"),
								row['changeset'].decode("utf-8"), 
								row['timestamp'].decode("utf-8")])

		cursor.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_sql)
		connection.commit()



	elif table_name == 'ways':
		cursor.execute('''
			CREATE TABLE ways(id INTEGER, user TEXT, uid INTEGER, version TEXT, \
									changeset INTEGER, timestamp TEXT)
			''')
		connection.commit()

		with open(csv_file, 'rb') as file_in:
			reader = csv.DictReader(file_in)
			to_sql = []
			for row in reader:
				to_sql.append([row['id'].decode("utf-8"), 
								row['user'].decode("utf-8"), 
								row['uid'].decode("utf-8"),
								row['version'].decode("utf-8"), 
								row['changeset'].decode("utf-8"), 
								row['timestamp'].decode("utf-8")])

		cursor.executemany("INSERT INTO ways(id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_sql)
		connection.commit()




	elif table_name == 'way_nodes':
		cursor.execute('''
			CREATE TABLE ways_nodes(id INTEGER, node_id INTEGER, position INTEGER)
			''')	
		connection.commit()

		with open(csv_file, 'rb') as file_in:
			reader = csv.DictReader(file_in)
			to_sql = []
			for row in reader:
				to_sql.append([row['id'].decode("utf-8"), 
								row['node_id'].decode("utf-8"),
								row['position'].decode("utf-8")])

		cursor.executemany("INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);", to_sql)
		connection.commit()




