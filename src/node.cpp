#include "include/node.h"
#include "include/network_util.h"

extern int delays[][MAX_NODES];

extern std::set<Event> EventQ;

void Node::sendMsg(const Event &event,shared_ptr<Node> dstNode) {
    Event new_event(event.refTime,
                    event.eventTime + delays[this->nodeId][dstNode->nodeId],
                    dstNode,
                    event.msgToDeliver,
                    event.evType,
                    event.eventTimeOutTime);

    EventQ.insert(new_event);
    cout << "Msg sent to (gossip message) " << dstNode->nodeId << endl;
}

void Node::sendGossip(const Event &event) {
    cout <<"Message received at "<<this->nodeId <<"["<<event.msgToDeliver<<"]"<< endl;
    this->priority_gossip_found = true;
    for(auto &peer:peers) {
        if( ((event.eventTime + delays[this->nodeId][peer->nodeId]) - event.refTime) <= event.eventTimeOutTime ) {
            sendMsg(event,peer);
        }
    }
}
void Node::selectTopProposer(Event const & event) {
    
	if(this->priority_gossip_found) {
		int topProposer = *prioritySet.begin();
		cout << nodeId <<" selects " << topProposer <<" as topProposer" << endl;
    }
	noMessage msg;
	Event new_event(event.refTime + 1,event.eventTime + 1,this,msg,
		BLOCK_PROPOSER_SORTITION_EVENT,
		TIMEOUT_NOT_APPLICABLE);
	
	EventQ.insert(new_event);
}

sortionResponse Node::sortition() {
    sortionResponse resp;
    resp.hash = 1;
    resp.pi = 2;
    resp.j = rand()%MAX_NODES;
    return resp;
}
int Node::computePriority() {
    // calculate sha for j number of times
    return rand()%MAX_NODES;
}

void Node::proposePriority(const Event &event) {
	sortionResponse resp = sortition();
	if(resp.j > 0) {
		int minn = 100000;
		for(int i = 0;i<resp.j;i++) {
			minn = min(computePriority(),minn);
		}

		gossipMessage msg(PRIORITY_GOSSIP,event.roundNumber,resp.hash,
			resp.j,minn);
		Event new_event(event.refTime + 1,event.eventTime + 1,this,msg,GOSSIP_EVENT,
			PRIORITY_GOSSIP_TIMEOUT);
		EventQ.insert(new_event);


		Event new_event2(event.refTime + PRIORITY_GOSSIP_TIMEOUT,
			event.eventTime + PRIORITY_GOSSIP_TIMEOUT,this,msg,
			SELECT_TOP_PROPOSER_EVENT,
			TIMEOUT_NOT_APPLICABLE);

		EventQ.insert(new_event2);
	}
}

