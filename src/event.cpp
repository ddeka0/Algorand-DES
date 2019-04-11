#include "include/event.h"
bool Event::operator < (const Event & event) const {
    return eventTime < event.eventTime;
}