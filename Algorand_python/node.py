# !/bin/python3
from event import Event
from network_utils import*

class Node(object):
	def __init__(self, Id,secretkey,publickey,w):
		self.secretkey = secretkey
		self.privatekey = publickey
		self.nodeId = Id
		self.peerList=[]
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
						event.round)

		eventQ.add(newEvent)
		#print("Pushed gossip event at time ",event.evTime + delays[self.nodeId][dstNode.nodeId])
		#print("Msg sent to (gossip message) ",dstNode.nodeId)

	def sendGossip(self,ev):
		#print("Round Number = ",ev.round)
		#print("Executing sendGossip at ",self.nodeId)
		#print("Message is :")
		if (ev.msgToDeliver not in self.sentGossipMessages):
			message = ev.msgToDeliver
			if message.gossipType == GossipType.PRIORITY_GOSSIP:
				self.priorityList.append(message)
				self.priorityGossipFound = True
			else:
				print("This code should never be executed")

			randomNodeCnt = 0
			while(randomNodeCnt <= GOSSIP_FAN_OUT):
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
		#print("Round Number = ",ev.round)
		IamTopProposer = None
		MyPriority = None
		if self.priorityGossipFound:
			res = FindMaxPriorityAndNode(self.priorityList)
			#print(self.nodeId," selects ",res[1].nodeId," as topProposer with priority ",res[0])
			if res[1].nodeId == self.nodeId:
				IamTopProposer = True
				MyPriority = res[0]
				print("I am (",self.nodeId,") topProposer and ",res[0]," is my priority")

		if IamTopProposer is not None:
			# I need to create a block and gossip to the network
			prevBlock = self.blockChain[len(self.blockChain) - 1]
			prevBlockHash = hashlib.sha256(prevBlock.__str__().encode()).hexdigest()
			thisBlockContent = secrets.randbits(256)
			newBlockPropMsg = BlockProposeMsg(prevBlockHash,thisBlockContent,MyPriority)
			print(newBlockPropMsg)



		self.priorityGossipFound = False
		self.priorityList.clear()
		self.sentGossipMessages.clear()

		newEvent = Event(ev.evTime + 1,
						ev.evTime + 1,
						EventType.BLOCK_PROPOSER_SORTITION_EVENT,
						noMessage(),
						TIMEOUT_NOT_APPLICABLE,
						self,
						self,
						ev.round + 1)

		# eventQ.add(newEvent)
		#print("\n")

	def computePriority(self):
		return np.random.randint(1,100) 				# TODO: generate random number

	def proposePriority(self,ev):
		#print("Round Number = ",ev.round)
		#print("Executing proposePriority event at ",self.nodeId)
		retval = Sortition(self.secretkey,self.seed,self.tau,"hello",self.w,self.W)
		resp = srtnResp(retval[0],retval[1],retval[2])
		if resp.j > 0:
			minPrio = 10000
			for i in range(resp.j):
				minPrio = min(self.computePriority(),minPrio)

			newGossipMsg = priorityMessage(GossipType.PRIORITY_GOSSIP,
										ev.round,
										resp.hashValue,
										resp.j,
										minPrio,
										self)

			newEvent = Event(ev.refTime,
							ev.evTime,
							EventType.GOSSIP_EVENT,
							newGossipMsg,
							PRIORITY_GOSSIP_TIMEOUT,
							self,
							self,
							ev.round)

			eventQ.add(newEvent)

			#print("Pushed an GOSSIP_EVENT at time ",ev.evTime)

		newEvent = Event(ev.refTime + PRIORITY_GOSSIP_TIMEOUT + 1,
							ev.evTime + PRIORITY_GOSSIP_TIMEOUT + 1,
							EventType.SELECT_TOP_PROPOSER_EVENT,
							noMessage(),
							TIMEOUT_NOT_APPLICABLE,
							self,
						 	self,
							ev.round)

		eventQ.add(newEvent)

		#print("pushed an SELECT_TOP_PROPOSER_EVENT at time ",ev.evTime + PRIORITY_GOSSIP_TIMEOUT + 1)
		#print("\n")
