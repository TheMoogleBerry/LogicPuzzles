from puzzle import Puzzle

'''
Information for the {@param: data_group}: 
"Days" : [ "June 10", "June 11", "June 12", "June 13" ],
"Departures" : [ "Buttonwillow", "Coulterville", "Farley", "Leland" ],
"Names" : [ "Allen", "Chris", "Julio", "Luke" ]
'''

data_group = {"Days" : [ "10", "11", "12", "13" ], "Departures" : [ "Buttonwillow", "Coulterville", "Farley", "Leland" ], "Names" : [ "Allen", "Chris", "Julio", "Luke"] }
puzzle = Puzzle(data_group)
puzzle.process_hint('Luke/np is/bez scheduled/vbd to/in leave/vb on/in June/np 11/cd.')
puzzle.process_hint('The/at conductor/nn departing/vbg from/in Leland/np will/md leave/vb 1/cd day/nn after/in Chris/np')
#hint1 = Hint('The person departing from Buttonwillow will leave 2 days after Julio.')

'''
hint2 = Hint('The person working on June 11 is either the person departing from Coulterville or Allen.')
hint3 = Hint('The conductor departing from Leland will leave 1 day after Chris')
hint4 = Hint('Luke is scheduled to leave on June 11.')

hints = [hint1, hint2, hint3, hint4]
for hint in hints:
	hint.print_hint()
	'''