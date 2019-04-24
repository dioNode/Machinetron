#ifndef SUBMACHINE_H_
#define SUBMACHINE_H_

#include "motor.h"

struct SubMachine {
   char* name;
   int id;
   struct Motor motors[3];
} submachine;

struct SubMachine initializeHandler();
struct SubMachine initializeDrill();
struct SubMachine initializeMill();
struct SubMachine initializeLathe();
void printSubMachineDetails(struct SubMachine submachine);
void tickSubMachine(struct SubMachine *submachine_ptr);
struct Motor * getMotorById(struct SubMachine *submachine_ptr, int id);
void processCommand(int initByte, double data[4], struct SubMachine *submachine_ptr);
int getDirectionBit(int initByte);
int getMotorIdBits(int initByte);
int isComplete(struct SubMachine submachine);

#endif // SUBMACHINE_H_