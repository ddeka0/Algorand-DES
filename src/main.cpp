#include <bits/stdc++.h>
#include "include/node.h"
#include "include/network_util.h"
vector<shared_ptr<Node>> all_nodes;

std::multiset<Event> EventQ;

int delays[MAX_NODES][MAX_NODES];

void executeEvent(const Event &event)
{
	auto targetNode = event.targetNode;
	int eventType = event.evType;
	int eventTime = event.eventTime;
	int refTime = event.refTime;
	
	cout <<"got eventType = " << eventType <<" for targetNode "<<targetNode->nodeId << endl;
	cout <<"got eventTime = " << eventTime <<" for targetNode "<<targetNode->nodeId << endl;
	cout <<"got refTime = " << refTime <<" for targetNode "<<targetNode->nodeId << endl;

	switch (eventType)
	{
	case BLOCK_PROPOSER_SORTITION_EVENT:
	{
		targetNode->proposePriority(event);
	}
	break;
	case GOSSIP_EVENT:
	{
		targetNode->sendGossip(event);
	}
	break;
	case SELECT_TOP_PROPOSER_EVENT:
	{
		targetNode->selectTopProposer(event);
	}
	break;
	default:
	{
		cout << "This is not a valid event type" << endl;
	}
	break;
	}
}

int main()
{
	srand(time(NULL));

	shared_ptr<Node> A = shared_ptr<Node>(new Node(1));
	shared_ptr<Node> B = shared_ptr<Node>(new Node(2));
	shared_ptr<Node> C = shared_ptr<Node>(new Node(3));
	shared_ptr<Node> D = shared_ptr<Node>(new Node(4));

	all_nodes.push_back(A);
	all_nodes.push_back(B);
	all_nodes.push_back(C);
	all_nodes.push_back(D);

	A->peers.push_back(D);
	A->peers.push_back(C);
	B->peers.push_back(C);
	C->peers.push_back(D);

	delays[A->nodeId][D->nodeId] = 2;
	delays[A->nodeId][C->nodeId] = 1;
	delays[B->nodeId][C->nodeId] = 2;
	delays[C->nodeId][D->nodeId] = 3;

	// push all the start events of all the nodes
	for (shared_ptr<Node> &node : all_nodes)
	{
		cout <<"hi"<<endl;
		noMessage msg;
		Event new_event(
			0,								// ref start time
			0,								// event start time
			node,							// where to execute
			msg,							// what to send
			BLOCK_PROPOSER_SORTITION_EVENT,	// type of event
			TIMEOUT_NOT_APPLICABLE,		// timeout if any
			1);								// round number
		
		EventQ.insert(new_event);			// push the event in the heap
	}
	cout <<"Initial EventQ size = "<<EventQ.size() << endl;
	while (true)
	{
		if (EventQ.empty())
		{
			break;
		}
		auto event = EventQ.begin();
		executeEvent(*event);
		EventQ.erase(event);
	}

	cout << "Simulation completed" << endl;
	return 0;
}