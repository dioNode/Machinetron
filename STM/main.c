#include <stdio.h>
#include <windows.h>
#include "motor.h"
#include "config.h"
#include "submachine.h"


int main() {

   float instructions[2][4] = {
      {0, 0, 500, 500},
      {3, 300, 100, 100}
   };

   int initByte = 0b00110000;
   double data[4] = {300, 100, 200};

   struct SubMachine machine = initializeHandler();

   struct Motor *motor_ptr = getMotorById(&machine, 1);

   processCommand(initByte, data, &machine);


   while(1) {
      tickSubMachine(&machine);
      printSubMachineDetails(machine);
      Sleep(LOOP_DELAY_MS);
   }
 
   return 0;
}
