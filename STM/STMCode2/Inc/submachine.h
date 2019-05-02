#ifndef __SUBMACHINE_H_
#define __SUBMACHINE_H_

#ifdef __cplusplus
extern "C" {
#endif

#include "motor.h"
#include "main.h"

extern struct SubMachine {
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
void processInstruction(uint8_t instData[28], struct SubMachine *submachine_ptr);
int getDirectionBit(int initByte);
int getMotorIdBits(int initByte);
int isComplete(struct SubMachine submachine);

#endif // __SUBMACHINE_H_
