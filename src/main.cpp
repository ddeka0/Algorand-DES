#include <bits/stdc++.h>
#include "include/node.h"
#include "include/network_util.h"

std::set<Event> EventQ; 	
vector<shared_ptr<Node>> all_nodes;

int delays[MAX_NODES][MAX_NODES];

void decide_all() {
	for(auto & node:all_nodes) {
		node->decide();
	}
}

void executeEvent(const Event &event) {
	auto targetNode = event.targetNode;
	int eventType = event.eventType;
	
	if(eventType == GOSSIP_EVENT) {
		targetNode->sendGossip(event);
	}else if(eventType == DECIDE_EVENT) {
		decide_all();
	}
}

int main() {
	srand(time(NULL));
	auto A = shared_ptr<Node>(new Node(1));
	auto B = shared_ptr<Node>(new Node(2));
	auto C = shared_ptr<Node>(new Node(3));
	auto D = shared_ptr<Node>(new Node(4));

	all_nodes.push_back(A);
	all_nodes.push_back(B);
	all_nodes.push_back(C);
	all_nodes.push_back(D);

	A->peers.push_back(B);
	A->peers.push_back(C);
	C->peers.push_back(D);
	D->peers.push_back(B);

	delays[A->nodeId][C->nodeId] = 3;
	delays[A->nodeId][B->nodeId] = 8;
	delays[C->nodeId][D->nodeId] = 2;
	delays[D->nodeId][B->nodeId] = 2;

	Event X(0,0,A,"Welcome",GOSSIP_EVENT,GOSSIP_TIMEOUT);
	Event Y(6,6,A,"",DECIDE_EVENT,0);

	EventQ.insert(X);
	EventQ.insert(Y);

	while(true) {
		if(EventQ.empty()) {
			break;
		}
		auto event = EventQ.begin();
		executeEvent(*event);
		EventQ.erase(event);
	}

	cout <<"Simulation completed" << endl;
	return 0;
}