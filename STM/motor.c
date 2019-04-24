#include "motor.h"
#include "config.h"
#include <stdio.h>
#include <math.h>

/*
 * Function: stepMotor
 * -------------------
 * steps the motor towards its target direction once
 * 
 * *motor_ptr: the pointer for the motor
 * 
 */

void stepMotor(struct Motor *motor_ptr) {
  int targetStep = motor_ptr -> targetStep;
  // Step towards the direction of target
  if (motor_ptr -> currentStep < targetStep)
    motor_ptr -> currentStep += 1;
  else if (motor_ptr -> currentStep > targetStep)
    motor_ptr -> currentStep -= 1;
}

void setTargets(struct Motor *motor_ptr, double disp, double startSpeed, double endSpeed) {
  // Set target displacements
  int numStepsToTarget = displacement2steps(disp, *motor_ptr);
  setTargetSteps(motor_ptr, numStepsToTarget);
  // Deal with speeds
  // v^2 = u^2 + 2as --> a = (v^2-u^2)/(2s)
  if (disp != 0){
    double acceleration = (pow(startSpeed, 2) - pow(endSpeed, 2)) / (2*disp);
  }
}

void setTargetSteps(struct Motor *motor_ptr, int numSteps) {
  // Sets the target numSteps from the current step
  motor_ptr -> targetStep = motor_ptr -> currentStep + numSteps;
}

void printMotorDetails(struct Motor motor) {
   printf("%s %d / %d\n", motor.name, motor.targetStep, motor.currentStep);
}

double getCurrentDisplacement(struct Motor motor) {
  return motor.currentStep * motor.dpr / NUM_STEPPER_STEPS;
}

double displacement2steps(double displacement, struct Motor motor) {
  // Finds the number of steps to get as close as possible to displacement
  int steps = round(displacement * NUM_STEPPER_STEPS / motor.dpr);
  return steps;
}
