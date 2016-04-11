import string

'''
For this logic puzzel there are three sections
A. Name
B. Departure Date
C. Location

- The first step is to decide which properties a given clue applies to
- Next, the implications must be determined using keywords (not, after, or, either...)
'''

class Puzzle(object):

	'''
	We need to figure out what the appropriate variables are for each logic puzzel.
	Perhaps this can be done with the POS classifier
	'''
	stopper = ['is/bez', 'to/to', 'on/on']
	keywords = ['either', 'not', 'or', 'after', 'day']

	# Lists of all properties in the given logic puzzel
	names = ['luke', 'allen', 'chris', 'julio']
	dates = ['10', '11', '12', '13']
	locations = ['buttonwillow', 'coulterville', 'farley', 'leland']

	def __init__(self, data_group): # property_array
		'''
		The {@param: data_group} is an array of arrays that contain all properties of the given logic puzzel
		as a required initialization parameter.
		For our sample puzzle, the following would be the data_group:
		"Days" : [ "June 10", "June 11", "June 12", "June 13" ],
		"Departures" : [ "Buttonwillow", "Coulterville", "Farley", "Leland" ],
		"Names" : [ "Allen", "Chris", "Julio", "Luke" ]
		'''
		self.data_group = data_group


	def process_hint(self, hint_text):

		'''
		Given the following hint_text:  Luke is scheduled to leave on June 11.
		Return the following KB map:
		    "AND" : [
            { "Names" : 3 },
            { "Days" : 1 }
        	]
		'''

		brown_stop_words = ['in', 'bez']

		# remove punctuation
		exclude = set('.')
		s = ''.join(ch for ch in hint_text if ch not in exclude)
		new_hint = [i for i in s.split() if i not in self.stopper]
		new_hint_text = list()
		hint_map = dict()
		for i in new_hint:
			new_hint_text.append(i[:i.find('/')])
			hint_map[i[:i.find('/')]] = i[i.find('/') + 1:]
		#print(hint_map)

		# Remove stop words from POS classifier
		hint_map_new = { k:v for k,v in hint_map.items() if v not in brown_stop_words}
		for (k,v) in self.data_group.items():
			for word in hint_map_new:
				if word in v:
					print(word)
					print("{}: {}".format(k, v.index(word)))

		#iterate through all elements in data group to check for contents

		# return appropriate KB map result

	def print_hint(self):
		print("original text: ", self.text)
		print(self.sections['names'])
		print(self.sections['dates'])
		print(self.sections['locations'])
		print(self.sections['keywords'])






