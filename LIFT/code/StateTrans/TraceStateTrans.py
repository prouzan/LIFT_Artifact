
class TraceStateTrans:
    def __init__(self, beginState, endState, trace, varList):
        ...
        self.Begin = tuple(beginState)
        self.End = tuple(endState)
        self.Trace = tuple(trace)
        self.Vars = tuple(varList)

    def __str__(self):
        return 'TR{}={}=>{}'.format(self.Begin, self.Trace, self.End)
    
    # 'appendC' * Const + A * X >= 'appendValue'
    def getMDataTerm(self, appendValue = 1, appendC = 0):
        data = []
        if appendC != None:
            data.append(appendC)
        for i in range(len(self.Vars)):
            data.append(self.Begin[i] - self.End[i])
        if appendValue != None:
            data.append(appendValue)
        return tuple(data)

    def __hash__(self):
        return hash((hash(self.Begin),
            hash(self.End),
            hash(self.Trace),
            hash(self.Vars)))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.Begin == other.Begin and \
                        self.End == other.End and \
                            self.Trace == other.Trace and \
                                self.Vars == other.Vars 
        else:
            return False      

    @staticmethod
    def TestDataP2mData(dataList, appendRName = 'r', appendValue = 1, appendC = 1):
        if len(dataList) == 0:
            raise RuntimeError("No data when transform to mData")
        # No check to reduce the time
        title = list(dataList[0].Vars)
        if appendRName != None:
            title = title + [appendRName]
        if appendC != None:
            title = ['1'] + title
        title = tuple(title)
        AllState = []
        for it in dataList:
            AllState.append(tuple([appendC] + list(it.Begin) + [appendValue]))
            AllState.append(tuple([appendC] + list(it.End) + [appendValue]))
        return (title, AllState)

    @staticmethod
    def TestDataTR2mDataDict(dataList, appendRName = 'r', appendValue = 1, appendC = 0):
        if len(dataList) == 0:
            raise RuntimeError("No data when transform to mData")
        # No check to reduce the time
        title = list(dataList[0].Vars)
        if appendRName != None:
            title = title + [appendRName]
        if appendC != None:
            title = ['1'] + title
        title = tuple(title)
        mDataDict = {}
        for it in dataList:
            if it.Trace not in mDataDict.keys():
                mDataDict[it.Trace] = (title, [])
            mDataDict[it.Trace][1].append(it.getMDataTerm(appendValue, appendC))
        for k in mDataDict.keys():
            mDataDict[k] = (mDataDict[k][0], list(set(mDataDict[k][1])))
        return mDataDict

    @staticmethod
    def TestResult2DataV3_0(testLines, varList, logger = None):
        data = []
        lastState = None
        trace = []
        TDataInfo = []
        for line in testLines:
            # print(line)
            replaceEmpty = line.replace(' ','').replace('\n','').replace('\r','').replace('\t','')
            if replaceEmpty == '':
                continue
            if replaceEmpty.startswith('[Testing]'):
                continue
            if line.startswith('L'):
                label = replaceEmpty
                trace.append(label)
            else:
                state = list(map(int, replaceEmpty.split(',')))
                if lastState != None:
                    data.append(TraceStateTrans(lastState, state, list(trace),varList))
                lastState = state
                trace = []
                if logger != None:
                    TDataInfo.append(dict())
                    for i in range(len(varList)):
                        TDataInfo[-1][varList[i]] = state[i]
                        i += 1
        if logger != None:
            logger.TestDataInfo.append(TDataInfo)
        return data

