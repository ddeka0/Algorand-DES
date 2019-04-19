#include "include/node.h"
#include "include/network_util.h"

extern int delays[][MAX_NODES];

extern std::multiset<Event> EventQ;

void Node::sendMsg(const Event &event, shared_ptr<Node> dstNode)
{
	Event new_event(event.refTime,
					event.eventTime + delays[this->nodeId][dstNode->nodeId],
					dstNode,
					event.msgToDeliver,
					event.evType,
					event.eventTimeOutTime,
					event.roundNumber);

	EventQ.insert(new_event);
	
	cout <<"**pushed an GOSSIP_EVENT at time "
		<<event.eventTime + delays[this->nodeId][dstNode->nodeId]<< endl;
	
	cout << "Msg sent to (gossip message) " << dstNode->nodeId << endl;
}

void Node::sendGossip(const Event &event)
{
	cout <<"Round Number "<<event.roundNumber<<endl;
	cout << "Executing sendGossip event at " << this->nodeId << endl;
	cout << "Message is : "<<endl;
	
	// TODO add if else condition for each type of message

	gossipMessage msg = std::any_cast<gossipMessage>(event.msgToDeliver);
	msg.Print();
	
	this->priority_gossip_found = true; // at least it has one priority value

	if(msg.gossipType == PRIORITY_GOSSIP) {
		prioritySet.insert(msg.priority);
	}

	for (auto &peer : peers)
	{
		if (((event.eventTime + delays[this->nodeId][peer->nodeId]) -
			 event.refTime) <= event.eventTimeOutTime)
		{
			sendMsg(event, peer);
		}
	}
	cout << endl;
}

void Node::selectTopProposer(Event const &event)
{
	cout <<"Round Number "<<event.roundNumber<<endl;
	if (this->priority_gossip_found)
	{
		int topProposer = *prioritySet.begin();
		cout << nodeId << " selects " << topProposer << " as topProposer" << endl;
	}
	this->priority_gossip_found = false;
	
	prioritySet.clear();
	
	// dummy algorand previous round is over
	// start a new round (push sortition event again)

	const auto wptr = std::shared_ptr<Node>( this, [](Node*){} );
	noMessage msg;
	Event new_event(event.eventTime + 1,
					event.eventTime + 1,
					shared_from_this(),
					msg,
					BLOCK_PROPOSER_SORTITION_EVENT,
					TIMEOUT_NOT_APPLICABLE,
					event.roundNumber + 1);
	EventQ.insert(new_event);
	cout << endl;
}

sortionResponse Node::sortition()
{
	sortionResponse resp;
	resp.hash = 1;
	resp.pi = 2;
	resp.j = 10;
	return resp;
}

int Node::computePriority()
{
	// calculate sha for j number of times
	return rand() % MAX_NODES;
}

void Node::proposePriority(const Event &event)
{
	cout <<"Round Number "<<event.roundNumber<<endl;
	cout << "Executing proposePriority event at " << nodeId << endl;
	sortionResponse resp = sortition();
	
	if (resp.j > 0) // sortition wining condition
	{
		int minn = 100000;
		for (int i = 0; i < resp.j; i++)
		{
			minn = min(computePriority(), minn);
		}

		gossipMessage msg(
			PRIORITY_GOSSIP,
			event.roundNumber,
			resp.hash,
			resp.j,
			minn);

		const auto wptr = std::shared_ptr<Node>( this, [](Node*){} );
		
		Event new_event(
			event.refTime,			 // ref start time
			event.eventTime,		 // event start time
			shared_from_this(),					 // where to execute
			msg,					 // what to send
			GOSSIP_EVENT,			 // type of event
			PRIORITY_GOSSIP_TIMEOUT, // timeout if any

			event.roundNumber);		 // round number
		EventQ.insert(new_event); // push the event in the heap
		cout <<"pushed an GOSSIP_EVENT at time "<<event.eventTime<< endl;
		
		// push the next special event also
		Event new_event2(event.refTime + PRIORITY_GOSSIP_TIMEOUT + 1,
						 event.eventTime + PRIORITY_GOSSIP_TIMEOUT + 1,
						 shared_from_this(),
						 msg,
						 SELECT_TOP_PROPOSER_EVENT,
						 TIMEOUT_NOT_APPLICABLE,
						 event.roundNumber); // we are still in the same round

		EventQ.insert(new_event2);
		cout <<"pushed an SELECT_TOP_PROPOSER_EVENT at time "
			<<event.eventTime + PRIORITY_GOSSIP_TIMEOUT << endl << endl;
	}
}
