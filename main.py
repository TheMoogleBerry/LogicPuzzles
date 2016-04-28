from logicPuzzleSolver import logicPuzzleSolver
import sys
import pos_classifier as pos
import puzzle

def request_clues():
    clues = []
    another = True
    while another:
        clue = input("Enter a clue: ")
        clues.append(clue)
        another = input("Would you like to enter another clue(Y/N)? ") == 'Y'
    return(clues)

def main(clues):
    kbClues = [
        {
            "AND" : [
                { "Departures" : 0 },
                { "EXPR" : {
                    "Names" : 2,
                    "DataGroup" : "Days",
                    "OP" : "PLUS",
                    "NUM" : 2
                    }
                }
            ]
        },
        {
            "AND" : [
                { "Days" : 1 },
                { "XOR" : [
                    { "Departures" : 1 },
                    { "Names" : 0 }
                    ]
                }
            ]
        },
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
        {
            "AND" : [
                { "Names" : 3 },
                { "Days" : 1 }
            ]
        }
    ]

    datagroup = {
        "Days" : [ "June 10", "June 11", "June 12", "June 13" ],
        "Departures" : [ "Buttonwillow", "Coulterville", "Farley", "Leland" ],
        "Names" : [ "Allen", "Chris", "Julio", "Luke" ]
    }
    kbData = []
    mapper = puzzle.Puzzle(datagroup)
    for clue in clues:
        classifier = pos.POSClassifier()
        tagged_clue = classifier.classify(clue)
        print(tagged_clue)
        mapped_hint = mapper.process_hint(tagged_clue)
        print(mapped_hint)
        kbData.append(tagged_clue)

    lps = logicPuzzleSolver(kbClues, datagroup)
    lps.solvePuzzle()

user_clues = request_clues()
main(user_clues)
