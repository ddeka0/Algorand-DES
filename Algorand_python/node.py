# !/bin/python3
from event import Event
from network_utils import*
from multiprocessing import  Pool,cpu_count
from functools import partial
import math
import config
from logging_config import * 

class Node(object):
	def __init__(self, Id, secretkey, publickey, w):
		self.secretkey = secretkey
		self.publickey = publickey
		self.nodeId = Id
		self.peerList = []
		self.w = w
		self.priorityGossipFound = False
		self.priorityList = []
		#self.tau = MAX_NODES * 0.1 # 10 percent
		#self.tau = 5  # 10 percent
		self.tau = config.tou_prop #this is for 2.2.4
		self.tau_committee = config.tou_step  # 20 percent
		self.W = config.MAX_NODES * (config.MAX_ALGORAND / 2)
		self.sentGossipMessages = []
		self.blockChain = []
		self.seed = "HASHOFPREVIOUSBLOCK" 
		# TODO: compute hash for different rounds
		# Set Genesis Block
		genesisBlock = Block(config.GENESIS_BLOCK_CONTENT)
		genesisBlock.state = config.FINAL_CONSENSUS
		self.blockChain.append(genesisBlock)
		
		self.incomingProposedBlocks = []	
		# this queue will be used for incoming block prop messages
		self.incomingBlockVoteMsg = {}		
		# this queue will be used for incoming vote block message
		self.bastarBlockHash = None
		self.bastarOutput = None
		self.bastarBlock = None

		
		self.isAdversary=False
		self.isByzantine =False

	def __str__(self):
		return '\n'.join(('{} = {}'.format(item, self.__dict__[item]) \
			for item in self.__dict__))

	def sendMsg(self,event,dstNode,deltaTime):
		newEvent = Event(event.refTime,
						event.evTime + deltaTime,
						event.evType,
						event.msgToDeliver,
						event.timeOut,
						dstNode,
						self,
						event.roundNumber,
						event.stepNumber)

		eventQ.add(newEvent)

	def genNextSeed(self,roundNumber,stepNumber):
		prevBlock = self.blockChain[len(self.blockChain) - 1]
		prevBlockHash = H(prevBlock)
		self.seed = prevBlockHash + str(roundNumber) + str(stepNumber)


	def sendPriorityGossip(self,ev):
		if ev.msgToDeliver not in self.sentGossipMessages:
			message = ev.msgToDeliver
			if message.gossipType == GossipType.PRIORITY_GOSSIP:
				self.priorityList.append(message)
				self.priorityGossipFound = True
			else:
				print("This code should never be executed")

			randomNodeCnt = 0
			while randomNodeCnt < config.GOSSIP_FAN_OUT:
				randomNode = random.choice(allNodes)
				if randomNode != self and (randomNode not in self.peerList):
					#DONT select myself
					self.peerList.append(randomNode)
					randomNodeCnt = randomNodeCnt + 1

			for peer in self.peerList:
				if ev.evTime + delays[self.nodeId][peer.nodeId] - ev.refTime \
					<= ev.timeOut: # delay non block
					self.sendMsg(ev,peer,delays[self.nodeId][peer.nodeId])
				else:
					pass
			self.peerList.clear()
			# not very perfect but still stops some messages
			self.sentGossipMessages.append(message)
		else:
			pass

	def selectTopProposer(self,ev):
		self.sentGossipMessages.clear()
		
		IamTopProposer = None
		MyPriority = None
		MyPriorityMsg = None

		if self.priorityGossipFound:
			res = FindMaxPriorityAndNode(self.priorityList)
			# 1. res[0] = Node (with MAX priority)
			# 2. res[1] = its priority Message (corresponding)
			if res[0].nodeId == self.nodeId:
				IamTopProposer = True
				MyPriority = res[1].priority
				print(BOLDYELLOW("=>"),self.nodeId,"sortition-top-proposer-round",\
					str(ev.roundNumber),RESET(""))
				MyPriorityMsg = res[1]
			else:
				pass
	
		if IamTopProposer is not None:
			prevBlock = self.blockChain[len(self.blockChain) - 1]
			prevBlockHash = hashlib.sha256(prevBlock.__str__().encode())\
							.hexdigest()
			thisBlockContent = secrets.randbits(256)
			newBlockPropMsg = BlockProposeMsg(prevBlockHash,thisBlockContent,\
				MyPriorityMsg)
			newEvent = Event(ev.evTime,
							 ev.evTime,
							 EventType.BLOCK_PROPOSE_GOSSIP_EVENT,
							 newBlockPropMsg,
							 config.BLOCK_PROPOSE_GOSSIP_TIMEOUT,
							 self,
							 self,
							 ev.roundNumber,
							 ev.stepNumber)

			eventQ.add(newEvent)


		self.priorityGossipFound = False
		self.priorityList.clear()

		newEvent = Event(ev.evTime + config.BLOCK_PROPOSE_GOSSIP_TIMEOUT + 1,
						ev.evTime + config.BLOCK_PROPOSE_GOSSIP_TIMEOUT + 1,
						EventType.REDUCTION_COMMITTEE_VOTE_STEP_ONE,
						noMessage(),
						config.TIMEOUT_NOT_APPLICABLE,
						self,
						self,
						ev.roundNumber,
						ev.stepNumber + 1)

		eventQ.add(newEvent)


	def sendBlockPropGossip(self,ev):
		if ev.msgToDeliver not in self.sentGossipMessages:
			message = ev.msgToDeliver
			self.incomingProposedBlocks.append(message)
			randomNodeCnt = 0
			while randomNodeCnt < config.GOSSIP_FAN_OUT:
				randomNode = random.choice(allNodes)
				if randomNode != self and (randomNode not in self.peerList):	
					#DONT select myself
					self.peerList.append(randomNode)
					randomNodeCnt = randomNodeCnt + 1

			for peer in self.peerList:
				if ev.evTime + blockDelays[self.nodeId][peer.nodeId] - \
					ev.refTime <= ev.timeOut:
					self.sendMsg(ev,peer,blockDelays[self.nodeId][peer.nodeId])
				else:
					pass

			self.peerList.clear()
			self.sentGossipMessages.append(message)
		else:
			pass

	def reductionCommitteVoteStepOne(self, ev):
		self.sentGossipMessages.clear()

		if len(self.incomingProposedBlocks) == 0:
			pass
		else:
			minPrio = 2**300
			maxPropBlockMsg = None
			for propBlockMsg in self.incomingProposedBlocks:
				if propBlockMsg.priorityMsgPayload.priority < minPrio:
					minPrio = propBlockMsg.priorityMsgPayload.priority
					maxPropBlockMsg = propBlockMsg
			self.genNextSeed(ev.roundNumber, ev.stepNumber)
			retval = Sortition(self.secretkey, self.seed, self.tau_committee,\
				 "hello", self.w, self.W)
			resp = srtnResp(retval[0],retval[1],retval[2]) # TODO remove
			if resp.j > 0: # If I have own the committe
				#print(BOLDGREEN("=>"),self.nodeId,"sortition-reduction-step-one",\
				#	str(ev.roundNumber),RESET(""))
				prevBlock = self.blockChain[len(self.blockChain) - 1]
				prevBlockHash = H(prevBlock)
				thisBlockHash = hashlib.sha256(maxPropBlockMsg.block.__str__()\
								.encode()).hexdigest()

				blockVoteMsg = BlockVoteMsg(self.publickey,
											self.secretkey,
											ev.roundNumber,
											ev.stepNumber,
											resp.hashValue,
											resp.pi,
											prevBlockHash,
											thisBlockHash,
											maxPropBlockMsg.block)

				newEvent = Event(ev.evTime,
								ev.evTime,
								EventType.BLOCK_VOTE_GOSSIP_EVENT,
								blockVoteMsg,
								config.BLOCK_VOTE_REDUCTION_S1_GOSSIP_TIMEOUT,
								self,
								self,
								ev.roundNumber,
								ev.stepNumber)

				eventQ.add(newEvent)

		newEvent2 = Event(ev.evTime + config.BLOCK_VOTE_REDUCTION_S1_GOSSIP_TIMEOUT + 1,
						ev.evTime + config.BLOCK_VOTE_REDUCTION_S1_GOSSIP_TIMEOUT + 1,
						EventType.REDUCTION_COUNT_VOTE_STEP_ONE,
						noMessage(),
						config.TIMEOUT_NOT_APPLICABLE,
						self,
						self,
						ev.roundNumber,
						ev.stepNumber)

		eventQ.add(newEvent2)

	def sendBlockVoteGossip(self,ev):
		if ev.msgToDeliver not in self.sentGossipMessages:
			message = ev.msgToDeliver
			if ev.getRoundStepTuple() not in self.incomingBlockVoteMsg:
				self.incomingBlockVoteMsg[ev.getRoundStepTuple()]=[]
			self.incomingBlockVoteMsg[ev.getRoundStepTuple()].append(message)

			randomNodeCnt = 0
			while randomNodeCnt < config.GOSSIP_FAN_OUT:
				randomNode = random.choice(allNodes)
				if randomNode != self and (randomNode not in self.peerList):	
					#DONT select myself
					self.peerList.append(randomNode)
					randomNodeCnt = randomNodeCnt + 1

			for peer in self.peerList:
				if ev.evTime + delays[self.nodeId][peer.nodeId] - ev.refTime \
					<= ev.timeOut:
					self.sendMsg(ev,peer,delays[self.nodeId][peer.nodeId])
				else:
					print("More Delay")

			self.peerList.clear()
			self.sentGossipMessages.append(message)
		else:
			pass


	def ProcessMsg(self, ctxw ,m):
		pk = m.userPk
		signed_m = m.sgnVoteMsg[0] # index for digest sgnVoteMsg is tuple
		msg = m.sgnVoteMsg[1] # index for msg
		block = m.block

		# TODO use fastecdsa
		# if not pk.verify(signed_m, str((msg)).encode('utf-8')):
		# 	print("Verification Failed")
		# 	return tuple((0,False,False))
		# else:
		roundNumber = msg.roudNumber
		step = msg.step
		sortHash = msg.hashValue
		pi = msg.pi
		hprev = msg.prevBlockHash
		value = msg.thisBlockHash
		if hprev != H(self.blockChain[len(self.blockChain)-1]):
			print("hprev is" ,hprev)
			print("from blockchain" ,H(self.blockChain[len(self.blockChain)-1]))
			print("prev block hash mismatch")
			return tuple((0,False,False,False,False))
		else:
			votes = VerifySort(pk,sortHash,pi,self.seed,self.tau_committee,\
				"hello",ctxw[pk],self.W)
			return tuple((votes,value,sortHash,pk,block))

	def printBlockchain(self):
		for blk in self.blockChain:
			print(blk)
	
	def CountVotes(self, Tstep ,ev):
		counts = {}
		msgs = []
		if ev.getRoundStepTuple() in self.incomingBlockVoteMsg:
			msgs = self.incomingBlockVoteMsg[ev.getRoundStepTuple()]
		voters = []
		
		while True:
			try:
				m=msgs.pop()
				votes, value, sortHasg, pk, block = self.ProcessMsg(ctx_Weight,m)
				if pk in voters or votes == 0:
					continue
				voters.append(pk)
				if value in counts:
					counts[value] += votes
				else:
					counts[value] = votes
				if counts[value] >= math.floor(Tstep * self.tau_committee):
					return (value,block)
				else:
					pass
			except:
				return (None , None)
		if ev.getRoundStepTuple() in self.incomingBlockVoteMsg:
			self.incomingBlockVoteMsg[ev.getRoundStepTuple()].clear()

		return (None,None)

	def reductionCountVoteStepOne(self,ev):
		hBlockOne,block = self.CountVotes(config.T_STEP_REDUCTION_STEP_ONE,ev)
		#print("Reduction step2 starts...")

		if hBlockOne is config.TIMEOUT:
			block = self.getEmptyBlock()
			self.reductionCommitteVoteStepTwo(ev,ev.roundNumber,config.REDUCTION_TWO,\
				config.tou_step,H(block),block)
		else:
			print(self.nodeId, "Got anough vote for (hblock-1)", BOLDGREEN(hBlockOne),RESET(""))
			self.reductionCommitteVoteStepTwo(ev,ev.roundNumber,config.REDUCTION_TWO,\
				config.tou_step,hBlockOne,block)


	def reductionCommitteVoteStepTwo(self,ev,roundNumber, stepNumber, \
		touCommitte, hBlock,block):
		self.sentGossipMessages.clear()

		self.genNextSeed(roundNumber, stepNumber)
		retval = Sortition(self.secretkey, self.seed, touCommitte, "hello", \
			self.w, self.W)
		resp = srtnResp(retval[0], retval[1], retval[2])  # TODO remove
		if resp.j > 0:  # If I have own the committe
			print(BOLDYELLOW("=>"),self.nodeId,"sortition-reduction-step-two at round",str(ev.roundNumber),RESET(""))
			prevBlock = self.blockChain[len(self.blockChain) - 1]
			prevBlockHash = H(prevBlock)
			thisBlockHash = hBlock

			blockVoteMsg = BlockVoteMsg(self.publickey,
										self.secretkey,
										roundNumber,
										stepNumber,
										resp.hashValue,
										resp.pi,
										prevBlockHash,
										thisBlockHash,
										block)

			newEvent = Event(ev.evTime,
							 ev.evTime,
							 EventType.BLOCK_VOTE_GOSSIP_EVENT,
							 blockVoteMsg,
							 config.BLOCK_VOTE_REDUCTION_S2_GOSSIP_TIMEOUT,
							 self,
							 self,
							 roundNumber,
							 stepNumber)

			eventQ.add(newEvent)
		else:
			pass

		newEvent2 = Event(ev.evTime + config.BLOCK_VOTE_REDUCTION_S2_GOSSIP_TIMEOUT + 1,
						  ev.evTime + config.BLOCK_VOTE_REDUCTION_S2_GOSSIP_TIMEOUT + 1,
						  EventType.REDUCTION_COUNT_VOTE_STEP_TWO,
						  noMessage(),
						  config.TIMEOUT_NOT_APPLICABLE,
						  self,
						  self,
						  roundNumber,
						  stepNumber)  # step = 1
		eventQ.add(newEvent2)

	def reductionCountVoteStepTwo(self,ev):
		hBlockTwo,block = self.CountVotes(config.T_STEP_REDUCTION_STEP_TWO, ev)
		if hBlockTwo == config.TIMEOUT:
			print(self.nodeId, "hblock-2 TIMEOUT")
			self.bastarBlockHash = self.getEmptyHash()
			self.bastarBlock = self.getEmptyBlock()
		else:
			print(self.nodeId, "Got anough vote for (hblock-2)", BOLDGREEN(hBlockTwo),RESET(""))
			self.bastarBlockHash = hBlockTwo
			self.bastarBlock = block

		self.BAstarPhaseOne(ev,3)


	def BAstarPhaseOne(self,ev,stepNumber):
		self.BAstartCommitteVote(ev,ev.roundNumber,stepNumber,config.tou_step,\
			INVOKE_BA_START_COUNT_VOTE_ONE,self.bastarBlockHash,self.bastarBlock)


	def BAstartCommitteVote(self,ev,roundNumber,stepNumber,touCommitte,flag,\
		block_hash,block):
		if flag == INVOKE_BA_START_COUNT_VOTE_ONE and stepNumber >= config.MAX_STEPS:
			print("***********************************************")
			self.bastarOutput = self.getEmptyHash()
			self.bastarBlock = self.getEmptyBlock()
			newEvent = Event(ev.evTime + 1,
							ev.evTime + 1,
							EventType.FINAL_COUNT_VOTE,
							noMessage(),
							config.TIMEOUT_NOT_APPLICABLE,
							self,
							self,
							ev.roundNumber,
							config.FINAL_STEP)

			eventQ.add(newEvent)
			return

		self.sentGossipMessages.clear()

		self.genNextSeed(roundNumber, stepNumber)
		retval = Sortition(self.secretkey, self.seed, touCommitte, "hello",\
				self.w, self.W)
		resp = srtnResp(retval[0], retval[1], retval[2])  # TODO remove
		if resp.j > 0:  # If I have own the committe
			print(BOLDMAGENTA("=>"),self.nodeId,"sortition-bastar-step",str(ev.stepNumber),\
				"round",str(ev.roundNumber),RESET(""))
			prevBlock = self.blockChain[len(self.blockChain) - 1]
			prevBlockHash = H(prevBlock)
			thisBlockHash = block_hash  # this could be empty or non empty also

			blockVoteMsg = BlockVoteMsg(self.publickey,
										self.secretkey,
										roundNumber,
										stepNumber,
										resp.hashValue,
										resp.pi,
										prevBlockHash,
										thisBlockHash,
										block)

			newEvent = Event(ev.evTime,
							 ev.evTime,
							 EventType.BLOCK_VOTE_GOSSIP_EVENT,
							 blockVoteMsg,
							 config.BLOCK_VOTE_REDUCTION_S2_GOSSIP_TIMEOUT,
							 self,
							 self,
							 roundNumber,
							 stepNumber)

			eventQ.add(newEvent)
		else:
			pass

		if flag == INVOKE_BA_START_COUNT_VOTE_ONE:
			# Push the reduction step 2 cound vote event after +3 sec
			newEvent2 = Event(ev.evTime + config.BA_STAR_GOSSIP_TIMEOUT + 1,
							  ev.evTime + config.BA_STAR_GOSSIP_TIMEOUT + 1,
							  EventType.BASTAR_COUNT_VOTE_ONE,
							  noMessage(),
							  config.TIMEOUT_NOT_APPLICABLE,
							  self,
							  self,
							  roundNumber,
							  stepNumber)
			eventQ.add(newEvent2)
		elif flag == INVOKE_BA_START_COUNT_VOTE_TWO:
			# Push the reduction step 2 cound vote event after +3 sec
			newEvent2 = Event(ev.evTime + config.BLOCK_VOTE_REDUCTION_S2_GOSSIP_TIMEOUT + 1,
							  ev.evTime + config.BLOCK_VOTE_REDUCTION_S2_GOSSIP_TIMEOUT + 1,
							  EventType.BASTAR_COUNT_VOTE_TWO,
							  noMessage(),
							  config.TIMEOUT_NOT_APPLICABLE,
							  self,
							  self,
							  roundNumber,
							  stepNumber)
			eventQ.add(newEvent2)
		elif flag == INVOKE_BA_START_COUNT_VOTE_THREE:
			newEvent2 = Event(ev.evTime + config.BLOCK_VOTE_REDUCTION_S2_GOSSIP_TIMEOUT + 1,
							  ev.evTime + config.BLOCK_VOTE_REDUCTION_S2_GOSSIP_TIMEOUT + 1,
							  EventType.BASTAR_COUNT_VOTE_THREE,
							  noMessage(),
							  config.TIMEOUT_NOT_APPLICABLE,
							  self,
							  self,
							  roundNumber,
							  stepNumber)
			eventQ.add(newEvent2)
		elif flag == DO_NOT_INVOKE_ANY_MORE_COUNT_VOTE:
			pass
		else:
			pass

	def BAstartCountVoteOne(self,ev):
		print(self.nodeId, " BA* Count Vote ONE is executing in step = "\
			,ev.stepNumber)
		step = ev.stepNumber
		r,block = self.CountVotes(config.T_STEP_REDUCTION_STEP_TWO, ev)
		if r is config.TIMEOUT:
			r = self.bastarBlockHash
			block = self.bastarBlock
		elif r is not self.getEmptyHash():
			for s in range(ev.stepNumber,ev.stepNumber + 3):
				self.BAstartCommitteVote(ev,ev.roundNumber,s,config.tou_step,\
					DO_NOT_INVOKE_ANY_MORE_COUNT_VOTE,r,block)
			if step == 3:
				self.BAstartCommitteVote(ev,ev.roundNumber,config.FINAL_STEP,\
					config.tou_final,DO_NOT_INVOKE_ANY_MORE_COUNT_VOTE,r,block)

			self.bastarOutput = r
			self.bastarBlock = block
			newEvent = Event(ev.evTime + 1,
							 ev.evTime + 1,
							 EventType.FINAL_COUNT_VOTE,
							 noMessage(),
							 config.TIMEOUT_NOT_APPLICABLE,
							 self,
							 self,
							 ev.roundNumber,
							 config.FINAL_STEP)

			eventQ.add(newEvent)
			return
		else:
			print("Got consesus on empty block")
			print("Need to move forward")

		step += 1
		self.BAstartCommitteVote(ev,ev.roundNumber,step,config.tou_step,\
			INVOKE_BA_START_COUNT_VOTE_TWO,r,block)


	def BAstartCountVoteTwo(self,ev):
		print(self.nodeId, " BA* Count Vote two is executing in step = ",\
			ev.stepNumber)
		step = ev.stepNumber
		r,block = self.CountVotes(config.T_STEP_REDUCTION_STEP_TWO, ev)
		if r is config.TIMEOUT:
			r = self.getEmptyHash()
			block = self.getEmptyBlock()
		elif r == self.getEmptyHash():
			for s in range(ev.stepNumber,ev.stepNumber + 3):
				# vote on the empty block
				# send an empty block also
				block = self.getEmptyBlock()
				self.BAstartCommitteVote(ev,ev.roundNumber,step,config.tou_step,\
					DO_NOT_INVOKE_ANY_MORE_COUNT_VOTE,r,block)

			self.bastarOutput = r
			self.bastarBlock = block
			newEvent = Event(ev.evTime + 1,
							 ev.evTime + 1,
							 EventType.FINAL_COUNT_VOTE,
							 noMessage(),
							 config.TIMEOUT_NOT_APPLICABLE,
							 self,
							 self,
							 ev.roundNumber,
							 config.FINAL_STEP)

			eventQ.add(newEvent)
			return

		step += 1
		self.BAstartCommitteVote(ev,ev.roundNumber,step,config.tou_step,\
								INVOKE_BA_START_COUNT_VOTE_THREE,r,block)

	def finalCountVote(self,ev):
		r,block = self.CountVotes(config.T_STEP_REDUCTION_STEP_TWO, ev)  # TODO T_STEP check
		#print("step number shuld be huge", ev.stepNumber)
		if r == self.bastarOutput:
			if r == self.getEmptyHash():
				print("Added block was empty")
			self.bastarBlock.state = config.FINAL_CONSENSUS
			self.blockChain.append(self.bastarBlock)
			print(BOLDGREEN("[FINAL"),RESET(""),str(self.nodeId),"](new block added)=", \
					H(self.bastarBlock), "in round =",BOLDGREEN(ev.roundNumber),RESET("") \
					,"at time" , ev.evTime)
			# print(str(self.nodeId),"Block transaction ",\
			# 	self.bastarBlock.transactions )
		else:
			print("[TENTATIVE",str(self.nodeId),"](new block added)=",\
				H(self.bastarBlock), "in round =",ev.roundNumber ,"at time" ,\
				ev.evTime)
			# print(str(self.nodeId),"Block transaction ",\
			# 	self.bastarBlock.transactions )
			if r == self.getEmptyHash():
				print("Added block was empty")
			self.bastarBlock.state = config.TENTATIVE_CONSENSUS
			self.blockChain.append(self.bastarBlock)

		newEvent = Event(ev.evTime + 1,
							ev.evTime + 1,
							EventType.BLOCK_PROPOSER_SORTITION_EVENT,
							noMessage(),
							config.TIMEOUT_NOT_APPLICABLE,
							self,
							self,
							ev.roundNumber + 1,
							0)

		eventQ.add(newEvent)		
		

	def BAstartCountVoteThree(self,ev):
		print(self.nodeId, " BA* Count Vote two is executing in step = ",\
				ev.stepNumber)
		step = ev.stepNumber
		r,block = self.CountVotes(config.T_STEP_REDUCTION_STEP_TWO, ev) 
		if r is config.TIMEOUT:
			if self.commonCoin(ev.roundNumber,step,config.tou_step) == 0:
				r = self.bastarBlockHash
				block = self.bastarBlock
			else:
				r = self.getEmptyHash()
				block = self.getEmptyBlock()

		step += 1
		self.BAstartCommitteVote(ev,ev.roundNumber,step,config.tou_step,\
								INVOKE_BA_START_COUNT_VOTE_ONE,r,block)


	def commonCoin(self,roundNumber,stepNumber,touStep):
		minHash = 2**512
		#msgs = self.incomingBlockVoteMsg
		msgs = []

		if (roundNumber,stepNumber) in self.incomingBlockVoteMsg:
			msgs = self.incomingBlockVoteMsg[(roundNumber,stepNumber)]
		
		# nprocs = cpu_count()
		# pool = Pool(nprocs)
		# results = list(pool.map(partial(self.ProcessMsg, ctx_Weight), msgs))
		# print(self.nodeId, " processed ", len(results), " \
		# block vote messages for common coin")
		# pool.close()

		while True:
			try:
				m = msgs.pop()
				votes, value, sortHasg, pk, block = self.ProcessMsg(ctx_Weight,m)
				for j in range(0,votes):
					h = H(str(sortHash) + str(j)) 
					if int(h,16) < minHash:
						minHash = h
			except:
				print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
				break

		if (roundNumber,stepNumber) in self.incomingBlockVoteMsg:
			self.incomingBlockVoteMsg[(roundNumber,stepNumber)].clear()

		return minHash % 2


	def computePriority(self,resp):
		hashList = []
		for i in range(resp.j):
			inp = str(resp.hashValue) + str(i + 1)
			sha = hashlib.sha256(inp.encode())
			hashList.append(sha.hexdigest())
		return int(min(hashList),16)

	def getEmptyHash(self):
		prevBlock = self.blockChain[len(self.blockChain) - 1]
		prevBlockHash = H(prevBlock)
		return H(Block("Empty", prevBlockHash))

	def getEmptyBlock(self):
		prevBlock = self.blockChain[len(self.blockChain) - 1]
		prevBlockHash = H(prevBlock)
		return Block("Empty", prevBlockHash)


	def proposePriority(self,ev): # round K

		self.peerList.clear()
		self.sentGossipMessages.clear()
		

		self.incomingBlockVoteMsg.clear()

		# REcovery protocol to handle inconsistent blockchains of nodes
		# block_to_add = None
		# for node in allNodes:
		# 	if node.blockChain[-1].state == FINAL_CONSENSUS:
		# 		block_to_add = node.blockChain[-1]
		
		# if block_to_add is not None:
		# 	for i in range(len(allNodes)):
		# 		allNodes[i].blockChain[-1] = block_to_add
		# else:
		# 	prevHash = allNodes[0].blockChain[-1].prevBlockHash
		# 	newBlock = Block("Empty",prevHash)
		# 	newBlock.state = FINAL_CONSENSUS 
		# 	for i in range(len(allNodes)):
		# 		allNodes[i].blockChain[-1] = newBlock

		# TODO clear all list from all keys

		# if ev.getRoundStepTuple() in self.incomingBlockVoteMsg:
		# 	self.incomingBlockVoteMsg[ev.getRoundStepTuple()].clear()

		self.incomingProposedBlocks.clear()

		self.genNextSeed(ev.roundNumber,ev.stepNumber) # self.seed gets updated
		retval = Sortition(self.secretkey,self.seed,self.tau,"hello",self.w,self.W)
		resp = srtnResp(retval[0],retval[1],retval[2])
		if resp.j > 0:
			#print(BOLDBLUE("=>"),self.nodeId,"sortition-priority-round",str(ev.roundNumber),RESET(""))
			minPrio = self.computePriority(resp) # min --> max in algorand
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
							config.PRIORITY_GOSSIP_TIMEOUT,
							self,
							self,
							ev.roundNumber,
							ev.stepNumber)

			eventQ.add(newEvent)

		newEvent = Event(ev.refTime + config.PRIORITY_GOSSIP_TIMEOUT + 1,
							ev.evTime + config.PRIORITY_GOSSIP_TIMEOUT + 1,
							EventType.SELECT_TOP_PROPOSER_EVENT,
							noMessage(),
							config.TIMEOUT_NOT_APPLICABLE,
							self,
						 	self,
							ev.roundNumber,
						 	ev.stepNumber)

		eventQ.add(newEvent)

	def hangForever(self):
		print("Hang Forever called")
