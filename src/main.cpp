#include <bits/stdc++.h>
#include "include/node.h"
#include "include/network_util.h"

std::set<Event> EventQ;
vector<shared_ptr<Node>> all_nodes;

int delays[MAX_NODES][MAX_NODES];

void executeEvent(const Event &event)
{
	auto targetNode = event.targetNode;
	int eventType = event.evType;

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

	auto A = shared_ptr<Node>(new Node(1));
	auto B = shared_ptr<Node>(new Node(2));
	auto C = shared_ptr<Node>(new Node(3));
	auto D = shared_ptr<Node>(new Node(4));
	auto E = shared_ptr<Node>(new Node(5));

	all_nodes.push_back(A);
	all_nodes.push_back(B);
	all_nodes.push_back(C);
	all_nodes.push_back(D);
	all_nodes.push_back(E);

	A->peers.push_back(D);
	A->peers.push_back(C);
	B->peers.push_back(C);
	C->peers.push_back(D);
	D->peers.push_back(E);

	delays[A->nodeId][D->nodeId] = 2;
	delays[A->nodeId][C->nodeId] = 1;
	delays[B->nodeId][C->nodeId] = 2;
	delays[C->nodeId][D->nodeId] = 1;
	delays[D->nodeId][B->nodeId] = 2;

	// push all the start events of all the nodes
	for (auto node : all_nodes)
	{
		noMessage msg;
		Event new_event(
			0,								// ref start time
			0,								// event start time
			node,							// where to execute
			msg,							// what to send
			BLOCK_PROPOSER_SORTITION_EVENT,	// type of event
			PRIORITY_GOSSIP_TIMEOUT,		// timeout if any
			1);								// round number
		EventQ.insert(new_event);			// push the event in the heap
	}

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