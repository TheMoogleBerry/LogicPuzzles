from logicPuzzleSolver import logicPuzzleSolver

def main():
    kbClues = [
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
    
    lps = logicPuzzleSolver(kbClues, datagroup)
    lps.solvePuzzle()
				
main()
