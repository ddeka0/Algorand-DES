#pragma once
#include <bits/stdc++.h>

#define GOSSIP_EVENT	0
#define DECIDE_EVENT	1
#define GOSSIP_TIMEOUT 	6
#define MAX_NODES       100
// 
// add more function and data types // #defines only


class sortionResponse {
public:
	int hash;
	int pi;
	int j
};

class gossipMessage {
public:
	int gossipType;
	int roundNumber;
	int hashOutput;
	int subUserIndex;
	int priority;
};

