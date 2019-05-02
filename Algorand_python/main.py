# !/bin/python3
from node import *
from network_utils import *


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
		targetNode.selectTopProposer(ev)
	elif eventType == EventType.BLOCK_PROPOSE_GOSSIP_EVENT:
		targetNode.sendBlockPropGossip(ev)
	elif eventType == EventType.REDUCTION_COMMITTEE_VOTE_STEP_ONE:
		targetNode.reductionCommitteVoteStepOne(ev)
	elif eventType == EventType.BLOCK_VOTE_GOSSIP_EVENT:
		targetNode.sendBlockVoteGossip(ev)
	elif eventType == EventType.REDUCTION_COUNT_VOTE_STEP_ONE:
		targetNode.reductionCountVoteStepOne(ev)
	elif eventType == EventType.REDUCTION_COUNT_VOTE_STEP_TWO:
		targetNode.reductionCountVoteStepTwo(ev)
	elif eventType == EventType.BASTAR_COUNT_VOTE_ONE:
		targetNode.BAstartCountVoteOne(ev)
	elif eventType == EventType.BASTAR_COUNT_VOTE_TWO:
		targetNode.BAstartCountVoteTwo(ev)
	elif eventType == EventType.BASTAR_COUNT_VOTE_THREE:
		targetNode.BAstartCountVoteThree(ev)
	elif eventType == EventType.FINAL_COUNT_VOTE:
		targetNode.finalCountVote(ev)
	else:
		print("Event Type is not recognised")

if __name__ == "__main__":

	init_AsymmtericKeys(sk_List,pk_List)

	print("max nodes in Algorand Network ", len(sk_List))

	init_w(ctx_Weight,pk_List)

	for i in range(MAX_NODES):
		allNodes.append(Node(i,sk_List[i],pk_List[i],ctx_Weight[pk_List[i]]))

	init_Delays()



	#print(delays)
	custom_time=0
	for i in range(10):
		custom_time = 400*i 
		for node in allNodes:
			#print("pushed new event")
			newEvent = Event(custom_time,
							custom_time,
							EventType.BLOCK_PROPOSER_SORTITION_EVENT,
							noMessage(),
							TIMEOUT_NOT_APPLICABLE,
							node,
							node,
							i+1,
							0)	# Initial step Number
			eventQ.add(newEvent)

	#print("Initial eventQ size = ",len(eventQ))

	while(True):
		if len(eventQ) == 0:
			break
		#print("*************************************")
		# for evn in eventQ:
		# 	print(evn)
		
		ev = eventQ.pop(0)
		# if ev.evType != EventType.BLOCK_PROPOSE_GOSSIP_EVENT and  ev.evType != EventType.PRIORITY_GOSSIP_EVENT and ev.evType != EventType.BLOCK_VOTE_GOSSIP_EVENT:
		# 	input("Press to unblock")
		
		executeEvent(ev)

	print("Simulation completed !")
