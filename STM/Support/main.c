#include <stdio.h>
#include <windows.h>
#include "motor.h"
#include "config.h"
#include "submachine.h"

int main() {

   int initByte = 0b00110000;
   double data[4] = {300, 100, 200};

   int initByte2 = 0b01100000;

   struct SubMachine machine = initializeDrill();

   processInstruction(initByte, data, &machine);
   processInstruction(initByte2, data, &machine);

   printf("COmplete %d\n", isComplete(machine));

   while(1) {
      tickSubMachine(&machine, LOOP_DELAY_MS);
      printSubMachineDetails(machine);
      Sleep(LOOP_DELAY_MS);
   }
 
   return 0;
}
