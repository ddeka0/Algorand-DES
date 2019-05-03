# !/bin/python3
class Event(object):
    def __init__(self,refTime,eventTime,eventType,msg,timeOut,targetNode,sourceNode,roundNumber,stepNumber):
        self.refTime = refTime
        self.evTime = eventTime
        self.evType = eventType
        self.msgToDeliver = msg
        self.timeOut = timeOut
        self.targetNode = targetNode
        self.sourceNode = sourceNode
        self.roundNumber = roundNumber
        self.stepNumber = stepNumber

    def __lt__(self, other):
        return self.evTime < other.evTime

    def __str__(self):
        return str(self.evType) + "\t from: " + str(self.sourceNode.nodeId) +"\t to" + str(self.targetNode.nodeId) +"\t"+ str(self.msgToDeliver)
        #return '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))
    
    def getRoundStepTuple(self):
        return (self.roundNumber,self.stepNumber)
