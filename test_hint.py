from puzzle import Puzzle

'''
Information for the {@param: data_group}: 
"Days" : [ "June 10", "June 11", "June 12", "June 13" ],
"Departures" : [ "uttonwillow", "Coulterville", "Farley", "Leland" ],
"Names" : [ "Allen", "Chris", "Julio", "Luke" ]
'''

data_group = {"Days" : [ "10", "11", "12", "13" ], "Departures" : [ "buttonwillow", "coulterville", "farley", "leland" ], "Names" : [ "allen", "chris", "julio", "luke"] }
puzzle = Puzzle(data_group)
# puzzle.process_hint('The/at person/nn departing/vbg from/in Buttonwillow/np will/md leave/vb 2/cd days/nn after/cs Julio/np.')
# puzzle.process_hint('Luke/np is/bez scheduled/vbd to/in leave/vb on/in June/np 11/cd.')
# puzzle.process_hint('The/at person/nn working/vbg on/in June/np 11/cd is/is either/cc the/at person/nn departing/vbg from/in Coulterville/np or/in Allen/np.')
puzzle.process_hint('The/at conductor/nn departing/vbg from/in Leland/np will/md leave/vb 1/cd day/nn after/cs Chris/np')
print(puzzle.kb_rule_list )
# print(puzzle.process_hint('The/at conductor/nn departing/vbg from/in Leland/np will/md leave/vb 1/cd day/nn after/cs Chris/np'))
# hint1 = Hint('The person departing from Buttonwillow will leave 2 days after Julio.')


def test_process_hint_puzzle_one(puzzle, num_tests = 4):
	print(puzzle.process_hint('The/at person/nn departing/vbg from/in Buttonwillow/np will/md leave/vb 2/cd days/nn after/cs Julio/np.'))
	#print(puzzle.process_hint('Luke/np is/bez scheduled/vbd to/in leave/vb on/in June/np 11/cd.'))
	#print(puzzle.process_hint('The/at conductor/nn departing/vbg from/in Leland/np will/md leave/vb 1/cd day/nn after/cs Chris/np'))