class TraceStates:
    def __init__(self, varList):
        self.VarList = varList
        self.States = []
        self.Traces = []
        self.Knowledge = {}

    def __str__(self):
        s = 'Var:{}\n'.format(self.VarList)
        for i in range(len(self.Traces)):
            s += '{} ={}=> '.format(self.States[i], self.Traces[i])
        s += '{}'.format(self.States[-1])
        return s
    @property
    def LoopIt(self):
        return len(self.Traces)

    def appendInitState(self, s):
        self.States = [tuple(s)]
        self.Traces = []

    def appendNextState(self, s, t):
        if type(t) == type(None):
            self.appendInitState(s)
            return
        self.States.append(tuple(s))
        self.Traces.append(tuple(t))

    @staticmethod
    def TestResult2TraceV4_0(testLines, varList):
        ts = TraceStates(varList)
        varDictList = []
        trace = None
        for line in testLines:
            replaceEmpty = line.replace(' ','').replace('\n','').replace('\r','').replace('\t','')
            if replaceEmpty == '':
                continue
            if replaceEmpty.startswith('[Testing]'):
                continue
            if line.startswith('L'):
                label = replaceEmpty
                trace.append(label)
            else:
                varInfo = replaceEmpty.split(',')
                varInfoDict = {}
                for item in varInfo:
                    varName, varValue = item.split(':')
                    varInfoDict[varName] = int(varValue)
                state = []
                for varName in varList:
                    state.append(varInfoDict[varName])
                ts.appendNextState(state, trace)
                varInfoDict['TR'] = trace
                varDictList.append(varInfoDict)
                trace = []
        return ts, varDictList

    @staticmethod
    def TestResult2V4_0(testLines, varList, randTester):
        dataList = []
        varDictList = []
        for line in testLines:
            replaceEmpty = line.replace(' ','').replace('\n','').replace('\r','').replace('\t','')
            if replaceEmpty == '':
                continue
            if replaceEmpty.startswith('[Testing]'):
                continue
            
            varInfo = replaceEmpty.split(',')
            varInfoDict = {}
            for item in varInfo:
                varName, varValue = item.split(':')
                varInfoDict[varName] = int(varValue)
            state = []
            for varName in varList:
                state.append(varInfoDict[varName])
            dataList.append(state)
            varDictList.append(varInfoDict)
        for i in range(len(dataList)):
            dataList[i].append(len(dataList) - i)
        
        # Set Maximun number of samples in one test, making the sample number not too large
        dataTraceLen = len(dataList)
        if dataTraceLen > randTester.MAX_SAMPLE_ONCE and randTester.MAX_SAMPLE_ONCE != 0:
            SampleDistance = dataTraceLen // randTester.MAX_SAMPLE_ONCE

            SelectedDataTrace = []
            for it in range(dataTraceLen):
                if it % SampleDistance == 0:
                    SelectedDataTrace.append(dataList[it])
            return SelectedDataTrace, varDictList
            
        return dataList, varDictList


    @staticmethod
    def TestResult2TraceV3_0(testLines, varList):
        ts = TraceStates(varList)
        trace = None
        for line in testLines:
            # print(line)
            replaceEmpty = line.replace(' ','').replace('\n','').replace('\r','').replace('\t','')
            if replaceEmpty == '':
                continue
            if replaceEmpty.startswith('[Testing]'):
                continue
            if line.startswith('L'):
                label = replaceEmpty
                trace.append(label)
            else:
                if line.startswith('#'):
                    state = []
                else:
                    state = list(map(int, replaceEmpty.split(',')))
                ts.appendNextState(state, trace)
                trace = []
        return ts

    # ranks is a tuple of several sets containing trace (tuple style) in iteration
    def GenerateMData4Dims(self, ranks, appendRName = 'r'):
        knowledgeKey = list(ranks)
        for rk in range(len(knowledgeKey)):
            hashedItem = list(knowledgeKey[rk])
            hashedItem.sort()
            hashedItem = tuple(hashedItem)
            knowledgeKey[rk] = hashedItem

        # knowledgeKey.sort()
        knowledgeKey = tuple(knowledgeKey)
        if knowledgeKey in self.Knowledge.keys():
            return self.Knowledge[knowledgeKey]
        DimsValue = []
        for _ in range(self.LoopIt + 1):
            DimsValue.append([])
        DimsValue[self.LoopIt] = [1] * len(ranks)
        for idx in range(self.LoopIt - 1, -1 , -1):
            tr = self.Traces[idx]
            rankDim = 0
            while tr not in ranks[rankDim]: # Copy
                DimsValue[idx].append(DimsValue[idx+1][rankDim])
                rankDim += 1
            DimsValue[idx].append(DimsValue[idx+1][rankDim]+1) # Dim + 1
            rankDim += 1
            while rankDim < len(ranks):
                DimsValue[idx].append(1) # Set 1
                rankDim += 1

        DimsMData = []
        for rankId in range(len(ranks)):
            DimsMData.append((tuple(self.VarList + [appendRName]), []))
            for stateId in range(len(DimsValue)):
                DimsMData[rankId][1].append(tuple(list(self.States[stateId]) + [DimsValue[stateId][rankId]]))

        self.Knowledge[knowledgeKey] = DimsMData
        return DimsMData

        
