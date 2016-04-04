import itertools

DataGroup = {
    "Days" : [ "June 10", "June 11", "June 12", "June 13" ],
    "Departures" : [ "Buttonwillow", "Coulterville", "Farley", "Leland" ],
    "Names" : [ "Allen", "Chris", "Julio", "Luke" ]
}
# Function that returns if the string is a DataGroup
def isDataGroup(str):
    if str in list(DataGroup.keys()):
        return True
    return False

Propositions = ["AND", "OR", "XOR"]
# Function that returns if the string is a proposition
def isProposition(str):
    if str in Propositions:
        return True
    return False

# knowledge base for the solutions
kbSolutionPairs = {
    "Days" : "Names",
    "Departures" : "Days",
    "Names" : "Departures"
}
kbSolution = {
    "Days" : {
        0 : [0,1,2,3],
        1 : [0,1,2,3],
        2 : [0,1,2,3],
        3 : [0,1,2,3]
    },
    "Departures" : {
        0 : [0,1,2,3],
        1 : [0,1,2,3],
        2 : [0,1,2,3],
        3 : [0,1,2,3]
    },
    "Names" : {
        0 : [0,1,2,3],
        1 : [0,1,2,3],
        2 : [0,1,2,3],
        3 : [0,1,2,3]
    }
}
kbAllOptions = [0,1,2,3]

def printKbSolution():
    for key in kbSolution.keys():
        print(key + " : " + kbSolutionPairs[key])
        for val in kbSolution[key]:
            print(kbSolution[key][val])

def printSolutionWithNames():
    dg1 = list(kbSolutionPairs.keys())[0]
    for i in kbAllOptions:
        dg1Val = DataGroup[dg1][i]
        dg2 = kbSolutionPairs[dg1]
        dg2Key = kbSolution[dg1][i][0]
        dg2Val = DataGroup[dg2][dg2Key]
        dg3 = kbSolutionPairs[dg2]
        dg3Key = kbSolution[dg2][dg2Key][0]
        dg3Val = DataGroup[dg3][dg3Key]
        print(dg1 + ": " + dg1Val + ", " + dg2 + ": " + dg2Val + ", " + dg3 + ": " + dg3Val)


# knowledge base for the clues
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

completeUpdates = {}

def updateAfterConcreteConnection(dg1Key, dg1Val, dg2Key, dg2Val):
    if dg1Key not in completeUpdates.keys() or dg1Val not in completeUpdates[dg1Key]:
        # Remove value from others in DataGroup key value pair
        for i in range(len(kbAllOptions)):
            if i != dg1Val:
                if dg2Val in kbSolution[dg1Key][i]:
                    kbSolution[dg1Key][i].remove(dg2Val)
            
        # Propagate other connections
        dg3Key = kbSolutionPairs[dg2Key]    # other datagroup
        dg3Val = kbSolution[dg2Key][dg2Val] # value of other datagroup

        if len(dg3Val) == 1:
            kbSolution[dg3Key][dg3Val[0]] = [dg1Val]
        else:
            dg3NotVal = list(set(kbAllOptions) - set(dg3Val))
            for opt in dg3NotVal:
                if dg1Val in kbSolution[dg3Key][opt]:
                    kbSolution[dg3Key][opt].remove(dg1Val)

        for opt in kbSolution[dg3Key]:
            if dg1Val not in kbSolution[dg3Key][opt]:
                if opt in kbSolution[dg2Key][dg2Val]:
                    kbSolution[dg2Key][dg2Val].remove(opt)
    
        if dg1Key in completeUpdates.keys():
            completeUpdates[dg1Key].append(dg1Val)
        else:
            completeUpdates[dg1Key] = [dg1Val]

        
        updateAfterClue()

def updateAfterClue():
    complete = True
    for dg in kbSolution:
        numValues = [0] * len(kbAllOptions)
        for item in kbSolution[dg]:
            arr = kbSolution[dg][item]
            if len(arr) == 1:
                numValues[arr[0]] += 1
                updateAfterConcreteConnection(dg, item, kbSolutionPairs[dg], arr[0])
            else:
                for arrItem in arr:
                    numValues[arrItem] += 1
                complete = False
        for i in range(len(numValues)):
            if numValues[i] == 1:
                dgItem = 0
                for item in kbSolution[dg]:
                    if i in kbSolution[dg][item]:
                        dgItem = item
                handleDataGroupAndDataGroup(dg, dgItem, kbSolutionPairs[dg], i)
                updateAfterConcreteConnection(dg, dgItem, kbSolutionPairs[dg], i)
    return complete

def handleDataGroupAndDataGroup(dg1Key, dg1Val, dg2Key, dg2Val):
    if (kbSolutionPairs[dg1Key] == dg2Key):
        kbSolution[dg1Key][dg1Val] = [dg2Val]
                
    # Data Group is secondary key
    else:
        kbSolution[dg2Key][dg2Val] = [dg1Val]
    

