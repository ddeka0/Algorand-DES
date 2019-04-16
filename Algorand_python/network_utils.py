# !/bin/python3
from enum import Enum
from sortedcontainers import SortedList
from pprint import pprint

delays = []
eventQ = SortedList()
allNodes = []

class EventType(Enum):
	BLOCK_PROPOSER_SORTITION_EVENT	= 0
	GOSSIP_EVENT					= 1
	SELECT_TOP_PROPOSER_EVENT		= 2

class GossipType(Enum):
	PRIORITY_GOSSIP					= 0
	BLOCK_GOSSIP					= 1

class srtnResp(object):
	def __init__(self, hash, pi,subUserIndex):
		self.hash = hash
		self.pi = pi
		self.j = subUserIndex

class gossipMessage(object):
	def __init__(self, gossipType, roundNumber, hashOutput,
				 subUserIndex,priority):
		self.gossipType = gossipType
		self.roundNumber = roundNumber
		self.hashOutput = hashOutput
		self.subUserIndex = subUserIndex
		self.priority = priority

	def Print(self):
		print("hash = ",self.hash)
		print("j = ", self.subUserIndex)
		print("priority = ", self.priority)

class noMessage(object):
	def __init__(self):
		pass
	def Print(self):
		print("This is not a valid message")

MAX_NODES 				=	10
PRIORITY_GOSSIP_TIMEOUT	=	3
TIMEOUT_NOT_APPLICABLE	=	-1

