#ifndef SUBMACHINE_H_
#define SUBMACHINE_H_

#include "motor.h"

struct Handler {
   char* name;
   int id;
   struct Motor spinMotor;
   struct Motor flipMotor;
   struct Motor shiftMotor;
} handler;

struct Handler initializeHandler();
void printHandlerDetails(struct Handler handler);
void tickHandler(struct Handler *handler_ptr);

#endif // SUBMACHINE_H_