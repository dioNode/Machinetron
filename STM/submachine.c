#include "submachine.h"
#include "motor.h"
#include<stdio.h>

struct Handler initializeHandler() {
  struct Handler handler = {"Handler", 1,
      {"Spin Motor", 0, -5, 1, 0, 2},
      {"Flip Motor", 0, -5, 1, 0, 0.5},
      {"Shift Motor", 0, -5, 1, 0, 0.1},
   };
   return handler;
}

void printHandlerDetails(struct Handler handler) {
  printf("%s: %d/%d %d/%d %d/%d\n", handler.name, 
    handler.spinMotor.currentStep, handler.spinMotor.targetStep,
    handler.flipMotor.currentStep, handler.flipMotor.targetStep,
    handler.shiftMotor.currentStep, handler.shiftMotor.targetStep);
}

void tickHandler(struct Handler *handler_ptr) {

  stepMotor(&handler_ptr -> spinMotor);
  stepMotor(&handler_ptr -> flipMotor);
  stepMotor(&handler_ptr -> shiftMotor);

}
