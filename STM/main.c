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

   struct Handler handler = initializeHandler();

   printf("%lf\n", instructions[1][3]);
   setTargetDisp(&handler.spinMotor, 500);


   while(1) {
      tickHandler(&handler);
      printHandlerDetails(handler);
      Sleep(LOOP_DELAY_MS);
   }
 
   return 0;
}
