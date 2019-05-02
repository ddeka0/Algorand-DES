# !/bin/python3
# TODO make incomingBlockVoteMsg as dictionary and index with it (round,step)
from event import Event
from network_utils import*
from multiprocessing import  Pool,cpu_count
from functools import partial
import math

class Node(object):
	def __init__(self, Id, secretkey, publickey, w):
		self.secretkey = secretkey
		self.publickey = publickey
		self.nodeId = Id
		self.peerList = []
		self.w = w
		self.priorityGossipFound = False
		self.priorityList = []
		self.tau = MAX_NODES * 0.1 # 10 percent
		#self.tau = 5  # 10 percent
		self.tau_committee = tou_step  # 20 percent
		self.W = MAX_NODES * (MAX_ALGORAND / 2)
		self.lastGossipMessage = ""
		self.sentGossipMessages = []
		self.blockChain = []
		self.seed = "HASHOFPREVIOUSBLOCK" # TODO: compute hash for different rounds
		# Set Genesis Block
		genesisBlock = Block(GENESIS_BLOCK_CONTENT)
		self.blockChain.append(genesisBlock)

		self.incomingProposedBlocks = []	# this queue will be used for incoming block prop messages
		self.incomingBlockVoteMsg = {}		# this queue will be used for incoming vote block message
		self.bastarBlockHash = None
		self.bastarOutput = None
		self.bastarBlock = None

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
			while randomNodeCnt < GOSSIP_FAN_OUT:
				randomNode = random.choice(allNodes)
				if randomNode != self and (randomNode not in self.peerList):	#DONT select myself
					self.peerList.append(randomNode)
					randomNodeCnt = randomNodeCnt + 1

			for peer in self.peerList:
				if ev.evTime + delays[self.nodeId][peer.nodeId] - ev.refTime <= ev.timeOut:
					self.sendMsg(ev,peer)
				else:
					pass
			self.peerList.clear()
			self.lastGossipMessage = message.__str__() # not very perfect but still stops some messages
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
				print("I am (",self.nodeId,") topProposer and ",MyPriority," is my priority")
				MyPriorityMsg = res[1]

		if IamTopProposer is not None:
			# I need to create a block and gossip to the network
			prevBlock = self.blockChain[len(self.blockChain) - 1]
			prevBlockHash = hashlib.sha256(prevBlock.__str__().encode()).hexdigest()
			thisBlockContent = secrets.randbits(256)

			newBlockPropMsg = BlockProposeMsg(prevBlockHash,thisBlockContent,MyPriorityMsg)

			print(H(newBlockPropMsg.block))

			# Gossip This newBlockPropMsg
			# create a sendBlockPropGossip on myself and return
			newEvent = Event(ev.evTime,
							 ev.evTime,
							 EventType.BLOCK_PROPOSE_GOSSIP_EVENT,
							 newBlockPropMsg,
							 BLOCK_PROPOSE_GOSSIP_TIMEOUT,
							 self,
							 self,
							 ev.roundNumber,
							 ev.stepNumber)

			eventQ.add(newEvent)


		self.priorityGossipFound = False
		self.priorityList.clear()

		newEvent = Event(ev.evTime + BLOCK_PROPOSE_GOSSIP_TIMEOUT + 1,
						ev.evTime + BLOCK_PROPOSE_GOSSIP_TIMEOUT + 1,
						EventType.REDUCTION_COMMITTEE_VOTE_STEP_ONE,
						noMessage(),
						TIMEOUT_NOT_APPLICABLE,
						self,
						self,
						ev.roundNumber,
						ev.stepNumber + 1) # check step 7 in the problem statement for +1

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

			while randomNodeCnt < GOSSIP_FAN_OUT:
				randomNode = random.choice(allNodes)
				if randomNode != self and (randomNode not in self.peerList):	#DONT select myself
					self.peerList.append(randomNode)
					randomNodeCnt = randomNodeCnt + 1

			for peer in self.peerList:
				if ev.evTime + delays[self.nodeId][peer.nodeId] - ev.refTime <= ev.timeOut:
					#print("Block Gossiped to ",peer.nodeId," by ",self.nodeId," at time  = ",ev.evTime)
					self.sendMsg(ev,peer)
				else:
					pass

			self.peerList.clear()
			self.sentGossipMessages.append(message)
		else:
			#print("Block Prop Message Discarded : already sent via this Node [", self.nodeId, "] at time = ",ev.evTime)
			pass

	def reductionCommitteVoteStepOne(self, ev):  # this is happening in 33 sec # step = 1
		# clear the record of outgoing proposed block gossip messages
		# we are going to push new block vote gossip message in this list
		self.sentGossipMessages.clear()

		if len(self.incomingProposedBlocks) == 0:
			#print(self.nodeId ,"Reduction step1 starts and I should vote on an empty block") # TODO implement
			pass
		else:
			# Find block from max priority proposer only and vote on it
			minPrio = 2**300
			maxPropBlockMsg = None
			for propBlockMsg in self.incomingProposedBlocks:
				if propBlockMsg.priorityMsgPayload.priority < minPrio:
					minPrio = propBlockMsg.priorityMsgPayload.priority
					maxPropBlockMsg = propBlockMsg
			# We have got the minBlock (block from max priority)
			self.genNextSeed(ev.roundNumber, ev.stepNumber)  # self.seed gets updated
			retval = Sortition(self.secretkey, self.seed, self.tau_committee, "hello", self.w, self.W)
			# resp = committe sorition result
			resp = srtnResp(retval[0],retval[1],retval[2]) # TODO remove
			if resp.j > 0: # If I have own the committe
				# push a gossip event on myself that will trigger further gossip
				#print(self.nodeId, " Reduction step1 starts and I am a committe member with j = ",resp.j)
				prevBlock = self.blockChain[len(self.blockChain) - 1]
				prevBlockHash = H(prevBlock)
				thisBlockHash = hashlib.sha256(maxPropBlockMsg.block.__str__().encode()).hexdigest()

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
								BLOCK_VOTE_REDUCTION_S1_GOSSIP_TIMEOUT,
								self,
								self,
								ev.roundNumber,
								ev.stepNumber)

				eventQ.add(newEvent)

		# Push the reduction step 1 cound vote event after +3 sec
		newEvent2 = Event(ev.evTime + BLOCK_VOTE_REDUCTION_S1_GOSSIP_TIMEOUT + 1,
						ev.evTime + BLOCK_VOTE_REDUCTION_S1_GOSSIP_TIMEOUT + 1,
						EventType.REDUCTION_COUNT_VOTE_STEP_ONE,
						noMessage(),
						TIMEOUT_NOT_APPLICABLE,
						self,
						self,
						ev.roundNumber,
						ev.stepNumber)

		eventQ.add(newEvent2)

	def sendBlockVoteGossip(self,ev):
		# self has received a proposed block just now
		# update my incomingProposedBlock List and relay further if possible
		# this incomingProposedBlock will be used in the reductionCommitteVoteStepOne() function
		if ev.msgToDeliver not in self.sentGossipMessages:
			message = ev.msgToDeliver

			if ev.getRoundStepTuple() not in self.incomingBlockVoteMsg:
				self.incomingBlockVoteMsg[ev.getRoundStepTuple()]=[]
			self.incomingBlockVoteMsg[ev.getRoundStepTuple()].append(message)

			randomNodeCnt = 0

			while randomNodeCnt < GOSSIP_FAN_OUT:
				randomNode = random.choice(allNodes)
				if randomNode != self and (randomNode not in self.peerList):	#DONT select myself
					self.peerList.append(randomNode)
					randomNodeCnt = randomNodeCnt + 1

			for peer in self.peerList:
				if ev.evTime + delays[self.nodeId][peer.nodeId] - ev.refTime <= ev.timeOut:
					#if ev.stepNumber == REDUCTION_TWO or ev.stepNumber == 3:
					#print("BlockVote Gossiped to ",peer.nodeId," by ",self.nodeId," at time  = ",ev.evTime)
					self.sendMsg(ev,peer)
				else:
					print("More Delay")

			self.peerList.clear()
			self.sentGossipMessages.append(message)
		else:
			#print("Block Prop Message Discarded : already sent via this Node [", self.nodeId, "] at time = ",ev.evTime)
			pass
			#pass



	def ProcessMsg(self, ctxw ,m):
		pk = m.userPk
		signed_m = m.sgnVoteMsg[0] # index for digest sgnVoteMsg is tuple
		msg = m.sgnVoteMsg[1] # index for msg
		block = m.block

		# TODO use fastecdsa

		if not pk.verify(signed_m, str((msg)).encode('utf-8')):
			print("Verification Failed")
			return tuple((0,False,False))
		else:
			roundNumber = msg.roudNumber
			step = msg.step
			sortHash = msg.hashValue
			pi = msg.pi
			hprev = msg.prevBlockHash
			value = msg.thisBlockHash
			if hprev != H(self.blockChain[len(self.blockChain)-1]):
				# print("hprev is" ,hprev)
				# print("from blockchain" ,H(self.blockChain[len(self.blockChain)-1]))
				#printBlockchain()
				print("prev block hash mismatch")
				return tuple((0,False,False,False,False))
			else:
				votes = VerifySort(pk,sortHash,pi,self.seed,self.tau_committee,"hello",ctxw[pk],self.W)
				#print(self.nodeId," vote = ",votes)
				return tuple((votes,value,sortHash,pk,block))
				#return 1

	def printBlockchain(self):
		for bc in self.blockChain:
			print(bc)
	def CountVotes(self, Tstep ,ev):
		counts = {}
		#msgs = self.incomingBlockVoteMsg
		msgs = []
		if ev.getRoundStepTuple() in self.incomingBlockVoteMsg:
			msgs = self.incomingBlockVoteMsg[ev.getRoundStepTuple()]
		#print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",len(msgs))
		#print(self.nodeId," found ",len(msgs)," no of incoming vote messages")
		voters = []
		# TODO parallelize the following while loop

		# nprocs = cpu_count()
		# pool = Pool(nprocs)
		# results = list(Pool(processes=nprocs).map(partial(self.ProcessMsg,ctx_Weight),msgs))
		# pool.close()
		# print(self.nodeId," processed ",len(results)," block vote messages")

		# Clear the incoming VoteMessage list
		# Could be used in the next step again
		#self.incomingBlockVoteMsg.clear()
		
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
				if counts[value] >= math.floor(Tstep * self.tau_committee): # TODO check this condition fully
					#print("found ", counts[value], " expected ", math.floor(Tstep * self.tau_committee))
					return (value,block)
				else:
					#print("found ",counts[value]," expected ",math.floor(Tstep * self.tau_committee))
					pass
			except:
				return (None , None)
		if ev.getRoundStepTuple() in self.incomingBlockVoteMsg:
			self.incomingBlockVoteMsg[ev.getRoundStepTuple()].clear()
		
		# for res in results:
		# 	votes, value, sortHasg, pk, block = res

		# 	if pk in voters or votes == 0:
		# 		continue
		# 	voters.append(pk)
		# 	if value in counts:
		# 		counts[value] += votes
		# 	else:
		# 		counts[value] = votes
		# 	if counts[value] >= math.floor(Tstep * self.tau_committee): # TODO check this condition fully
		# 		#print("found ", counts[value], " expected ", math.floor(Tstep * self.tau_committee))
		# 		return (value,block)
		# 	else:
		# 		#print("found ",counts[value]," expected ",math.floor(Tstep * self.tau_committee))
		# 		pass
		return (None,None)




	def reductionCountVoteStepOne(self,ev):
		#print(self.nodeId ," has started Count Vote in reduction step one")
		#self.CountVotes(T_STEP_REDUCTION_STEP_ONE, ev)
		hBlockOne,block = self.CountVotes(T_STEP_REDUCTION_STEP_ONE,ev)
		#print("Reduction step2 starts...")

		if hBlockOne is TIMEOUT:
			block = self.getEmptyBlock()
			self.reductionCommitteVoteStepTwo(ev,ev.roundNumber,REDUCTION_TWO,tou_step,H(block),block)
		else:
			print(self.nodeId, "Got anough vote for ", hBlockOne)
			self.reductionCommitteVoteStepTwo(ev,ev.roundNumber,REDUCTION_TWO,tou_step,hBlockOne,block)


	def reductionCommitteVoteStepTwo(self,ev,roundNumber, stepNumber, touCommitte, hBlock,block):
		# TODO passing ev or not to pass # anyway its working
		# clearing is important
		self.sentGossipMessages.clear()

		self.genNextSeed(roundNumber, stepNumber)
		retval = Sortition(self.secretkey, self.seed, touCommitte, "hello", self.w, self.W)
		resp = srtnResp(retval[0], retval[1], retval[2])  # TODO remove
		if resp.j > 0:  # If I have own the committe
			# push a gossip event on myself that will trigger further gossip
			print(self.nodeId, " Reduction step2 starts and I am a committe member with j = ", resp.j)
			prevBlock = self.blockChain[len(self.blockChain) - 1]
			prevBlockHash = H(prevBlock)
			thisBlockHash = hBlock  # this could be empty or non empty also

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
							 BLOCK_VOTE_REDUCTION_S2_GOSSIP_TIMEOUT,
							 self,
							 self,
							 roundNumber,
							 stepNumber)  # step = 1

			eventQ.add(newEvent)
		else:
			print(self.nodeId," lose the second round of committe vote")
			pass
		# Push the reduction step 2 cound vote event after +3 sec
		newEvent2 = Event(ev.evTime + BLOCK_VOTE_REDUCTION_S2_GOSSIP_TIMEOUT + 1,
						  ev.evTime + BLOCK_VOTE_REDUCTION_S2_GOSSIP_TIMEOUT + 1,
						  EventType.REDUCTION_COUNT_VOTE_STEP_TWO,
						  noMessage(),
						  TIMEOUT_NOT_APPLICABLE,
						  self,
						  self,
						  roundNumber,
						  stepNumber)  # step = 1
		eventQ.add(newEvent2)

	def reductionCountVoteStepTwo(self,ev):
		#print("Reduction step2 Count Vote started at time ", ev.evTime)
		hBlockTwo,block = self.CountVotes(T_STEP_REDUCTION_STEP_TWO, ev)
		if hBlockTwo == TIMEOUT:
			print(self.nodeId, "Got hBlockTwo TIMEOUT")
			self.bastarBlockHash = self.getEmptyHash()
			self.bastarBlock = self.getEmptyBlock()
		else:
			print(self.nodeId, "Got anough vote for ", hBlockTwo)
			self.bastarBlockHash = hBlockTwo
			self.bastarBlock = block

		self.BAstarPhaseOne(ev,3)


	def BAstarPhaseOne(self,ev,stepNumber):
		#print("BA* phase 1 started step = ",ev.stepNumber)
		self.BAstartCommitteVote(ev,ev.roundNumber,stepNumber,tou_step,INVOKE_BA_START_COUNT_VOTE_ONE,self.bastarBlockHash,self.bastarBlock)


	def BAstartCommitteVote(self,ev,roundNumber,stepNumber,touCommitte,flag,block_hash,block):
		if flag == INVOKE_BA_START_COUNT_VOTE_ONE and stepNumber >= MAX_STEPS:
			return

		# flag will decide which countVote event to push after this committe vote is over
		# TODO passing ev or not to pass # anyway its working
		# clearing is important
		self.sentGossipMessages.clear()

		self.genNextSeed(roundNumber, stepNumber)
		retval = Sortition(self.secretkey, self.seed, touCommitte, "hello", self.w, self.W)
		resp = srtnResp(retval[0], retval[1], retval[2])  # TODO remove
		if resp.j > 0:  # If I have own the committe
			# push a gossip event on myself that will trigger further gossip
			#print(self.nodeId, "BA* step ",stepNumber,"and round =",roundNumber," : selected as committe member with j = ", resp.j)
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
							 BLOCK_VOTE_REDUCTION_S2_GOSSIP_TIMEOUT, # TODO change this timeout or check
							 self,
							 self,
							 roundNumber,
							 stepNumber)

			eventQ.add(newEvent)
		else:
			print(self.nodeId," lose the ",roundNumber," round and ",stepNumber," step of committe vote")
			pass
		# TODO all of the following timeout valus are not correct
		# TODO these are somehow working only
		if flag == INVOKE_BA_START_COUNT_VOTE_ONE:
			# Push the reduction step 2 cound vote event after +3 sec
			newEvent2 = Event(ev.evTime + BA_STAR_GOSSIP_TIMEOUT + 1,
							  ev.evTime + BA_STAR_GOSSIP_TIMEOUT + 1,
							  EventType.BASTAR_COUNT_VOTE_ONE,
							  noMessage(),
							  TIMEOUT_NOT_APPLICABLE,
							  self,
							  self,
							  roundNumber,
							  stepNumber)
			eventQ.add(newEvent2)
		elif flag == INVOKE_BA_START_COUNT_VOTE_TWO:
			# Push the reduction step 2 cound vote event after +3 sec
			newEvent2 = Event(ev.evTime + BLOCK_VOTE_REDUCTION_S2_GOSSIP_TIMEOUT + 1,
							  ev.evTime + BLOCK_VOTE_REDUCTION_S2_GOSSIP_TIMEOUT + 1,
							  EventType.BASTAR_COUNT_VOTE_TWO,
							  noMessage(),
							  TIMEOUT_NOT_APPLICABLE,
							  self,
							  self,
							  roundNumber,
							  stepNumber)
			eventQ.add(newEvent2)
		elif flag == INVOKE_BA_START_COUNT_VOTE_THREE:
			# Push the reduction step 2 cound vote event after +3 sec
			newEvent2 = Event(ev.evTime + BLOCK_VOTE_REDUCTION_S2_GOSSIP_TIMEOUT + 1,
							  ev.evTime + BLOCK_VOTE_REDUCTION_S2_GOSSIP_TIMEOUT + 1,
							  EventType.BASTAR_COUNT_VOTE_THREE,
							  noMessage(),
							  TIMEOUT_NOT_APPLICABLE,
							  self,
							  self,
							  roundNumber,
							  stepNumber)
			eventQ.add(newEvent2)
		elif flag == DO_NOT_INVOKE_ANY_MORE_COUNT_VOTE:
			#print(self.nodeId," Not creating any more count vote step ", ev.roundNumber," ends.")
			pass
		else:
			#print(self.nodeId, " Unknown flag received")
			pass

	def BAstartCountVoteOne(self,ev):
		print(self.nodeId, " BA* Count Vote ONE is executing in step = ",ev.stepNumber)
		step = ev.stepNumber
		r,block = self.CountVotes(T_STEP_REDUCTION_STEP_TWO, ev) # TODO T_STEP check
		if r is TIMEOUT:
			r = self.bastarBlockHash # we are using self.bastarBlockHash instead of block_hash
			#print("BAstartCountVoteOne getting timeout")
			block = self.bastarBlock
		elif r is not self.getEmptyHash():
			for s in range(ev.stepNumber,ev.stepNumber + 3):
				self.BAstartCommitteVote(ev,ev.roundNumber,s,tou_step,DO_NOT_INVOKE_ANY_MORE_COUNT_VOTE,r,block)
			if step == 3:
				self.BAstartCommitteVote(ev,ev.roundNumber,FINAL_STEP,tou_final,DO_NOT_INVOKE_ANY_MORE_COUNT_VOTE,r,block)	# use a committe vote
			#print("This is the final agreed value of hash = ",r," round ends.")

			# Push the next sortion event
			# Push the next sortion event
			# newEvent = Event(ev.evTime + 1,
			# 				 ev.evTime + 1,
			# 				 EventType.BLOCK_PROPOSER_SORTITION_EVENT,
			# 				 noMessage(),
			# 				 TIMEOUT_NOT_APPLICABLE,
			# 				 self,
			# 				 self,
			# 				 ev.roundNumber + 1,
			# 				 0)  # Initial step Number

			# eventQ.add(newEvent)
			self.bastarOutput = r
			self.bastarBlock = block
			newEvent = Event(ev.evTime + 1,
							 ev.evTime + 1,
							 EventType.FINAL_COUNT_VOTE,
							 noMessage(),
							 TIMEOUT_NOT_APPLICABLE,
							 self,
							 self,
							 ev.roundNumber,
							 FINAL_STEP)

			eventQ.add(newEvent)
			return
		else:
			print("Got consesus on empty block")
			print("Need to move forward")

		step += 1
		self.BAstartCommitteVote(ev,ev.roundNumber,step,tou_step,INVOKE_BA_START_COUNT_VOTE_TWO,r,block)


	def BAstartCountVoteTwo(self,ev):
		print(self.nodeId, " BA* Count Vote two is executing in step = ",ev.stepNumber)
		step = ev.stepNumber
		r,block = self.CountVotes(T_STEP_REDUCTION_STEP_TWO, ev)  # TODO T_STEP check
		if r is TIMEOUT:
			r = self.getEmptyHash()
			block = self.getEmptyBlock()
		elif r == self.getEmptyHash():
			for s in range(ev.stepNumber,ev.stepNumber + 3):
				# vote on the empty block
				# send an empty block also
				block = self.getEmptyBlock()
				self.BAstartCommitteVote(ev,ev.roundNumber,step,tou_step,DO_NOT_INVOKE_ANY_MORE_COUNT_VOTE,r,block)
			#print("This is the final agreed value of hash (empty block hash) = ", r," round ends.")

			# Push the Final count vote event
			self.bastarOutput = r
			self.bastarBlock = block
			newEvent = Event(ev.evTime + 1,
							 ev.evTime + 1,
							 EventType.FINAL_COUNT_VOTE,
							 noMessage(),
							 TIMEOUT_NOT_APPLICABLE,
							 self,
							 self,
							 ev.roundNumber,
							 FINAL_STEP)

			eventQ.add(newEvent)
			return

		step += 1
		# Try to vote on a empty block
		self.BAstartCommitteVote(ev,ev.roundNumber,step,tou_step,INVOKE_BA_START_COUNT_VOTE_THREE,r,block)

	def finalCountVote(self,ev):
		r,block = self.CountVotes(T_STEP_REDUCTION_STEP_TWO, ev)  # TODO T_STEP check
		#print("step number shuld be huge", ev.stepNumber)
		if r == self.bastarOutput:
			if r == self.getEmptyHash():
				print("Added block was empty")

			self.blockChain.append(self.bastarBlock)
			print(">>>>>>>>>>>>>[FINAL",str(self.nodeId),"]New Block added with hash = ",H(self.bastarBlock), " in round = ",ev.roundNumber , " ev time " ,ev.evTime )
			
			# add final flag later
		else:
			print(">>>>>>>>>>>>>[TENTATIVE",str(self.nodeId)," ]New Block added with hash = ", H(self.bastarBlock), " in round = ",ev.roundNumber , " ev time " , ev.evTime)
			if r == self.getEmptyHash():
				print("Added block was empty")
			self.blockChain.append(self.bastarBlock)
			# if r == self.getEmptyHash():
			# 	print("Added block was empty")
			# elif r == None:
			# 	print("#########################")
			# add tentative flag later

		# newEvent = Event(ev.evTime + 1,
		# 					ev.evTime + 1,
		# 					EventType.BLOCK_PROPOSER_SORTITION_EVENT,
		# 					noMessage(),
		# 					TIMEOUT_NOT_APPLICABLE,
		# 					self,
		# 					self,
		# 					ev.roundNumber + 1,
		# 					0)

		#eventQ.add(newEvent)		
		

	def BAstartCountVoteThree(self,ev):
		print(self.nodeId, " BA* Count Vote two is executing in step = ",ev.stepNumber)
		step = ev.stepNumber
		r,block = self.CountVotes(T_STEP_REDUCTION_STEP_TWO, ev)  # TODO T_STEP check
		if r is TIMEOUT:
			if self.commonCoin(ev.roundNumber,step,tou_step) == 0:
				r = self.bastarBlockHash
				block = self.bastarBlock
			else:
				r = self.getEmptyHash()
				block = self.getEmptyBlock()

		step += 1
		self.BAstartCommitteVote(ev,ev.roundNumber,step,tou_step,INVOKE_BA_START_COUNT_VOTE_ONE,r,block)


	def commonCoin(self,roundNumber,stepNumber,touStep):
		minHash = 2**512
		#msgs = self.incomingBlockVoteMsg
		msgs = []
		if (roundNumber,stepNumber) in self.incomingBlockVoteMsg:
			msgs = self.incomingBlockVoteMsg[(roundNumber,stepNumber)]
		nprocs = cpu_count()
		pool = Pool(nprocs)
		results = list(pool.map(partial(self.ProcessMsg, ctx_Weight), msgs))
		print(self.nodeId, " processed ", len(results), " block vote messages for common coin")
		pool.close()

		#self.incomingBlockVoteMsg.clear()
		if (roundNumber,stepNumber) in self.incomingBlockVoteMsg:
			self.incomingBlockVoteMsg[(roundNumber,stepNumber)].clear()

		for res in results:
			votes, value,sortHash, pk,block = res
			for j in range(0,votes):
				h = H(str(sortHash) + str(j))  # TODO check the type of sortHash
				if int(h,16) < minHash:
					minHash = h

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


	def proposePriority(self,ev):

		self.peerList.clear()
		self.sentGossipMessages.clear()
		self.incomingBlockVoteMsg.clear()

		# TODO clear all list from all keys

		# if ev.getRoundStepTuple() in self.incomingBlockVoteMsg:
		# 	self.incomingBlockVoteMsg[ev.getRoundStepTuple()].clear()

		self.incomingProposedBlocks.clear()

		self.genNextSeed(ev.roundNumber,ev.stepNumber) # self.seed gets updated
		retval = Sortition(self.secretkey,self.seed,self.tau,"hello",self.w,self.W)
		resp = srtnResp(retval[0],retval[1],retval[2])
		if resp.j > 0:
			print(self.nodeId, " I am a possible proposer")
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
							PRIORITY_GOSSIP_TIMEOUT,
							self,
							self,
							ev.roundNumber,
							ev.stepNumber)

			eventQ.add(newEvent)

		# Push a special event at time +4 seconds
		# in that event this node will decide whether it is top proposer of not
		# and then if true, it will propose a block
		newEvent = Event(ev.refTime + PRIORITY_GOSSIP_TIMEOUT + 1,
							ev.evTime + PRIORITY_GOSSIP_TIMEOUT + 1,
							EventType.SELECT_TOP_PROPOSER_EVENT,
							noMessage(),
							TIMEOUT_NOT_APPLICABLE,
							self,
						 	self,
							ev.roundNumber,
						 	ev.stepNumber)

		eventQ.add(newEvent)

	def hangForever(self):
		print("Hang Forever called")

	def printStorage(self):
		print("size of incomingProposedBlocks[] = ",len(self.incomingProposedBlocks))
		print("size of sentGossipMessages[] = ", len(self.sentGossipMessages))
		print("size of priorityList[] = ", len(self.priorityList))
		print("size of incomingBlockVoteMsg[] = ", len(self.incomingBlockVoteMsg))