def handleDataGroupAndProposition(dgKey, dgVal, propobj, prop):
    if prop == "OR":
        propkey = list(propobj.keys())[0] # Key for proposition
        proplist = propobj[propkey] # Value for proposition
                
        # DataGroup is main key
        if (kbSolutionPairs[dgKey] == propkey):
            listAnd = list(set(kbSolution[dgKey][dgVal]) & set(proplist))
            kbSolution[dgKey][dgVal] = listAnd
                    
        # Data Group is secondary key
        else:
            for val in list(set(kbAllOptions) - set(proplist)):
                if dgVal in kbSolution[propkey][val]:
                    kbSolution[propkey][val].remove(dgVal)
    elif prop == "XOR":
        # Removes xors
        for x in itertools.combinations(propobj, 2):
            obj1Key = list(x[0].keys())[0]
            obj1Val = x[0][obj1Key]
            obj2Key = list(x[1].keys())[0]
            obj2Val = x[1][obj2Key]
            if obj1Key != obj2Key:
                # DataGroup 1 is main key
                if kbSolutionPairs[obj1Key] == obj2Key:
                    if obj2Val in kbSolution[obj1Key][obj1Val]:
                        kbSolution[obj1Key][obj1Val].remove(obj2Val)
                # DataGroup 2 is main key
                else:
                    if obj1Val in kbSolution[obj2Key][obj2Val]:
                        kbSolution[obj2Key][obj2Val].remove(obj1Val)
        # Makes a concrete connection
        numconnections = 0
        xordg = ""
        xorval = 0
        for opt in propobj:
            optKey = list(opt.keys())[0]
            optVal = opt[optKey]
            # DataGroup 1 is main key
            if kbSolutionPairs[dgKey] ==optKey:
                if optVal in kbSolution[dgKey][dgVal]:
                    numconnections += 1
                    xordg = optKey
                    xorval = optVal
            # DataGroup 2 is main key
            else:
                if dgVal in kbSolution[optKey][optVal]:
                    numconnections += 1
                    xordg = optKey
                    xorval = optVal
        if numconnections == 1:
            if kbSolutionPairs[dgKey] == xordg:
                kbSolution[dgKey][dgVal] = [xorval]
            else:
                kbSolution[xordg][xorval] = [dgVal]

for i in range(len(kbClues) + 6):
    clue = kbClues[i%len(kbClues)]    # Full clue from the knowledge base
    prop = list(clue.keys())[0]     # Proposition that binds the clue
    stmnts = list(clue.values())[0] # List of statements in the clue
    for j in range(len(stmnts)):
        stmnt1 = stmnts[j]
        keyS1 = list(stmnt1.keys())[0] # Key for statement 1
        valueS1 = stmnt1[keyS1]
        
        for k in range(j + 1, len(stmnts)):
            stmnt2 = stmnts[k]
            keyS2 = list(stmnt2.keys())[0] # Key for statment 2
            
            # DataGroup and DataGroup
            if isDataGroup(keyS1) and isDataGroup(keyS2):
                handleDataGroupAndDataGroup(keyS1, valueS1, keyS2, stmnt2[keyS2])
                
            # DataGroup(s1) and Proposition(s2)
            elif isDataGroup(keyS1) and isProposition(keyS2):
                s2obj = stmnt2[keyS2] # Values in proposition
                handleDataGroupAndProposition(keyS1, valueS1, s2obj, keyS2)                    
                
            # DataGroup(s2) and Proposition(s1)
            elif isDataGroup(keyS2) and isProposition(keyS1):
                valueS2 = stmnt2[keyS2]
                handleDataGroupAndProposition(keyS2, valueS2, valueS1, keyS1)
                
            # DataGroupS1 and Expression
            elif isDataGroup(keyS1) and keyS2 == "EXPR":
                expr = stmnt2[keyS2]
                primaryDataGroupKey = ""
                for key in list(expr.keys()):
                    if isDataGroup(key):
                        primaryDataGroupKey = key
                primaryDataGroupVal = expr[primaryDataGroupKey]
                secondaryDataGroup = expr["DataGroup"]
                op = expr["OP"]
                num = expr["NUM"]
                if op == "PLUS":
                    proplist = list(range(len(kbAllOptions) - num))
                    propobj = { secondaryDataGroup : proplist }

                handleDataGroupAndProposition(primaryDataGroupKey, primaryDataGroupVal, propobj, "OR")
                
                # PrimaryDataGroup is main key
                if (kbSolutionPairs[primaryDataGroupKey] == secondaryDataGroup):
                    # Check if expression value is defined
                    if len(kbSolution[primaryDataGroupKey][primaryDataGroupVal]) == 1:
                        if op == "PLUS":
                            exprVal = kbSolution[primaryDataGroupKey][primaryDataGroupVal][0] + num
                        handleDataGroupAndDataGroup(keyS1, valueS1, secondaryDataGroup, exprVal)
                    
                # PrimaryDataGroup is secondary key   
                else:
                    numAppearances = 0
                    option = 0
                    for opt in kbAllOptions:
                        arr = kbSolution[secondaryDataGroup][opt]
                        if primaryDataGroupVal in arr and len(arr) == 1:
                            option = opt
                            numAppearances += 1
                    if numAppearances == 1:
                        if op == "PLUS":
                            exprVal = option + num
                        handleDataGroupAndDataGroup(keyS1, valueS1, secondaryDataGroup, exprVal)
                  
    if updateAfterClue():
        print(i)
        #print(clue)
        #printKbSolution()
        #print("\n")

        printSolutionWithNames()
        break
    # DataGroupS2 and Expression
    #print(clue)
    #printKbSolution()
    #print("\n") 
    
              
