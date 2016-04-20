from logicPuzzleSolver import logicPuzzleSolver
import sys
import pos_classifier as pos

def main(corpus):
    """kbClues = [
        {
            "AND" : [
                { "Departures" : 0 },
                { "OR" : { "Days" : [2,3] } },
                { "OR" : { "Names" : [0,1,3] } }
            ]
        },
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
                { "OR" : { "Days" : [1,2,3] } },
                { "OR" : { "Names" : [0,2,3] } }
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

    kbClues = [
        {
            "AND" : [
                { "Winners" : 2 },
                { "Winnings" : 1 }
            ]
        },
        {
            "AND" : [
                { "Winners" : 0 },
                { "EXPR" : {
                    "States" : 1,
                    "DataGroup" : "Winnings",
                    "OP" : "PLUS",
                    "NUM" : 1
                    }
                }
            ]
        },
        {
            "AND" : [
                { "Winnings" : 1 },
                { "States" : 3 }
            ]
        },
        {
            "XOR" : [
                { "States" : 1 },
                { "Winners" : 2 },
                { "Winners" : 1 }
            ]
        },
        {
            "AND" : [
                { "States" : 1 },
                { "EXPR" : {
                    "States" : 0,
                    "DataGroup" : "Winnings",
                    "OP" : "PLUS",
                    "NUM" : 2
                    }
                }
            ]
        }
    ]
    datagroup = {
        "Winnings" : [ "$5 million", "$10 million", "$15 million", "$20 million" ],
        "Winners" : [ "Cal Chandler", "Dharma Day", "Ed Elliot", "Ferris Fry" ],
        "States" : [ "Georgia", "Pennsylvania", "Vermont", "Washington" ]
    }
    """
    kbClues = [
		{
            "AND" : [
                { "Islands" : 0 },
                { "EXPR" : {
                    "Resorts" : 3,
                    "DataGroup" : "Prices",
                    "OP" : "PLUS",
                    "NUM" : 1
                    }
                }
            ]
        },
        {
            "AND" : [
                { "Resorts" : 1 },
                { "Islands" : 2 }
            ]
        },
		{
            "AND" : [
                { "Resorts" : 1 },
                { "EXPR" : {
                    "Islands" : 0,
                    "DataGroup" : "Prices",
                    "OP" : "PLUS",
                    "NUM" : 2
                    }
                }
            ]
        },
        {
            "AND" : [
                { "Resorts" : 2 },
                { "Islands" : 3 }
            ]
        },

    ]

    datagroup = {
        "Prices" : [ "$175", "$195", "$215", "$235" ],
        "Resorts" : [ "Azure Hills", "El Pacifico", "Emerald View", "Silver Harbor" ],
        "Islands" : [ "Anguilla", "Barbados", "St. Martin", "St. Barts" ]
    }
    classifier = pos.POSClassifier()
    taggest_body = classifier.classify(corpus)
    print(taggest_body)

    lps = logicPuzzleSolver(kbClues, datagroup)
    lps.solvePuzzle()

logic_corpus = input("Enter the Puzzle's body of text :")
main(logic_corpus)
