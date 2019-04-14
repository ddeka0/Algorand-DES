#pragma once
#include "include/event.h"

class Node : public std::enable_shared_from_this<Node> {
public:
	int nodeId;
	vector<shared_ptr<Node>> peers;
	bool priority_gossip_found;
	set<int> prioritySet;
	
	Node(int Id) {
		this->nodeId = Id;
		this->priority_gossip_found = false;
	}
	void sendMsg(const Event &event,shared_ptr<Node> dstNode);	
	void sendGossip(const Event &event);
	void selectTopProposer(Event const & event);  // just a dummy second round task
	sortionResponse sortition(); // TODO: modify this sortition function
	int	computePriority();
	void proposePriority(const Event &event);
};