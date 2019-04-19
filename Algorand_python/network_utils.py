# !/bin/python3
from enum import Enum
from sortedcontainers import SortedList
from sortiton import *
import random
from pprint import pprint
import numpy as np
import ecdsa

delays = []
eventQ = SortedList()
allNodes = []
sk_List = []
pk_List = []
w_list = []

MAX_NODES 				= 20
PRIORITY_GOSSIP_TIMEOUT	= 3
TIMEOUT_NOT_APPLICABLE	= -1
MAX_ALGORAND			= 50

GOSSIP_FAN_OUT 			= 2

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
				 subUserIndex, priority,sourceNode):
		self.gossipType = gossipType
		self.roundNumber = roundNumber
		self.hashOutput = hashOutput
		self.subUserIndex = subUserIndex
		self.priority = priority
		self.sourceNode = sourceNode

	def __str__(self):
		return '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))


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
				delays[i.nodeId][j.nodeId] = max(0,normal_delay)/1000  # TODO: change value here


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
	minPrioValue = 100000000
	minPrioNode = None
	for msg in priorityList:
		p = msg.priority
		if p < minPrioValue:
			minPrioValue = p
			minPrioNode = msg.sourceNode

	return tuple((minPrioValue,minPrioNode))
