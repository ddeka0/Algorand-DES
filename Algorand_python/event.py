# !/bin/python3
class Event(object):
    def __init__(self,refTime,eventTime,eventType,msg,timeOut,targetNode,round):
        self.refTime = refTime
        self.evTime = eventTime
        self.evType = eventType
        self.msgToDeliver = msg
        self.timeOut = timeOut
        self.targetNode = targetNode
        self.round = round

    def __lt__(self, other):
        return self.evTime < other.evTime
