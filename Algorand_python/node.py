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
		self.prioritySet = SortedList()
		self.tau = 20
		self.W = 500
		self.seed = "HASHOFPREVIOUSBLOCK" # TODO: compute hash for different rounds

	def __str__(self):
		return '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))

	def sendMsg(self,event,dstNode):
		newEvent = Event(event.refTime,
						event.evTime + delays[self.nodeId][dstNode.nodeId],
						event.evType,
						event.msgToDeliver,
						event.timeOut,
						dstNode,
						event.round)

		eventQ.add(newEvent)
		print("Pushed gossip event at time ",event.evTime + delays[self.nodeId][dstNode.nodeId])
		print("Msg sent to (gossip message) ",dstNode.nodeId)

	def sendGossip(self,ev):
		print("Round Number = ",ev.round)
		print("Executing sendGossip at ",self.nodeId)
		print("Message is :")


		message = ev.msgToDeliver
		if message.gossipType == GossipType.PRIORITY_GOSSIP:
			self.prioritySet.add(message.priority)
			self.priorityGossipFound = True
		else:
			print("This code should never be executed")

		print(message)

		for i in range(2):
			self.peerList.append(random.choice(allNodes))

		for peer in self.peerList:
			if ev.evTime + delays[self.nodeId][peer.nodeId] - ev.refTime <= ev.timeOut:
				self.sendMsg(ev,peer)

		self.peerList.clear()

		print("\n")

	def selectTopProposer(self,ev):
		print("Round Number = ",ev.round)
		if self.priorityGossipFound:
			topProposerPriority = self.prioritySet[0]
			print(self.nodeId," selects ",topProposerPriority," as topProposer")

		self.priorityGossipFound = False
		self.prioritySet.clear()

		newEvent = Event(ev.evTime + 1,
						ev.evTime + 1,
						EventType.BLOCK_PROPOSER_SORTITION_EVENT,
						noMessage(),
						TIMEOUT_NOT_APPLICABLE,
						self,
						ev.round + 1)

		# eventQ.add(newEvent)
		print("\n")

	# def sortition(self):
	# 	resp = srtnResp(1,2,10)	# TODO: implement this sortition algorithm
	# 	return resp

	def computePriority(self):
		return 1 				# TODO: generate random number

	def proposePriority(self,ev):
		print("Round Number = ",ev.round)
		print("Executing proposePriority event at ",self.nodeId)
		retval = Sortition(self.secretkey,self.seed,self.tau,"hello",self.w,self.W)
		resp = srtnResp(retval[0],retval[1],retval[2])
		if resp.j > 0:
			minPrio = 10000
			for i in range(resp.j):
				minPrio = min(self.computePriority(),minPrio)

			newGossipMsg = gossipMessage(GossipType.PRIORITY_GOSSIP,
										ev.round,
										resp.hash,
										resp.j,
										minPrio)

			newEvent = Event(ev.refTime,
							ev.evTime,
							EventType.GOSSIP_EVENT,
							newGossipMsg,
							PRIORITY_GOSSIP_TIMEOUT,
							self,
							ev.round)

			eventQ.add(newEvent)

			print("Pushed an GOSSIP_EVENT at time ",ev.evTime)

		newEvent = Event(ev.refTime + PRIORITY_GOSSIP_TIMEOUT + 1,
							ev.evTime + PRIORITY_GOSSIP_TIMEOUT + 1,
							EventType.SELECT_TOP_PROPOSER_EVENT,
							noMessage(),
							TIMEOUT_NOT_APPLICABLE,
							self,
							ev.round)

		eventQ.add(newEvent)

		print("pushed an SELECT_TOP_PROPOSER_EVENT at time ",ev.evTime + PRIORITY_GOSSIP_TIMEOUT + 1)
		print("\n")
