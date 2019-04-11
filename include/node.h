#pragma once
#include "include/event.h"

class Node {
public:
	int nodeId;
	vector<shared_ptr<Node>> peers;
	bool gossip_found;
	bool decide_event_started;
	
	Node(int Id) {
		this->nodeId = Id;
		this->gossip_found = false;
		this->decide_event_started = false;
	}
    void sendMsg(const Event &event,shared_ptr<Node> dstNode);	
	void sendGossip(const Event &event);
    void decide();  // just a dummy second round task
};