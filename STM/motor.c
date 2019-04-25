#include "motor.h"
#include "config.h"
#include <stdio.h>
#include <math.h>
#include <windows.h>

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
  if (motor_ptr -> currentStep < targetStep || motor_ptr -> targetStep == INF_VAL)
    motor_ptr -> currentStep += 1;
  else if (motor_ptr -> currentStep > targetStep)
    motor_ptr -> currentStep -= 1;
}

void setTargets(struct Motor *motor_ptr, double disp, double startSpeed, double endSpeed) {
  // Set target displacements
  motor_ptr -> targetStep = displacement2steps(disp, *motor_ptr);
  // Deal with speeds
  // v^2 = u^2 + 2as --> a = (v^2-u^2)/(2s)
  int startStepSpeed = displacement2steps(startSpeed, *motor_ptr);
  int endStepSpeed = displacement2steps(endSpeed, *motor_ptr);
  if (disp != 0){
    double accelerationStep = (pow(startStepSpeed, 2) - pow(endStepSpeed, 2)) / (2*disp);
    motor_ptr -> currentSpeed = startStepSpeed;
    motor_ptr -> acceleration = accelerationStep;
  }
}

void printMotorDetails(struct Motor motor) {
   printf("%s %d / %d\n", motor.name, motor.targetStep, motor.currentStep);
}

double getCurrentDisplacement(struct Motor motor) {
  return motor.currentStep * motor.dpr / NUM_STEPPER_STEPS;
}

double displacement2steps(double displacement, struct Motor motor) {
  // Special number return same
  if (displacement == INF_VAL) {
    return INF_VAL;
  }
  // Finds the number of steps to get as close as possible to displacement
  int steps = round(displacement * NUM_STEPPER_STEPS / motor.dpr);
  return steps;
}

double msPerStep(struct Motor motor) {
  // Find number of ms required per step (currentSpeed is in steps per second)
  return 1000 / motor.currentSpeed;
}
