#pragma once
#include <bits/stdc++.h>
#include "include/network_util.h"

using namespace std;

using myVariantType = std::variant<gossipMessage, noMessage>;

struct PrintMessage
{
	void operator()(gossipMessage &msg)
	{
		msg();
	}
	void operator()(noMessage &msg)
	{
		msg();
	}
};
struct getPriority
{
	int operator()(gossipMessage &msg)
	{
		return msg.priority;
	}
	// add more later
};

struct getGossipType
{
	int operator()(gossipMessage &msg)
	{
		return msg.gossipType;
	}
	// add more later
};
class Node;
class Event
{
public:
	int refTime; // start reference time of this type of event
	int eventTime;
	eventType evType; // it is an enum
	int eventTimeOutTime;
	shared_ptr<Node> targetNode; // where to execute
	myVariantType msgToDeliver;  // handles different types of message
	int roundNumber;

	// add more field if required
	Event(int refTime,
		  int eventTime,
		  shared_ptr<Node> targetNode,
		  myVariantType const &msg,
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