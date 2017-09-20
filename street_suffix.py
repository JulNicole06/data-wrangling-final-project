#!/usr/bin/python

import requests
from bs4 import BeautifulSoup

def map_street_suffix():
	'''
	Scrapes data table found at: "https://pe.usps.com/text/pub28/28apc_002.htm"

	OUTPUT: 
		List of expected street suffix names as well as a dictionary 
		mapping of street suffix abbreviations to full street suffix names
	'''
	with requests.Session() as session:
		response = session.get('https://pe.usps.com/text/pub28/28apc_002.htm', headers={'user-agent': 'Chrome/60.0.3112.113'})
		html = response.text
		soup = BeautifulSoup(html, "html.parser")
		table = soup.find(id='ep533076')
		expected = []
		mapping = {}
		for each in table.find_all('tr')[1:]:
		    if len(each) == 6:
		        text = str(each.text)
		        text = text.split(" ")
		        while '' in text: #remove all blank spaces created from converting unicode to str
		            text.remove('')
		        street_suffix_name = str(text[0]).capitalize() 
		        abbr = str(text[1]).capitalize()
		        expected.append(street_suffix_name)
		    else:
		        text = str(each.text)
		        text = text.split(" ")
		        while '' in text: #remove all blank spaces created from converting unicode to str
		            text.remove('')
		        abbr = str(text[0]).capitalize()
		    mapping[abbr] = street_suffix_name

	#adds additional mapping for cardinal directions
	mapping['N'] = 'North'
	mapping['S'] = 'South'
	mapping['E'] = 'East'
	mapping['W'] = 'West'
	mapping['NE'] = 'Northeast'
	mapping['NW'] = 'Northwest'
	mapping['SE'] = 'Southeast'
	mapping['SW'] = 'Southwest'

	return expected, mapping