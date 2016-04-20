import itertools

# Function that returns if the string is a DataGroup
def isDataGroup(str, datagroup):
    if str in list(datagroup.keys()):
        return True
    return False
    

# Function that returns if the string is a proposition
def isProposition(str):
    Propositions = ["AND", "OR", "XOR"]
    if str in Propositions:
        return True
    return False


class logicPuzzleSolver:
    kbClues = []
    DataGroup = {}
    kbSolutionPairs = {}
    kbAllOptions = []
    kbSolution = {}
    completeUpdates = {}

    def __init__(self, clues, groups):
        self.kbClues = clues
        self.DataGroup = groups
        datagroupkeys = list(self.DataGroup.keys())
        dgKeysLen = len(datagroupkeys)
        # Create all options for a knowledge base key
        for j in range(len(self.DataGroup[datagroupkeys[0]])):
            self.kbAllOptions.append(j)
        # Create solution pairs and knowledge base
        for i in range(dgKeysLen):
            key = datagroupkeys[i%dgKeysLen]
            value = datagroupkeys[(i+1)%dgKeysLen]
            self.kbSolutionPairs[key]=value
            self.kbSolution[key] = {}
            for j in range(len(self.kbAllOptions)):
                self.kbSolution[key][j] = list(range(len(self.kbAllOptions)))
              
		
    def printKbSolution(self):
        for key in self.kbSolution.keys():
            print(key + " : " + self.kbSolutionPairs[key])
            for val in self.kbSolution[key]:
                print(self.kbSolution[key][val])
				
    def printSolutionWithNames(self):
        dg1 = list(self.kbSolutionPairs.keys())[0]
        for i in self.kbAllOptions:
            dg1Val = self.DataGroup[dg1][i]
            dg2 = self.kbSolutionPairs[dg1]
            dg2Key = self.kbSolution[dg1][i][0]
            dg2Val = self.DataGroup[dg2][dg2Key]
            dg3 = self.kbSolutionPairs[dg2]
            dg3Key = self.kbSolution[dg2][dg2Key][0]
            dg3Val = self.DataGroup[dg3][dg3Key]
            print(dg1 + ": " + dg1Val + ", " + dg2 + ": " + dg2Val + ", " + dg3 + ": " + dg3Val)			
	
    def updateAfterClue(self):
        complete = True
        for dg in self.kbSolution:
            numValues = [0] * len(self.kbAllOptions)
            for item in self.kbSolution[dg]:
                arr = self.kbSolution[dg][item]
                if len(arr) == 1:
                    numValues[arr[0]] += 1
                    self.updateAfterConcreteConnection(dg, item, self.kbSolutionPairs[dg], arr[0])
                else:
                    for arrItem in arr:
                        numValues[arrItem] += 1
                    complete = False
            for i in range(len(numValues)):
                if numValues[i] == 1:
                    dgItem = 0
                    for item in self.kbSolution[dg]:
                        if i in self.kbSolution[dg][item]:
                            dgItem = item
                    self.handleDataGroupAndDataGroup(dg, dgItem, self.kbSolutionPairs[dg], i)
                    self.updateAfterConcreteConnection(dg, dgItem, self.kbSolutionPairs[dg], i)
        return complete
	
    def updateAfterConcreteConnection(self, dg1Key, dg1Val, dg2Key, dg2Val):
        if dg1Key not in self.completeUpdates.keys() or dg1Val not in self.completeUpdates[dg1Key]:
            # Remove value from others in DataGroup key value pair
            for i in range(len(self.kbAllOptions)):
                if i != dg1Val:
                    if dg2Val in self.kbSolution[dg1Key][i]:
                        self.kbSolution[dg1Key][i].remove(dg2Val)
				
            # Propagate other connections
            dg3Key = self.kbSolutionPairs[dg2Key]    # other datagroup
            dg3Val = self.kbSolution[dg2Key][dg2Val] # value of other datagroup

            if len(dg3Val) == 1:
                self.kbSolution[dg3Key][dg3Val[0]] = [dg1Val]
            else:
                dg3NotVal = list(set(self.kbAllOptions) - set(dg3Val))
                for opt in dg3NotVal:
                    if dg1Val in self.kbSolution[dg3Key][opt]:
                        self.kbSolution[dg3Key][opt].remove(dg1Val)

            for opt in self.kbSolution[dg3Key]:
                if dg1Val not in self.kbSolution[dg3Key][opt]:
                    if opt in self.kbSolution[dg2Key][dg2Val]:
                        self.kbSolution[dg2Key][dg2Val].remove(opt)
		
            if dg1Key in self.completeUpdates.keys():
                self.completeUpdates[dg1Key].append(dg1Val)
            else:
                self.completeUpdates[dg1Key] = [dg1Val]

			
            self.updateAfterClue()			
			
    def handleDataGroupAndProposition(self, dgKey, dgVal, propobj, prop):
        if prop == "OR":
            propkey = list(propobj.keys())[0] # Key for proposition
            proplist = propobj[propkey] # Value for proposition
                    
            # DataGroup is main key
            if (self.kbSolutionPairs[dgKey] == propkey):
                listAnd = list(set(self.kbSolution[dgKey][dgVal]) & set(proplist))
                self.kbSolution[dgKey][dgVal] = listAnd
						
            # Data Group is secondary key
            else:
                for val in list(set(self.kbAllOptions) - set(proplist)):
                    if dgVal in self.kbSolution[propkey][val]:
                        self.kbSolution[propkey][val].remove(dgVal)
        elif prop == "XOR":
            # Removes xors
            for x in itertools.combinations(propobj, 2):
                obj1Key = list(x[0].keys())[0]
                obj1Val = x[0][obj1Key]
                obj2Key = list(x[1].keys())[0]
                obj2Val = x[1][obj2Key]
                if obj1Key != obj2Key:
                    # DataGroup 1 is main key
                    if self.kbSolutionPairs[obj1Key] == obj2Key:
                        if obj2Val in self.kbSolution[obj1Key][obj1Val]:
                            self.kbSolution[obj1Key][obj1Val].remove(obj2Val)
                    # DataGroup 2 is main key
                    else:
                        if obj1Val in self.kbSolution[obj2Key][obj2Val]:
                            self.kbSolution[obj2Key][obj2Val].remove(obj1Val)
            # Makes a concrete connection
            numconnections = 0
            xordg = ""
            xorval = 0
            for opt in propobj:
                optKey = list(opt.keys())[0]
                optVal = opt[optKey]
                # DataGroup 1 is main key
                if self.kbSolutionPairs[dgKey] ==optKey:
                    if optVal in self.kbSolution[dgKey][dgVal]:
                        numconnections += 1
                        xordg = optKey
                        xorval = optVal
                # DataGroup 2 is main key
                else:
                    if dgVal in self.kbSolution[optKey][optVal]:
                        numconnections += 1
                        xordg = optKey
                        xorval = optVal
            if numconnections == 1:
                if self.kbSolutionPairs[dgKey] == xordg:
                    self.kbSolution[dgKey][dgVal] = [xorval]
                else:
                    self.kbSolution[xordg][xorval] = [dgVal]
				
    def handleDataGroupAndDataGroup(self, dg1Key, dg1Val, dg2Key, dg2Val):
        if (self.kbSolutionPairs[dg1Key] == dg2Key):
            self.kbSolution[dg1Key][dg1Val] = [dg2Val]
                
        # Data Group is secondary key
        else:
            self.kbSolution[dg2Key][dg2Val] = [dg1Val]
     
    def handleDataGroupAndExpressions(self, keyS1, valueS1, exprKey, exprVal, exprDg, op, num):
        if keyS1 != exprKey:
            if (self.kbSolutionPairs[keyS1] == exprKey):
                if exprVal in self.kbSolution[keyS1][valueS1]:
                    self.kbSolution[keyS1][valueS1].remove(exprVal)
            else:
                if valueS1 in self.kbSolution[exprKey][exprVal]:
                    self.kbSolution[exprKey][exprVal].remove(valueS1)
        
        if op == "PLUS":
            proplist = list(range(len(self.kbAllOptions) - num))
            proplist1 = [x+num for x in proplist]
            propobj = { exprDg : proplist1 }
            propobj2 = { exprDg : proplist }
            
        elif op == "SUBTRACT":
            proplist = list(range(len(self.kbAllOptions) - num))
            proplist1 = [x+num for x in proplist]
            propobj = { exprDg : proplist }
            propobj2 = { exprDg : proplist1 }
        self.handleDataGroupAndProposition(keyS1, valueS1, propobj, "OR")
        self.handleDataGroupAndProposition(exprKey, exprVal, propobj2, "OR")
        
        # PrimaryDataGroup is main key
        if (self.kbSolutionPairs[exprKey] == exprDg):
            # Check if expression value is defined
            if len(self.kbSolution[exprKey][exprVal]) == 1:
                if op == "PLUS":
                    exprVal = self.kbSolution[exprKey][exprVal][0] + num
                elif op == "SUBTRACT":
                    exprVal = self.kbSolution[exprKey][exprVal][0] - num
                self.handleDataGroupAndDataGroup(keyS1, valueS1, exprDg, exprVal)
            
        # PrimaryDataGroup is secondary key   
        else:
            numAppearances = 0
            option = 0
            for opt in self.kbAllOptions:
                arr = self.kbSolution[exprDg][opt]
                if exprVal in arr and len(arr) == 1:
                    option = opt
                    numAppearances += 1
            if numAppearances == 1:
                if op == "PLUS":
                    exprVal = option + num
                elif op == "SUBTRACT":
                    exprVal = option - num
                self.handleDataGroupAndDataGroup(keyS1, valueS1, exprDg, exprVal)
    
     
    def solvePuzzle(self):
        for i in range(len(self.kbClues) * 4):
            clue = self.kbClues[i%len(self.kbClues)]    # Full clue from the knowledge base
            prop = list(clue.keys())[0]     # Proposition that binds the clue
            stmnts = list(clue.values())[0] # List of statements in the clue
            if prop == "AND":    
                for j in range(len(stmnts)):
                    stmnt1 = stmnts[j]
                    keyS1 = list(stmnt1.keys())[0] # Key for statement 1
                    valueS1 = stmnt1[keyS1]
                    
                    for k in range(j + 1, len(stmnts)):
                        stmnt2 = stmnts[k]
                        keyS2 = list(stmnt2.keys())[0] # Key for statment 2

                        # DataGroup and DataGroup
                        if isDataGroup(keyS1, self.DataGroup) and isDataGroup(keyS2, self.DataGroup):
                            self.handleDataGroupAndDataGroup(keyS1, valueS1, keyS2, stmnt2[keyS2])
                            
                        # DataGroup(s1) and Proposition(s2)
                        elif isDataGroup(keyS1, self.DataGroup) and isProposition(keyS2):
                            s2obj = stmnt2[keyS2] # Values in proposition
                            self.handleDataGroupAndProposition(keyS1, valueS1, s2obj, keyS2)                    
                            
                        # DataGroup(s2) and Proposition(s1)
                        elif isDataGroup(keyS2, self.DataGroup) and isProposition(keyS1):
                            valueS2 = stmnt2[keyS2]
                            self.handleDataGroupAndProposition(keyS2, valueS2, valueS1, keyS1)
                        
                        # DataGroupS1 and Expression
                        elif isDataGroup(keyS1, self.DataGroup) and keyS2 == "EXPR":
                            expr = stmnt2[keyS2]
                            exprKey = ""
                            for key in list(expr.keys()):
                                if isDataGroup(key, self.DataGroup):
                                    exprKey = key
                            exprVal = expr[exprKey]
                            exprDg = expr["DataGroup"]
                            op = expr["OP"]
                            op2 = ""
                            if op == "PLUS":
                                op2 = "SUBTRACT"
                            else:
                                op2 = "PLUS"
                            num = expr["NUM"]
                            self.handleDataGroupAndExpressions(keyS1, valueS1, exprKey, exprVal, exprDg, op, num)
                            self.handleDataGroupAndExpressions(exprKey, exprVal, keyS1, valueS1, exprDg, op2, num)
 
            
            elif prop == "XOR":
                for j in range(len(stmnts)):
                    stmnt1 = stmnts[j]
                    keyS1 = list(stmnt1.keys())[0] # Key for statement 1
                    valueS1 = stmnt1[keyS1]
                    
                    for k in range(j + 1, len(stmnts)):
                        stmnt2 = stmnts[k]
                        keyS2 = list(stmnt2.keys())[0] # Key for statment 2
                        valueS2 = stmnt2[keyS2]
                        if keyS2 != keyS1:
                            if (self.kbSolutionPairs[keyS1] == keyS2):
                                if valueS2 in self.kbSolution[keyS1][valueS1]:
                                    self.kbSolution[keyS1][valueS1].remove(valueS2)
                            else:
                                if valueS1 in self.kbSolution[keyS2][valueS2]:
                                    self.kbSolution[keyS2][valueS2].remove(valueS1)
                        
            if self.updateAfterClue():
                print("Number of clues read in: ", len(self.kbClues))
                print("Number of clues to solve: ",i)
                print("Number of iterations through clues: ", i/len(self.kbClues))
                #print(clue)
                
                print("")

                print("Solution:")
                self.printSolutionWithNames()
                break
            # DataGroupS2 and Expression
            #print(clue)
            #self.printKbSolution()
            #print("\n") 
