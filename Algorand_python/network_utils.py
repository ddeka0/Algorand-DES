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
import pickle

delays = []
eventQ = SortedList()
allNodes = []
sk_List = []
pk_List = []
w_list = []
ctx_Weight = {}
blockDelays=[]

MAX_NODES = 100
TIMEOUT = None

REDUCTION_TWO = 2
tou_step = MAX_NODES * 0.2
tou_final = MAX_NODES * 0.2

FINAL_STEP  = 1000000

MAX_STEPS = 10 # given in the problem statement

INVOKE_BA_START_COUNT_VOTE_ONE = 1

INVOKE_BA_START_COUNT_VOTE_TWO = 2

INVOKE_BA_START_COUNT_VOTE_THREE = 3

DO_NOT_INVOKE_ANY_MORE_COUNT_VOTE = 0

PRIORITY_GOSSIP_TIMEOUT = 3
BLOCK_PROPOSE_GOSSIP_TIMEOUT	= 3
BLOCK_VOTE_REDUCTION_S1_GOSSIP_TIMEOUT = 20 # TODO check once
BLOCK_VOTE_REDUCTION_S2_GOSSIP_TIMEOUT = 20 # TODO check once
BA_STAR_GOSSIP_TIMEOUT = 20 # TODO check
TIMEOUT_NOT_APPLICABLE = -1
MAX_ALGORAND = 50
GENESIS_BLOCK_CONTENT = "We are building the best Algorand Discrete Event Simulator"

# max(MIN_DELAY,normal_delay)/DIVIDE_BY
MIN_DELAY = 0
DIVIDE_BY = 1000


GOSSIP_FAN_OUT 			= 3
T_STEP_REDUCTION_STEP_ONE = 2/3
T_STEP_REDUCTION_STEP_TWO = 2/3

class EventType(Enum):
	BLOCK_PROPOSER_SORTITION_EVENT = 0
	PRIORITY_GOSSIP_EVENT = 1
	SELECT_TOP_PROPOSER_EVENT = 2
	BLOCK_PROPOSE_GOSSIP_EVENT = 3
	REDUCTION_COMMITTEE_VOTE_STEP_ONE = 4
	BLOCK_VOTE_GOSSIP_EVENT = 5
	REDUCTION_COUNT_VOTE_STEP_ONE = 6
	REDUCTION_COUNT_VOTE_STEP_TWO = 7

	BASTAR_COUNT_VOTE_ONE = 8
	BASTAR_COUNT_VOTE_TWO = 9
	BASTAR_COUNT_VOTE_THREE = 10

	FINAL_COUNT_VOTE = 11

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
	global blockDelays

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

	for i in range(MAX_NODES):
		lz = [0] * MAX_NODES
		blockDelays.append(lz)

	for i in allNodes:
		for j in allNodes:
			if i == j:
				blockDelays[i.nodeId][j.nodeId] = 0
			else:
				normal_delay = np.random.normal(30,64,1)
				normal_delay = list(normal_delay)[0]
				blockDelays[i.nodeId][j.nodeId] = max(MIN_DELAY,normal_delay)/DIVIDE_BY


def init_AsymmtericKeys(listsk, listpk):
	pickleFile = open("keysFile-" + str(MAX_NODES), 'rb')
	keys = pickle.load(pickleFile)
	listsk.extend(keys[0])
	listpk.extend(keys[1])
	pickleFile.close()

def init_w(ctx_Weight,pk_list):
	for i in pk_list:
		r = random.randint(1, MAX_ALGORAND)
		ctx_Weight[i] = r


def FindMaxPriorityAndNode(priorityList):
	minPrioValue = 2**300
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
		self.block = Block(thisBlockContent,prevBlockHash)
		# start of Node's priority payload
		self.priorityMsgPayload = priorityMsgPayload
		self.sourceNode = self # TODO check

	def __str__(self):
		return "\n" + "block = " + str(self.block) + "\n" \
				+ self.priorityMsgPayload.__str__()

class VoteMsg(object):
	def __init__(self, roundNumber, step, hashValue, pi, prevBlockHash,thisBlockHash):
		self.roudNumber = roundNumber
		self.step = step
		self.hashValue = hashValue
		self.pi = pi
		self.prevBlockHash = prevBlockHash
		self.thisBlockHash = thisBlockHash
	def __str__(self):
		return "roundNumber = " + str(self.roudNumber) + "\n" \
			+ "step = " + str(self.step) + "\n" \
			+ "hashValue = " + str(self.hashValue) + "\n" \
			+ "pi = " + str(self.pi) + "\n" \
			+ "prevBlockHash = " + str(self.prevBlockHash) + "\n" \
			+ "thisBlockHash = " + str(self.thisBlockHash)

class BlockVoteMsg(object):
	def __init__(self, userPk, userSk, roundNumber, step, hashValue, pi, prevBlockHash, thisBlockHash,block):
		self.userPk = userPk
		msg = VoteMsg(roundNumber, step, hashValue, pi, prevBlockHash, thisBlockHash)
		digest = userSk.sign(str(msg).encode())
		# sgnVoteMsg is a tuple consisting of digest and the actual VoteMsg
		# actual VoteMsg : will be used for verification of the digest
		self.sgnVoteMsg = (digest,msg)
		self.block = block
def H(block):
	return (hashlib.sha256(str(block).encode())).hexdigest()


