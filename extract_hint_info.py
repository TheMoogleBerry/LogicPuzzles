from nltk.corpus import stopwords

'''
For this logic puzzel there are three sections
A. Name
B. Departure Date
C. Location

- The first step is to decide which section a given clue applies to
'''

class Hint(object):

	stopper = ['is', 'to', 'on']
	names = ['Luke', 'Allen', 'Chris', 'Julio']
	dates = ['10', '11', '12', '13']
	locations = ['Buttonwillow', 'Coulterville', 'Farley', 'Leland']

	def __init__(self, hint_text):
		self.text = hint_text
		self.sections = dict()

		self.process_hint(hint_text)

	def process_hint(self, hint_text):
		new_hint = [i for i in self.text.split() if i not in self.stopper]
		self.sections['names'] = list()
		self.sections['dates'] = list()
		self.sections['locations'] = list()
		for n in new_hint:
			if n in self.names:
				self.sections['names'].append(n)
			if n in self.dates:
				self.sections['dates'].append(n)
			if n in self.locations:
				self.sections['locations'].append(n)

hint = Hint("Luke is scheduled to leave on June 11")
print(hint.sections['names'])
print(hint.sections['dates'])
print(hint.sections['locations'])
