#pragma once
#include <bits/stdc++.h>
using namespace std;

#define PRIORITY_GOSSIP_TIMEOUT 3
#define TIMEOUT_NOT_APPLICABLE -1
#define MAX_NODES 100
//
// add more function and data types // #defines only
enum gossipType
{
	PRIORITY_GOSSIP,
	BLOCK_GOSSIP
};

enum eventType
{
	BLOCK_PROPOSER_SORTITION_EVENT,
	GOSSIP_EVENT,
	SELECT_TOP_PROPOSER_EVENT
};

class sortionResponse
{
public:
	int hash;
	int pi;
	int j;
};

class gossipMessage
{
public:
	int gossipType;
	int roundNumber;
	int hashOutput;
	int subUserIndex;
	int priority;
	gossipMessage(int gossipType, int roundNumber, int hashOutput,
				  int subUserIndex, int priority)
	{
		this->gossipType = gossipType;
		this->roundNumber = roundNumber;
		this->hashOutput = hashOutput;
		this->subUserIndex = subUserIndex;
		this->priority = priority;
	}
	void operator()()
	{
		cout << "hash = " << hashOutput << endl;
		cout << "j	 = " << subUserIndex << endl;
		cout << "priority = " << priority << endl;
	}
};
class noMessage
{
public:
	void operator()()
	{
		cout << "This is not a message" << endl;
	}
};
