#pragma once
#include <bits/stdc++.h>
using namespace std;

using myVariantType = std::variant<gossipMessage,noMessage>;
class Node;
class Event {
public:
	int refTime;	// start reference time of this type of event
	int eventTime;
	eventType evType;
	int eventTimeOutTime;
	shared_ptr<Node> targetNode;
	myVariantType msgToDeliver;
	int roundNumber;
	
	// add more field if required
	Event(int refTime,int eventTime,shared_ptr<Node> targetNode,
		myVariantType const & msg,
        eventType evType,int timeOut) {

		this->refTime = refTime;
		this->eventTime = eventTime;
		this->targetNode = targetNode;
		this->msgToDeliver = msg;
		this->evType = evType;
		this->eventTimeOutTime = timeOut;
	}
	// overload < operator so that the queue can be sorted atomatically
	bool operator < (const Event & event) const;
};