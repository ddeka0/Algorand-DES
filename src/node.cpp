#include "include/node.h"
#include "include/network_util.h"

extern int delays[][MAX_NODES];

extern std::set<Event> EventQ;

void Node::sendMsg(const Event &event,shared_ptr<Node> dstNode) {
    Event new_event(event.refTime,
                    event.eventTime + delays[this->nodeId][dstNode->nodeId],
                    dstNode,
                    event.msgToDeliver,
                    event.eventType,
                    event.eventTimeOutTime);

    EventQ.insert(new_event);
    cout << "Msg sent to (gossip message) " << dstNode->nodeId << endl;
}

void Node::sendGossip(const Event &event) {
    cout <<"Message received at "<<this->nodeId <<"["<<event.msgToDeliver<<"]"<< endl;
    this->gossip_found = true;
    for(auto &peer:peers) {
        if( ((event.eventTime + delays[this->nodeId][peer->nodeId]) - event.refTime) <= event.eventTimeOutTime ) {
            sendMsg(event,peer);
        }
    }
}
void Node::decide() {
    if(this->gossip_found) {
        cout <<"Round 2 has started "<< this->nodeId <<" has decided" << endl;
        this->decide_event_started = true;
    }
}