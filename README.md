# LogicPuzzles
CSE 5522: AI Game Group Project

Contributors: Andrew Motika, Johnny Mercado, Samuel Rosenstein

Structure of the project:

 ---------------      ----------------------      ----------------------
|POS Classifier | -> | Puzzle Hint Processor| -> | Knowlegebase Solver |
 ---------------      ----------------------      ----------------------

### POS Classifier

### Puzzle Hint Processor
Contains one class: Puzzle
Implements the following method:
```process_hint(hint_text)``

Once initialize, an object of the Puzzle class can process hints that contain classification tags from the POS Classifier. In order to initialize a Puzzle object, pass the data_group as a parameter. The data_group must be in the form of a map of arrays where each key is a data group field title and the array are the possible solution values for that data group field.
The ```process_hint`` method creates the necessary JSONified hints and then appends them to the object attribute 'kb_rule_list'. Thus, in order to return all KB rules that have been created from the processed hints, first call ```process_hint`` for each hint and then get the 'kb_rule_list' attribute from the object.

Example code to use the Puzzle object:
```python

# Information for the {@param: data_group}: 
data_group = {"Days" : [ "10", "11", "12", "13" ], "Departures" : [ "buttonwillow", "coulterville", "farley", "leland" ], "Names" : [ "allen", "chris", "julio", "luke"] }
puzzle = Puzzle(data_group)

# process first hint
puzzle.process_hint('The/at person/nn departing/vbg from/in Buttonwillow/np will/md leave/vb 2/cd days/nn after/cs Julio/np.')

# print current KB list for the puzzle object after processing first hint
print(puzzle.kb_rule_list )
``

### Knowlegebase Solver


