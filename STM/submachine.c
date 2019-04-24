#include "submachine.h"
#include "motor.h"
#include<stdio.h>
#include <windows.h>


struct SubMachine initializeHandler() {
  struct SubMachine handler = {"Handler", 1,
      {{"Spin Motor", 1, 0, 0, 1, 0, 2},
      {"Flip Motor", 5, 23, 0, 1, 0, 0.5},
      {"Shift Motor", 4, 0, 0, 1, 0, 0.1}},
   };
   return handler;
}

void printSubMachineDetails(struct SubMachine submachine) {
  printf("%s: %d/%d %d/%d %d/%d\n", submachine.name, 
    submachine.motors[0].currentStep, submachine.motors[0].targetStep,
    submachine.motors[1].currentStep, submachine.motors[1].targetStep,
    submachine.motors[2].currentStep, submachine.motors[2].targetStep);
}

void tickSubMachine(struct SubMachine *submachine_ptr) {
  for (int motorNum = 0; motorNum < 3; motorNum++) {
    stepMotor(&submachine_ptr -> motors[motorNum]);
  }
}

struct Motor * getMotorById(struct SubMachine *submachine_ptr, int id) {
  struct Motor *motor_ptr;
  for (int motorNum = 0; motorNum < 3; motorNum++) {
    motor_ptr = &submachine_ptr -> motors[motorNum];
    if (motor_ptr -> id == id) {
      return motor_ptr;
    }
  }
  printf("Motor not found\n");
  return NULL;
}

void processCommand(int initByte, double data[4], struct SubMachine *submachine_ptr) {
  // Extract important variables
  int motorID = getMotorIdBits(initByte);
  int direction = getDirectionBit(initByte);
  double targetDisp = data[0];
  double startSpeed = data[1];
  double endSpeed = data[2];
  
  // Flip displacement if direction is negative (0)
  if (direction == 0) {
    targetDisp = -targetDisp;
  }
  // Get the motor pointer
  struct Motor *motor_ptr = getMotorById(submachine_ptr, motorID);
  // Set targets
  setTargets(motor_ptr, targetDisp, startSpeed, endSpeed);

}

int getDirectionBit(int initByte) {
  // Need to read the 5th bit
  initByte = initByte >> 4;
  initByte &= 0b0001;
  return initByte;
}

int getMotorIdBits(int initByte) {
  // Return the leftmost 3 bits
  return initByte >> 5;
}
