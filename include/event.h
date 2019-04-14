#pragma once
#include <bits/stdc++.h>
#include <any>
#include "include/network_util.h"
#include <memory>

using namespace std;

class Node;
class Event
{
public:
	int refTime; // start reference time of this type of event
	int eventTime;
	eventType evType; // it is an enum
	int eventTimeOutTime;
	shared_ptr<Node> targetNode; // where to execute
	std::any msgToDeliver;		 // handles different types of message
	int roundNumber;

	// add more field if required
	Event(int refTime,
		  int eventTime,
		  shared_ptr<Node> targetNode,
		  std::any msg,
		  eventType evType,
		  int timeOut,
		  int roundNumber)
	{

		this->refTime = refTime;
		this->eventTime = eventTime;
		this->targetNode = targetNode;
		this->msgToDeliver = msg;
		this->evType = evType;
		this->eventTimeOutTime = timeOut;
		this->roundNumber = roundNumber;
	}
	// overload < operator so that the queue can be sorted atomatically
	bool operator<(const Event &event) const;
};