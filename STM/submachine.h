#ifndef SUBMACHINE_H_
#define SUBMACHINE_H_

#include "motor.h"

struct SubMachine {
   char* name;
   int id;
   struct Motor motors[3];
} submachine;

struct SubMachine initializeHandler();
void printSubMachineDetails(struct SubMachine submachine);
void tickSubMachine(struct SubMachine *submachine_ptr);
struct Motor * getMotorById(struct SubMachine *submachine_ptr, int id);
void processCommand(int initByte, double data[4], struct SubMachine *submachine_ptr);
int getDirectionBit(int initByte);
int getMotorIdBits(int initByte);

#endif // SUBMACHINE_H_