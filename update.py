#!/usr/bin/python

def update_word(word, mapping, expected):
	'''
		INPUT: 
			word: possible abbreviation
			mapping: dictionary mapping of known abbreviations to full street suffix names
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
			mapping: dictionary mapping of known abbreviations to full street suffix names
			expected: list of expected street suffix names

		OUTPUT: 
			formatted tag value
	'''
	if key == "street":
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
	elif key == "city":
		if value == "Sandy Springa":
			value = "Sandy Springs"
		return value
	elif key == "state":
		if value == "Georgia":
			value = "GA"
		return value.upper()
	elif key == "postcode":
		return value[0:5]
	else:
		return value