import string

'''
For this logic puzzel there are three sections
A. Name
B. Departure Date
C. Location

- The first step is to decide which properties a given clue applies to
- Next, the implications must be determined using keywords (not, after, or, either...)
'''

class Hint(object):

	'''
	We need to figure out what the appropriate variables are for each logic puzzel.
	Perhaps this can be done with the POS classifier
	'''
	stopper = ['is', 'to', 'on']
	keywords = ['either', 'not', 'or', 'after', 'day']

	# Lists of all properties in the given logic puzzel
	names = ['luke', 'allen', 'chris', 'julio']
	dates = ['10', '11', '12', '13']
	locations = ['buttonwillow', 'coulterville', 'farley', 'leland']

	def __init__(self, hint_text): # property_array
		'''
		Eventually include an array of arrays that contain all properties of the given logic puzzel
		as a required initialization parameter.
		For this puzzel, the following would be the property_array:
		[ ['luke', 'allen', 'chris', 'julio'],
		['10', '11', '12', '13'],
		['buttonwillow', 'coulterville', 'farley', 'leland'] ]
		'''
		self.text = hint_text.lower()
		# self.property_array = property_array
		self.sections = dict()

		self.process_hint(hint_text)

	def process_hint(self, hint_text):
		# remove punctuation
		exclude = set(string.punctuation)
		s = ''.join(ch for ch in self.text if ch not in exclude)
		new_hint = [i for i in s.split() if i not in self.stopper]
		self.sections['names'] = list()
		self.sections['dates'] = list()
		self.sections['locations'] = list()
		self.sections['keywords'] = list()
		for n in new_hint:
			if n in self.names:
				self.sections['names'].append(n)
			if n in self.dates:
				self.sections['dates'].append(n)
			if n in self.locations:
				self.sections['locations'].append(n)
			if n in self.keywords or ( n.isdigit() and n not in self.dates):
				self.sections['keywords'].append(n)

	def print_hint(self):
		print("original text: ", self.text)
		print(self.sections['names'])
		print(self.sections['dates'])
		print(self.sections['locations'])
		print(self.sections['keywords'])

hint1 = Hint('The person departing from Buttonwillow will leave 2 days after Julio.')
hint2 = Hint('The person working on June 11 is either the person departing from Coulterville or Allen.')
hint3 = Hint('The conductor departing from Leland will leave 1 day after Chris')
hint4 = Hint('Luke is scheduled to leave on June 11.')

hints = [hint1, hint2, hint3, hint4]
for hint in hints:
	hint.print_hint()




