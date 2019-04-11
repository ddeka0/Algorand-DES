/* 	Debashish Deka
	g++ -std=c++14 des.cpp
	./a.out
*/
#include <bits/stdc++.h>
using namespace std;

int delays[10][10];

class Event; 		// forward declaration
std::set<Event> Set; 	// this will act as a priority queue
			// and store the events maintaining the
			// relative order of time

class Node;
class Event {
public:
	int eventTime;
	shared_ptr<Node> targetNode;
	string msgToDeliver;
	Event(int t,shared_ptr<Node> target,string msg):eventTime(t),targetNode(target),msgToDeliver(msg) {}
	bool operator < (const Event & event) const {
		return eventTime < event.eventTime;
	}
};

class Node {
public:
	int nodeId;
	vector<shared_ptr<Node>> peers;
	queue<string> msgQ;
	
	Node(int Id) : nodeId(Id) {}

	// send message to one peer
	void sendMsg(int eventTime,string msg,shared_ptr<Node> dstNode) {
		Event event(eventTime + delays[this->nodeId][dstNode->nodeId],dstNode,msg);
		Set.insert(event);
	}	
	// send message to all the peers
	void sendMsgToPeer(int eventTime,string msg) {
		for(auto &peer:peers) {
			cout << "msg sent to " << peer->nodeId << endl;
 			sendMsg(eventTime,msg,peer);
		}
	}
	
	// add more functionality when required 

};
void executeEvent(const Event &event) {
	auto targetNode = event.targetNode;
	string msgToDeliver = event.msgToDeliver;
	cout <<"Message received at "<<targetNode->nodeId <<"["<<msgToDeliver<<"]"<< endl;
	targetNode->sendMsgToPeer(event.eventTime,msgToDeliver);
}
int main() {

	// create the nodes 
	auto A = shared_ptr<Node>(new Node(1));
	auto B = shared_ptr<Node>(new Node(2));
	auto C = shared_ptr<Node>(new Node(3));
	auto D = shared_ptr<Node>(new Node(4));

	// set the sending peers 
	A->peers.push_back(B);
	A->peers.push_back(C);
	C->peers.push_back(D);
	D->peers.push_back(B);

	// set the delays in the links
	// these delays will come from the Normal distribution
	delays[A->nodeId][C->nodeId] = 3;
	delays[A->nodeId][B->nodeId] = 8;
	delays[C->nodeId][D->nodeId] = 2;
	delays[D->nodeId][B->nodeId] = 2;

	// create a start event at node A
	// helps us to initiate the system
	Event X(0,A,"Welcome");
	Set.insert(X);

	// loop indefinitely
	while(true) {
		if(Set.empty()) {
			break;
		}
		auto event = Set.begin();
		executeEvent(*event);
		Set.erase(event);
	}

	cout <<"Simulation completed" << endl;
}
