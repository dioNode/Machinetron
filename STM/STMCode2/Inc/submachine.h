#ifndef SUBMACHINE_H_
#define SUBMACHINE_H_

//#include "motor.h"

struct SubMachine {
   char* name;
   int id;
   struct Motor motors[3];
} submachine;

struct SubMachine initializeHandler(void);
struct SubMachine initializeDrill(void);
struct SubMachine initializeMill(void);
struct SubMachine initializeLathe(void);
void printSubMachineDetails(struct SubMachine submachine);
void tickSubMachine(struct SubMachine *submachine_ptr, double delay);
struct Motor * getMotorById(struct SubMachine *submachine_ptr, int id);
void processInstruction(int initByte, double data[4], struct SubMachine *submachine_ptr);
int getDirectionBit(int initByte);
int getMotorIdBits(int initByte);
int isComplete(struct SubMachine submachine);

#endif // SUBMACHINE_H_
