# !/bin/python3
from enum import Enum
from sortedcontainers import SortedList
from sortiton import *
import random
from pprint import pprint
import numpy as np
import ecdsa
import hashlib
import secrets

delays = []
eventQ = SortedList()
allNodes = []
sk_List = []
pk_List = []
w_list = []

MAX_NODES = 30
PRIORITY_GOSSIP_TIMEOUT = 3
BLOCK_PROPOSE_GOSSIP_TIMEOUT	= 33
TIMEOUT_NOT_APPLICABLE = -1
MAX_ALGORAND = 50
GENESIS_BLOCK_CONTENT = "We are building the best Algorand Discrete Event Simulator"

# max(MIN_DELAY,normal_delay)/DIVIDE_BY
MIN_DELAY = 0
DIVIDE_BY = 1000


GOSSIP_FAN_OUT 			= 2


class EventType(Enum):
	BLOCK_PROPOSER_SORTITION_EVENT = 0
	PRIORITY_GOSSIP_EVENT = 1
	SELECT_TOP_PROPOSER_EVENT = 2
	BLOCK_PROPOSE_GOSSIP_EVENT = 3
	REDUCTION_COMMITTEE_VOTE_STEP_ONE = 4



class GossipType(Enum):
	PRIORITY_GOSSIP					= 0
	BLOCK_GOSSIP					= 1


class srtnResp(object):
	def __init__(self, hashValue, pi, subUserIndex):
		self.hashValue = hashValue
		self.pi = pi
		self.j = subUserIndex


class priorityMessage(object):
	def __init__(self, gossipType, roundNumber, hashOutput,
				subUserIndex, priority,sourceNode):
		self.gossipType = gossipType
		self.roundNumber = roundNumber
		self.hashOutput = hashOutput
		self.subUserIndex = subUserIndex
		self.priority = priority
		self.sourceNode = sourceNode

	def __str__(self):
		#return '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))
		return "\n" + "roundNumber = " + str(self.roundNumber) + "\n" \
				+ "hashOutput = " + str(self.hashOutput) + "\n" \
				+ "subUserIndex = " + str(self.subUserIndex) + "\n" \
				+ "priority = " + str(self.priority)

class noMessage(object):
	def __init__(self):
		pass
	def __str__(self):
		return '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))


def init_Delays():
	global delays
	global allNodes

	for i in range(MAX_NODES):
		lz = [0] * MAX_NODES
		delays.append(lz)

	for i in allNodes:
		for j in allNodes:
			if i == j:
				delays[i.nodeId][j.nodeId] = 0
			else:
				normal_delay = np.random.normal(200,400,1)
				normal_delay = list(normal_delay)[0]
				delays[i.nodeId][j.nodeId] = max(MIN_DELAY,normal_delay)/DIVIDE_BY  # TODO: change value here


def init_AsymmtericKeys(listsk, listpk):
	for i in range(MAX_NODES):
		listsk.append(ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1))
		#print("sk = ", i)

	for i in range(MAX_NODES):
		listpk.append(listsk[i].get_verifying_key())
		#print("vk = ", i)


def init_w(listw):
	for i in range(MAX_NODES):
		listw.append(random.randint(1, MAX_ALGORAND))


def FindMaxPriorityAndNode(priorityList):
	minPrioValue = 2**260
	minPrioNode = None
	minPrioMsg = None
	for msg in priorityList:
		p = msg.priority
		if p < minPrioValue:
			minPrioValue = p
			minPrioNode = msg.sourceNode
			minPrioMsg = msg
	return tuple((minPrioNode,minPrioMsg))


class Block(object):
	def __init__(self, randomString, prevBlockHash = None):
		self.transactions = randomString
		self.prevBlockHash = prevBlockHash

	def __str__(self):
		#return '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))
		return "\n" + "transactions = " + str(self.transactions) + "\n" \
				+ "prevBlockHash = " + str(self.prevBlockHash)

class BlockProposeMsg(object):
	def __init__(self,prevBlockHash, thisBlockContent, priorityMsgPayload):
		self.prevBlockHash = prevBlockHash
		self.thisBlockContent = thisBlockContent
		# start of Node's priority payload
		self.priorityMsgPayload = priorityMsgPayload
		self.sourceNode = self

	def __str__(self):
		return "\n" + "prevBlockHash = " + str(self.prevBlockHash) + "\n" \
				+ "thisBlockContent = " + str(self.thisBlockContent) + "\n" \
				+ self.priorityMsgPayload.__str__()