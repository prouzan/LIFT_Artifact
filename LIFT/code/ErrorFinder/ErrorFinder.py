from enum import Enum
import os
import sys
sys.path.append(os.path.abspath('code'))
from StateTrans import TraceStateTrans  #pylint: disable=import-error
from StateTrans.TraceStateTrans import * #pylint: disable=import-error

class ErrorFinder:
    class State:

        LabelType = Enum('LabelType', ('Positive', 'Negative', 'Unknown'))

        def __init__(self, id, label, values):
            self.id = id
            self.label = label
            self.values = values
            self.next = []

        def addNext(self, id):
            self.next.append(id)

    Suffix_Data = '.data'
    Suffix_Names = '.names'
    Suffix_Implications = '.implications'


    @staticmethod
    def simpCounterexample(logger, path2bpl, inputVars, simpError, firstLoop='b0'):
        nameList = []
        nameListLen = 0
        testNames = {}
        with open(path2bpl + ErrorFinder.Suffix_Names) as NamesReader:
            NamesReaderLines = NamesReader.readlines()
            for line in NamesReaderLines:
                if line.replace('\n','').replace('\r','') == '':
                    continue
                if 'continuous.' in line:
                    varName = line.split(':')[0]
                    nameList.append(varName)
                    nameListLen += 1
                    splitResult = varName.split('$')
                    loopName = splitResult[0]
                    trueName = splitResult[1]
                    if loopName == firstLoop and trueName in inputVars:
                        testNames[varName] = trueName
        valueDict = {}
        for idx in range(nameListLen):
            if nameList[idx] in testNames.keys():
                valueDict[testNames[nameList[idx]]] = int(simpError[idx].replace(' ',''))
        
        return [(valueDict, 1)]

    @staticmethod
    def load(logger, path2bpl, inputVars, firstLoop='b0', tracePrefix='TR'):
        nameList = []
        nameListId = 0
        testNames = {}
        with open(path2bpl + ErrorFinder.Suffix_Names) as NamesReader:
            NamesReaderLines = NamesReader.readlines()
            for line in NamesReaderLines:
                if line.replace('\n','').replace('\r','') == '':
                    continue
                if 'continuous.' in line:
                    varName = line.split(':')[0]
                    nameList.append(varName)
                    nameListId += 1
                    splitResult = varName.split('$')
                    loopName = splitResult[0]
                    trueName = splitResult[1]
                    if loopName == firstLoop and trueName in inputVars:
                        testNames[varName] = trueName
                    elif loopName == firstLoop and tracePrefix != None and trueName.startswith(tracePrefix):
                        testNames[varName] = trueName

        dataList = []
        with open(path2bpl + ErrorFinder.Suffix_Data) as DataReader:
            DataReaderLines = DataReader.readlines()
            lineId = 0
            for line in DataReaderLines:
                line = line.replace('\n','').replace('\r','')
                if line == '':
                    continue
                terms = line.split(',')
                values = []
                datalabel = None
                for i in range(len(terms)):
                    if i == 0:
                        continue
                    term = terms[i]
                    if i != len(terms) - 1: # mid data column
                        if (term == '' or term == '?'):
                            values.append(None)
                        else:
                            values.append(int(term))
                    else:
                        if term == 'true':
                            datalabel = ErrorFinder.State.LabelType.Positive
                        elif term == 'false':
                            datalabel = ErrorFinder.State.LabelType.Negative
                        elif term == '?':
                            datalabel = ErrorFinder.State.LabelType.Unknown
                dataList.append(ErrorFinder.State(lineId, datalabel, values))
                lineId += 1
        with open(path2bpl + ErrorFinder.Suffix_Implications) as ImplicationsReader:
            ImplicationsReaderLines = ImplicationsReader.readlines()
            for line in ImplicationsReaderLines:
                line = line.replace('\n','').replace('\r','')
                if line == '':
                    continue
                ids = list(map(int, line.split(' ')))
                dataList[ids[0]].addNext(dataList[ids[1]])
        return ErrorFinder(logger, dataList, nameList, testNames, inputVars)


    def __init__(self, logger, stateList, nameList, testNames, inputVars): # testName is a dict to true name
        self.Logger = logger
        self.States = stateList
        self.Names = nameList
        self.TestNames = testNames
        self.InputVars = inputVars
        
    def checkDFS(self, state, trace = []):
        if state.label == ErrorFinder.State.LabelType.Negative:
            return [trace + [state]]
        traceList = []
        for node in state.next:
            traceList += self.checkDFS(node, trace + [state])
        return traceList
        
    def check(self):
        traceList = []
        for item in self.States:
            if item.label == ErrorFinder.State.LabelType.Positive:
                traceList += self.checkDFS(item)
        return traceList        

    def getErrorInput(self):
        traceList = self.check()

        errorList = []
        for trace in traceList:
            valueDict = {}
            for nameId in range(len(self.Names)):
                name = self.Names[nameId]
                if name in self.TestNames.keys():
                    valueDict[self.TestNames[name]] = trace[0].values[nameId] # pylint: disable=no-member
            errorList.append((valueDict, len(trace)))
            #self.Logger.Log('[Debug] Error {}\nTrace: {}'.format(errorList[-1],list(map(lambda x:x.values, trace))))
        return errorList


    def getErrorInputLexicalTr(self, tracePrefix='TR', labelPrefix='L'):
        traceList = self.check()
        errorInputList = []
        RTraceList = []
        for trace in traceList:
            # import pdb; pdb.set_trace()
            firstState = True
            Tr = TraceStates(self.InputVars) # pylint: disable=undefined-variable
            for state in trace:
                RState, RTrace = self.getLexicalStateAndTrace(state, tracePrefix, labelPrefix)

                if firstState:
                    Tr.appendInitState(RState)
                    errorInputList.append(RState)
                    firstState = False
                else:
                    Tr.appendNextState(RState, RTrace)
            RTraceList.append(Tr)
        errorInputList = list(set(errorInputList))
        return errorInputList, RTraceList

    def getErrorInputLexical(self, tracePrefix='TR', labelPrefix='L', option='default'):
        if option == 'trace':
            return self.getErrorInputLexicalTr(tracePrefix, labelPrefix)
        traceList = self.check()
        errorInputList = []
        transList = []

        for trace in traceList:
            lastRState = None
            for state in trace:
                RState, RTrace = self.getLexicalStateAndTrace(state, tracePrefix, labelPrefix)
                if lastRState != None:
                    trans = TraceStateTrans(lastRState, RState, RTrace, self.InputVars)
                    transList.append(trans)
                else:
                    errorInputList.append(RState)
                lastRState = RState
        errorInputList = list(set(errorInputList))
        # transList = list(set(transList))
        return errorInputList, transList


    
    def getLexicalStateAndTrace(self, state, tracePrefix='TR', labelPrefix='L'):
        RState = []
        # print(self.TestNames)
        # print(self.Names)
        # print(state.values)
        for varName in self.InputVars:
            for nameId in range(len(self.Names)):
                name = self.Names[nameId]
                if name in self.TestNames.keys() and self.TestNames[name] == varName:
                    RState.append(state.values[nameId])
                    break
                elif nameId == len(self.Names) - 1:
                    raise RuntimeError('Test varname {} not found!'.format(varName))
        
        RTrace = []
        TRid = 0
        flagEnd = False
        while True:
            TRid += 1
            if flagEnd:
                break
            TRstr = tracePrefix + '{}'.format(TRid)
            Lstr = labelPrefix + '{}'.format(TRid)

            for nameId in range(len(self.Names)):
                name = self.Names[nameId]
                if name in self.TestNames.keys() and self.TestNames[name] == TRstr:
                    if state.values[nameId] == 1:
                        # print("AA")
                        RTrace.append(Lstr)
                    break
                elif nameId == len(self.Names) - 1:
                    flagEnd = True
        return tuple(RState), tuple(RTrace)


