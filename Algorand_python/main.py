# !/bin/python3
from node import *
from network_utils import *
import signal
import time

def executeEvent(ev):

	#print("got eventType = ",ev.evType," for targetNode ",ev.targetNode.nodeId)
	#print("got eventTime = ", ev.evTime, " for targetNode ", ev.targetNode.nodeId)
	#print("got refTime = ", ev.refTime, " for targetNode ", ev.targetNode.nodeId)

	eventType = ev.evType
	targetNode = ev.targetNode

	if eventType == EventType.BLOCK_PROPOSER_SORTITION_EVENT:
		targetNode.proposePriority(ev)
	elif eventType == EventType.PRIORITY_GOSSIP_EVENT:
		targetNode.sendPriorityGossip(ev)
	elif eventType == EventType.SELECT_TOP_PROPOSER_EVENT:
		if not targetNode.isAdversary:
			targetNode.selectTopProposer(ev)
		else:
			print("~~~~~~~~~~~~~~~~ I am adversary. I do bad stuff. " , eventType )
			pass
	elif eventType == EventType.BLOCK_PROPOSE_GOSSIP_EVENT:
		targetNode.sendBlockPropGossip(ev)
	elif eventType == EventType.REDUCTION_COMMITTEE_VOTE_STEP_ONE:
		if not targetNode.isAdversary:
			targetNode.reductionCommitteVoteStepOne(ev)
		else:
			print("~~~~~~~~~~~~~~~~ I am adversary. I do bad stuff. " , eventType )
			pass
	elif eventType == EventType.BLOCK_VOTE_GOSSIP_EVENT:
		targetNode.sendBlockVoteGossip(ev)
	elif eventType == EventType.REDUCTION_COUNT_VOTE_STEP_ONE:
		if not targetNode.isAdversary:
			targetNode.reductionCountVoteStepOne(ev)
		else:
			print("~~~~~~~~~~~~~~~~ I am adversary. I do bad stuff. " , eventType )
			pass
	elif eventType == EventType.REDUCTION_COUNT_VOTE_STEP_TWO:
		if not targetNode.isAdversary:
			targetNode.reductionCountVoteStepTwo(ev)
		else:
			print("~~~~~~~~~~~~~~~~ I am adversary. I do bad stuff. " , eventType )
			pass
	elif eventType == EventType.BASTAR_COUNT_VOTE_ONE:
		if not targetNode.isAdversary:
			targetNode.BAstartCountVoteOne(ev)
		else:
			print("~~~~~~~~~~~~~~~~ I am adversary. I do bad stuff. " , eventType )
			pass
	elif eventType == EventType.BASTAR_COUNT_VOTE_TWO:
		if not targetNode.isAdversary:
			targetNode.BAstartCountVoteTwo(ev)
		else:
			print("~~~~~~~~~~~~~~~~ I am adversary. I do bad stuff. " , eventType )
			pass
	elif eventType == EventType.BASTAR_COUNT_VOTE_THREE:
		if not targetNode.isAdversary:
			targetNode.BAstartCountVoteThree(ev)
		else:
			print("~~~~~~~~~~~~~~~~ I am adversary. I do bad stuff. " , eventType )
			pass
	elif eventType == EventType.FINAL_COUNT_VOTE:
		if not targetNode.isAdversary:
			targetNode.finalCountVote(ev)
		else:
			print("~~~~~~~~~~~~~~~~ I am adversary. I do bad stuff. " , eventType )
			pass
	else:
		print("Event Type is not recognised")

def handler(signum, frame):
	print("Simulation terminated manually")
	sys.exit()

if __name__ == "__main__":
	
	signal.signal(signal.SIGINT, handler)

	init_AsymmtericKeys(sk_List,pk_List)
	print("max nodes in Algorand Network ", len(sk_List))
	init_w(ctx_Weight,pk_List)
	for i in range(MAX_NODES):
		allNodes.append(Node(i,sk_List[i],pk_List[i],ctx_Weight[pk_List[i]]))

	#2.3 fail stop adversary
	# for i in range(MAX_NODES):
	# 	random_number = random.randint(1, 1000)
	# 	if random_number < 50 :
	# 		allNodes[i].isAdversary=True
	# 		print("Hi I am adversary",allNodes[i].nodeId)


	#2.3 fail stop adversary
	#for i in range(MAX_NODES):
	#	random_number = random.randint(1, 1000)
	#	if random_number < 50 :
	#		allNodes[i].isByzantine=True
	#		print("Hi I am byzantine",allNodes[i].nodeId)
	

	init_Delays()

	custom_time=0
	for i in range(16):
		custom_time = 400*i 
		for node in allNodes:
			newEvent = Event(custom_time,
							custom_time,
							EventType.BLOCK_PROPOSER_SORTITION_EVENT,
							noMessage(),
							TIMEOUT_NOT_APPLICABLE,
							node,
							node,
							i+1,
							0)
			eventQ.add(newEvent)

	while(True):
		if len(eventQ) == 0:
			break
		ev = eventQ.pop(0)
		executeEvent(ev)
	print("Simulation completed !")