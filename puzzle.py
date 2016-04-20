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
	stopper = ['is/bez', 'to/to', 'on/on', 'june/np']
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
		self.kb_rule_list = list() # list of KB rules

	def process_hint(self, hint_text):

		'''
		Given the following hint_text:  Luke is scheduled to leave on June 11.
		Append the following rule to self.kb_rule_list:
		    "AND" : [
            { "Names" : 3 },
            { "Days" : 1 }
        	]

        Given the following hint_text: The conductor departing from Leland will leave 1 day after Chris.
    	Append the following 2 rules to self.kb_rule_list:
    	{
        	"AND" : [
            { "Departures" : 3 },
            { "OR" : { "Days" : [1,2,3] } },
            { "OR" : { "Names" : [0,2,3] } }
        	]
        }, 

        OR notes:
        first_np-> first map


        {
            "AND" : [
                { "Departures" : 3 },
                { "EXPR" : {
                    "Names" : 1,
                    "DataGroup" : "Days",
                    "OP" : "PLUS",
                    "NUM" : 1
                    }
                }
            ]
        },
		'''

		brown_stop_words = ['in', 'bez']
		expr_words = {'after': 'PLUS', 'before': 'SUBTRACT', 'less': 'SUBTRACT', 'more': 'PLUS'}
		data_group_words = ['day', 'days']

		has_expression = False

		# remove punctuation
		exclude = set('.')
		s = ''.join(ch for ch in hint_text if ch not in exclude)
		new_hint = [i for i in s.lower().split() if i not in self.stopper]
		new_hint_text = list()
		hint_map = dict()
		for i in new_hint:
			new_hint_text.append(i[:i.find('/')])
			hint_map[i[:i.find('/')]] = i[i.find('/') + 1:]
		#print(hint_map)
		# Check if hint contains an expression
		for index, expr_word in enumerate(expr_words.keys()):
			if expr_word in hint_map:
				has_expression = True
		#print(self.hint_map)
		# Remove stop words from POS classifier
		hint_map_new = { k:v for k,v in hint_map.items() if v not in brown_stop_words}
		kb_return_map_key = "AND"
		kb_return_list = list()

		return_map = list() # list of AND JSON processed hints

		first_np = ''
		second_np = ''
		third_np = ''
		for word in new_hint_text:
			if (hint_map[word] == 'np' or  hint_map[word] == 'cd') and first_np == '': # and word in data_group
				first_np = word
			elif (hint_map[word] == 'np' or  hint_map[word] == 'cd') and second_np == '':
				second_np = word
			elif (hint_map[word] == 'np' or  hint_map[word] == 'cd') and third_np == '':
				third_np = word

		#print("first_np:", first_np)
		#print("second_np:", second_np)
		#print("third_np:", third_np)



		# Process ORs and append ORs
		# Hint contains OR when there are multiple (> 3) datagroup items mentioned in a hint. All of these
		# items must not be matched together

		# determine which datagroup entries are in the clue
		if third_np != '':
			or_map_list = list() # list of dicts for OR section of hint

			or_map_list.append(self._get_item_map(first_np))

			# relativly hard coded
			data_index_1 = self._get_item_index(third_np)
			data_group_1 = self._get_item_data_group(third_np)
			index_list_1 = [0,1,2,3]
			index_list_1.remove(data_index_1)
			or_map_list.append({"OR":  {data_group_1: index_list_1}})
			
			index_list_2 = [0,1,2,3]
			data_group_2 = self._get_item_data_group(second_np)
			for i in range(0, int(second_np)):
				#print(i)
				index_list_2.remove(i)

			
			or_map_list.append({"OR": {"Days": index_list_2}})



			# append OR clue to self.kb_rule_list
			self.kb_rule_list.append({"AND": or_map_list})

		# print(or_map_list)

		if has_expression:
			# Add first np to the 'AND' operation, second 'np' to the 'EXP'
			
			expr_map = dict()
			expr_map = self._get_item_map(third_np)
			#print(expr_map)
			num = [el for el, val in hint_map_new.items() if val == 'cd'][0]

			expr_map["NUM"] = num

			dg = [el for el, val in hint_map_new.items() if el in data_group_words][0]
			expr_map["DATAGROUP"] = dg

			op = [expr_words[el] for el, val in hint_map_new.items() if el in list(expr_words.keys())][0]
			expr_map["OP"] = op

			kb_return_list.append(self._get_item_map(first_np))
			kb_return_list.append({"EXPR" : expr_map})#self._process_expr(new_hint_text)})

			self.kb_rule_list.append({"AND": kb_return_list})


		# No EXPR in current hint
		else:
			for (k,v) in self.data_group.items():
				for word in hint_map_new:
					if word in v:
						d = dict()
						kb_return_list.append({k: v.index(word)})
			return_map.append({"AND": kb_return_list})

		# return appropriate KB map result
		
		
		return return_map

	def _get_item_map(self, item):
		'''
		This method returns the map of the item with the corresponding datagroup entry and value
		Ex. item: 'buttonwillow'
			return: {'Departures': 0 }

		Requires: The item to be an item in the datagroup arrays

		'''

		for (k,v) in self.data_group.items():
				for datagroup_item in v: 
					if datagroup_item == item:
						return ({k: v.index(datagroup_item)})

	def _get_item_index(self, item):

		for (k,v) in self.data_group.items():
				for datagroup_item in v: 
					if datagroup_item == item:
						return v.index(datagroup_item)

	def _get_item_data_group(self, item):
		for (k,v) in self.data_group.items():
				for datagroup_item in v: 
					if datagroup_item == item:
						return k

	# def _process_expr(self, new_hint_text):

	


	# def _process_or(self, hint_text):








