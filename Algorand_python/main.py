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

	for node in allNodes:
		#print("pushed new event")
		newEvent = Event(0,
						0,
						EventType.BLOCK_PROPOSER_SORTITION_EVENT,
						noMessage(),
						TIMEOUT_NOT_APPLICABLE,
						node,
						node,
						1,
						0)	# Initial step Number
		eventQ.add(newEvent)

	#print("Initial eventQ size = ",len(eventQ))

	while(True):
		if len(eventQ) == 0:
			break
		ev = eventQ.pop(0)
		executeEvent(ev)

	print("Simulation completed !")
