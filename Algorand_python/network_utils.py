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
import sys
import os.path
from keygen import *
import config

eventQ = SortedList()
allNodes = []
delays = []
blockDelays=[]
sk_List = []
pk_List = []
w_list = []
ctx_Weight = {}

INVOKE_BA_START_COUNT_VOTE_ONE = 1

INVOKE_BA_START_COUNT_VOTE_TWO = 2

INVOKE_BA_START_COUNT_VOTE_THREE = 3

DO_NOT_INVOKE_ANY_MORE_COUNT_VOTE = 0

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
		return "\n" + "roundNumber = " + str(self.roundNumber) + "\n" \
				+ "hashOutput = " + str(self.hashOutput) + "\n" \
				+ "subUserIndex = " + str(self.subUserIndex) + "\n" \
				+ "priority = " + str(self.priority)

class noMessage(object):
	def __init__(self):
		pass
	def __str__(self):
		return '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item 
			in self.__dict__))


def init_Delays(delays,blockDelays):
	all_delays = []
	if not os.path.exists("delays-" + str(config.MAX_NODES)):
		print("non-block delays are not stored in file yet.")
		print("generating non-block delay martix..")
		generate_delays(config.MAX_NODES,config.NON_BLOCK_MSG_DELAY_MEAN,\
						config.NON_BLOCK_MSG_DELAY_SIGMA,config.BLOCK_MSG_DELAY_MEAN,\
						config.BLOCK_MSG_DELAY_SIGMA,config.MIN_DELAY)	

	with open('delays-'+  str(config.MAX_NODES), 'rb') as f:
		all_delays = pickle.load(f)

	delays.extend(all_delays[0])
	blockDelays.extend(all_delays[1])


def init_AsymmtericKeys(listsk, listpk):
	if not os.path.exists("keysFile-" + str(config.MAX_NODES)):
		print("keys are not stored in file yet.")
		print("generating keys..")
		generate_keys(config.MAX_NODES)
	
	pickleFile = open("keysFile-" + str(config.MAX_NODES), 'rb')
	keys = pickle.load(pickleFile)
	listsk.extend(keys[0])
	listpk.extend(keys[1])
	pickleFile.close()


def init_w(ctx_Weight,pk_list):
	for i in pk_list:
		r = random.randint(1, config.MAX_ALGORAND)
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
	def __init__(self, randomString ,prevBlockHash = None):
		self.transactions = randomString
		self.prevBlockHash = prevBlockHash
		self.state = config.NO_CONSENSUS

	def __str__(self):
		return "\n" + "transactions = " + str(self.transactions) + "\t" \
				+ "prevBlockHash = " + str(self.prevBlockHash)

class BlockProposeMsg(object):
	def __init__(self,prevBlockHash, thisBlockContent, priorityMsgPayload):
		self.block = Block(thisBlockContent,prevBlockHash)
		self.priorityMsgPayload = priorityMsgPayload
		self.sourceNode = self

	def __str__(self):
		return "\n" + "block = " + str(self.block) + "\n" \
				+ self.priorityMsgPayload.__str__()

class VoteMsg(object):
	def __init__(self, roundNumber, step, hashValue, pi, prevBlockHash,\
				thisBlockHash):
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
	def __init__(self, userPk, userSk, roundNumber, step, hashValue, pi,\
		prevBlockHash, thisBlockHash,block):
		self.userPk = userPk
		msg = VoteMsg(roundNumber, step, hashValue, pi, prevBlockHash,\
			thisBlockHash)
		digest = userSk.sign(str(msg).encode())
		# sgnVoteMsg is a tuple consisting of digest and the actual VoteMsg
		# actual VoteMsg : will be used for verification of the digest
		self.sgnVoteMsg = (digest,msg)
		self.block = block


def H(block):
	return (hashlib.sha256(str(block).encode())).hexdigest()


def initControlParams(args):

	print("Welcome to Algorand Discrete Event Simulator")
	config.MAX_NODES = args.max_nodes
	print("MAX_NODES = ",config.MAX_NODES)

	config.GOSSIP_FAN_OUT = args.fan_out
	print("GOSSIP_FAN_OUT = ",config.GOSSIP_FAN_OUT)

	config.NON_BLOCK_MSG_DELAY_MEAN = args.non_block_delay_mean
	print("NON_BLOCK_MSG_DELAY_MEAN = ",config.NON_BLOCK_MSG_DELAY_MEAN)

	config.NON_BLOCK_MSG_DELAY_SIGMA = args.non_block_delay_sigma
	print("NON_BLOCK_MSG_DELAY_SIGMA = ",config.NON_BLOCK_MSG_DELAY_SIGMA)

	config.BLOCK_MSG_DELAY_MEAN = args.block_delay_mean
	print("BLOCK_MSG_DELAY_MEAN = ",config.BLOCK_MSG_DELAY_MEAN)

	config.BLOCK_MSG_DELAY_SIGMA = args.block_delay_sigma
	print("BLOCK_MSG_DELAY_SIGMA = ",config.BLOCK_MSG_DELAY_SIGMA)

	config.tou_step = args.tou_step
	print("tou_step = ",config.tou_step)

	config.tou_prop = args.tou_prop
	print("tou_prop = ",config.tou_prop)

	config.tou_final = args.tou_final
	print("tou_final = ",config.tou_final)

	config.MAX_ALGORAND = args.max_algorand
	print("MAX_ALGORAND = ",config.MAX_ALGORAND)
	