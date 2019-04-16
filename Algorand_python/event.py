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

    def __str__(self):
        return '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))