#ifndef __SUBMACHINE_H_
#define __SUBMACHINE_H_

#ifdef __cplusplus
extern "C" {
#endif


#include "main.h"
#include "motor.h"

extern struct SubMachine {
   char name[11];
   int id;
   struct Motor motors[3];
} submachine;

struct SubMachine initializeHandler(void);
struct SubMachine initializeDrill(void);
struct SubMachine initializeMill(void);
struct SubMachine initializeLathe(void);

void printSubMachineDetails(struct SubMachine submachine);

struct Motor * getMotorById(struct SubMachine *submachine_ptr, int id);

void processInstruction(uint8_t instData[28], struct SubMachine *submachine_ptr);

int getDirectionBit(int initByte);

int getMotorIdBits(int initByte);

int isComplete(struct SubMachine submachine);

#endif // __SUBMACHINE_H_
