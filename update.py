#!/usr/bin/python

def update_word(word, mapping, expected):
	'''
		INPUT: 
			word: possible abbreviation
			mapping: dictionary mapping of known abbreviations to full
				street suffix names
			expected: list of expected street suffix names
		OUTPUT: 
			full street suffix name if word is a known abbreviation,
				original word if it is not.  
	'''
	if word not in expected:
		try:
			new_word = mapping[word]
			return new_word
		except KeyError:
			return word
	else:
		return word

def update_addr(key, value, mapping, expected):
	'''
		INPUT:
			key: tag key name
			value: tag value
			mapping: dictionary mapping of known abbreviations to full
				street suffix names
			expected: list of expected street suffix names

		OUTPUT: 
			formatted tag value
	'''
	if key == "street" or "name" in key:
		value_split = value.split()
		i = 0
		new_value = ""
		while i < len(value_split):
			if value_split[i] != None:
				word = value_split[i]
				word = word.capitalize().replace(".", "")
				word = update_word(word, mapping, expected)
				new_value += word + " "
			i += 1
		return new_value
	elif key == "state":
		return value.upper()
	elif key == "postcode" or "zip" in key:
		if len(value) < 5:
			new_value = "0"+value
			return new_value
		elif "-" in value:
			return str(value[0:5])
		else:
			return value
	elif key == "city":
		return value.capitalize()
	else:
		return value