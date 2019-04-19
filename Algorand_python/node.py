# !/bin/python3
from event import Event
from network_utils import*

class Node(object):
	def __init__(self, Id, secretkey, publickey, w):
		self.secretkey = secretkey
		self.privatekey = publickey
		self.nodeId = Id
		self.peerList = []
		self.w = w
		self.priorityGossipFound = False
		self.priorityList = []
		self.tau = 20
		self.W = 500
		self.lastGossipMessage = ""
		self.sentGossipMessages = []
		self.blockChain = []
		self.seed = "HASHOFPREVIOUSBLOCK" # TODO: compute hash for different rounds
		# Set Genesis Block
		genesisBlock = Block(GENESIS_BLOCK_CONTENT)
		self.blockChain.append(genesisBlock)

		self.incomingProposedBlocks = []

	def __str__(self):
		return '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))

	def sendMsg(self,event,dstNode):
		newEvent = Event(event.refTime,
						event.evTime + delays[self.nodeId][dstNode.nodeId],
						event.evType,
						event.msgToDeliver,
						event.timeOut,
						dstNode,
						self,
						event.roundNumber)

		eventQ.add(newEvent)
		#print("Pushed gossip event at time ",event.evTime + delays[self.nodeId][dstNode.nodeId])
		#print("Msg sent to (gossip message) ",dstNode.nodeId)

	def sendPriorityGossip(self,ev):
		#print("Round Number = ",ev.round)
		#print("Executing sendGossip at ",self.nodeId)
		#print("Message is :")
		if ev.msgToDeliver not in self.sentGossipMessages:
			message = ev.msgToDeliver
			if message.gossipType == GossipType.PRIORITY_GOSSIP:
				self.priorityList.append(message)
				self.priorityGossipFound = True
			else:
				print("This code should never be executed")

			randomNodeCnt = 0
			while randomNodeCnt <= GOSSIP_FAN_OUT:
				randomNode = random.choice(allNodes)
				if randomNode != self and (randomNode not in self.peerList):	#DONT select myself
					self.peerList.append(randomNode)
					randomNodeCnt = randomNodeCnt + 1

			for peer in self.peerList:
				if ev.evTime + delays[self.nodeId][peer.nodeId] - ev.refTime <= ev.timeOut:
					self.sendMsg(ev,peer)

			self.peerList.clear()
			self.lastGossipMessage = message.__str__() # not very perfect but still stops some messages
			self.sentGossipMessages.append(message)
		else:
			pass
			#print("Message Discarded : already sent via this Node [",self.nodeId,"]")

	def selectTopProposer(self,ev):
		# clear the record of outgoing priority gossip messages
		# we are going to push new block propose gossip message in this list
		self.sentGossipMessages.clear()

		IamTopProposer = None
		MyPriority = None
		MyPriorityMsg = None

		if self.priorityGossipFound:
			res = FindMaxPriorityAndNode(self.priorityList)
			# res will container three things
			# 1. res[0] = Node (with MAX priority)
			# 2. res[1] = its priority Message (corresponding)
			# print(self.nodeId," selects ",res[1].nodeId," as topProposer with priority ",res[0])
			if res[0].nodeId == self.nodeId:
				IamTopProposer = True
				MyPriority = res[1].priority
				print("I am (",self.nodeId,") topProposer and ",MyPriority," is my priority")
				MyPriorityMsg = res[1]

		if IamTopProposer is not None:
			# I need to create a block and gossip to the network
			prevBlock = self.blockChain[len(self.blockChain) - 1]
			prevBlockHash = hashlib.sha256(prevBlock.__str__().encode()).hexdigest()
			thisBlockContent = secrets.randbits(256)

			newBlockPropMsg = BlockProposeMsg(prevBlockHash,thisBlockContent,MyPriorityMsg)

			print(newBlockPropMsg)

			# Gossip This newBlockPropMsg
			randomNodeCnt = 0
			while randomNodeCnt <= GOSSIP_FAN_OUT:
				randomNode = random.choice(allNodes)
				if randomNode != self and (randomNode not in self.peerList):	#DONT select myself
					self.peerList.append(randomNode)
					randomNodeCnt = randomNodeCnt + 1

			# Two random nodes are selected
			# Now create two events and push in the Priority Queue

			for peer in self.peerList:
				# check the delay constraint first and then cerate event
				#
				if ev.evTime + 1 + delays[self.nodeId][peer.nodeId] - ev.refTime <= BLOCK_PROPOSE_GOSSIP_TIMEOUT:
					newEvent = Event(ev.evTime + 1,
									 ev.evTime + 1,
									 EventType.BLOCK_PROPOSE_GOSSIP_EVENT,
									 newBlockPropMsg,
									 BLOCK_PROPOSE_GOSSIP_TIMEOUT,
									 peer,
									 self,
									 ev.roundNumber)

					eventQ.add(newEvent)

			self.sentGossipMessages.append(newBlockPropMsg)
			self.peerList.clear()


		self.priorityGossipFound = False
		self.priorityList.clear()


		newEvent = Event(ev.evTime + BLOCK_PROPOSE_GOSSIP_TIMEOUT + 1,
						ev.evTime + BLOCK_PROPOSE_GOSSIP_TIMEOUT + 1,
						EventType.REDUCTION_COMMITTEE_VOTE_STEP_ONE,
						noMessage(),
						TIMEOUT_NOT_APPLICABLE,
						self,
						self,
						ev.roundNumber)

		eventQ.add(newEvent)
		#print("\n")


	def sendBlockPropGossip(self,ev):
		# self has received a proposed block just now
		# update my incomingProposedBlock List and relay further if possible
		# this incomingProposedBlock will be used in the reductionCommitteVoteStepOne() function
		if ev.msgToDeliver not in self.sentGossipMessages:
			message = ev.msgToDeliver
			self.incomingProposedBlocks.append(message)

			randomNodeCnt = 0

			while randomNodeCnt <= GOSSIP_FAN_OUT:
				randomNode = random.choice(allNodes)
				if randomNode != self and (randomNode not in self.peerList):	#DONT select myself
					self.peerList.append(randomNode)
					randomNodeCnt = randomNodeCnt + 1

			for peer in self.peerList:
				if ev.evTime + delays[self.nodeId][peer.nodeId] - ev.refTime <= ev.timeOut:
					self.sendMsg(ev,peer)

			self.peerList.clear()
			self.sentGossipMessages.append(message)

		else:
			pass



	def reductionCommitteVoteStepOne(self, ev):  # this is happening in 33 sec
		print("Performing reduction on ", self.nodeId)


	def computePriority(self,resp):
		#return np.random.randint(1,100) 				# TODO: generate random number
		hashList = []
		for i in range(resp.j):
			inp = str(resp.hashValue) + str(i + 1)
			sha = hashlib.sha256(inp.encode())
			hashList.append(sha.hexdigest())
		return hashList.index(min(hashList)) + 1


	def proposePriority(self,ev):
		#print("Round Number = ",ev.round)
		#print("Executing proposePriority event at ",self.nodeId)
		retval = Sortition(self.secretkey,self.seed,self.tau,"hello",self.w,self.W)
		resp = srtnResp(retval[0],retval[1],retval[2])
		if resp.j > 0:
			minPrio = 10000
			for i in range(resp.j):
				minPrio = min(self.computePriority(resp),minPrio)

			newPriorityMsg = priorityMessage(GossipType.PRIORITY_GOSSIP,
										ev.roundNumber,
										resp.hashValue,
										resp.j,
										minPrio,
										self)

			newEvent = Event(ev.refTime,
							ev.evTime,
							EventType.PRIORITY_GOSSIP_EVENT,
							newPriorityMsg,
							PRIORITY_GOSSIP_TIMEOUT,
							self,
							self,
							ev.roundNumber)

			eventQ.add(newEvent)

			#print("Pushed an GOSSIP_EVENT at time ",ev.evTime)

		newEvent = Event(ev.refTime + PRIORITY_GOSSIP_TIMEOUT + 1,
							ev.evTime + PRIORITY_GOSSIP_TIMEOUT + 1,
							EventType.SELECT_TOP_PROPOSER_EVENT,
							noMessage(),
							TIMEOUT_NOT_APPLICABLE,
							self,
						 	self,
							ev.roundNumber)

		eventQ.add(newEvent)

		#print("pushed an SELECT_TOP_PROPOSER_EVENT at time ",ev.evTime + PRIORITY_GOSSIP_TIMEOUT + 1)
		#print("\n")

