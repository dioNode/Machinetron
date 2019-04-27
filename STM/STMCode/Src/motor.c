#include "motor.h"
#include "config.h"
#include "stm32f1xx_hal.h"
#include "main.h"
#include <stdio.h>
#include <math.h>
#include <string.h>

/**
 * Initialises the motor stepsize pins
 * @param[out] motor_array An array containing all the motors
 */
void initMotorsStepSize(struct Motor motors_array[], int len) {
	int stepSelector;
	for(int i = 0; i < len; i++) {
		if(strncmp(motors_array[i].type, "STEP", 4) == 1) {
			stepSelector = getStepSizeSelector(motors_array[i].stepsize);
			switch(motors_array[i].id) {
			case 1:
				HAL_GPIO_WritePin(ST1MS1_GPIO_Port,ST1MS1_Pin, (GPIO_PinState)((stepSelector & (1 << 0)) >> 0));
				HAL_GPIO_WritePin(ST1MS2_GPIO_Port,ST1MS1_Pin, (GPIO_PinState)((stepSelector & (1 << 1)) >> 1));
				HAL_GPIO_WritePin(ST1MS3_GPIO_Port,ST1MS1_Pin, (GPIO_PinState)((stepSelector & (1 << 2)) >> 2));
				break;
			case 2:
				HAL_GPIO_WritePin(ST2MS1_GPIO_Port,ST2MS1_Pin, (GPIO_PinState)((stepSelector & (1 << 0)) >> 0));
				HAL_GPIO_WritePin(ST2MS2_GPIO_Port,ST2MS1_Pin, (GPIO_PinState)((stepSelector & (1 << 1)) >> 1));
				HAL_GPIO_WritePin(ST2MS3_GPIO_Port,ST2MS1_Pin, (GPIO_PinState)((stepSelector & (1 << 2)) >> 2));
				break;
			case 3:
				HAL_GPIO_WritePin(ST3MS1_GPIO_Port,ST3MS1_Pin, (GPIO_PinState)((stepSelector & (1 << 0)) >> 0));
				HAL_GPIO_WritePin(ST3MS2_GPIO_Port,ST3MS1_Pin, (GPIO_PinState)((stepSelector & (1 << 1)) >> 1));
				HAL_GPIO_WritePin(ST3MS3_GPIO_Port,ST3MS1_Pin, (GPIO_PinState)((stepSelector & (1 << 2)) >> 2));
				break;	
			//default:
				//Error_Handler();
			}
		} else {
			// Set the spinning direction for the DC motors
			HAL_GPIO_WritePin(ST2MS1_GPIO_Port,ST2MS1_Pin, GPIO_PIN_RESET);
			HAL_GPIO_WritePin(ST2MS2_GPIO_Port,ST2MS1_Pin, GPIO_PIN_SET);
		}			
	}
}

/**
 * Function to return the MS3,MS2,MS1, number based on the stepsize selected for the motor
 * @param[out] stepSize The size of the step inverted (1,2,4,8,16)
 */
int getStepSizeSelector(int stepSize) {
	int sizeSelector;
	// Switch statement to set the correct value to sizeSelector
	switch(stepSize) {
		case 1 :
			sizeSelector = 0;
			break;
		case 2 :
			sizeSelector = 1;
			break;
		case 4 :
			sizeSelector = 2;
			break;
		case 8 :
			sizeSelector = 3;
			break;
		case 16 :
			sizeSelector = 7;
			break;
		default:
			sizeSelector = 0;
	}
	return sizeSelector;
}

/**
 * Steps the motor towards its target direction once.
 * @param[out] motor_ptr The pointer for the motor.
 */
void stepMotor(struct Motor *motor_ptr) {
  int targetStep = motor_ptr -> targetStep;
  // Step towards the direction of target
  
  if (motor_ptr -> currentStep < targetStep || motor_ptr -> targetStep == INF_VAL)
    motor_ptr -> currentStep += 1;
    // TODO step forward
    
  else if (motor_ptr -> currentStep > targetStep)
    motor_ptr -> currentStep -= 1;
    // TODO step backwards

}

/**
 * Sets the correct targets for the motor. This requires converting
 * displacement values to number of steps.
 * @param[out]  motor_ptr   The pointer for the motor you want to set targets for.
 * @param[in]   disp        The displacement you want to reach (mm).
 * @param[in]   startSpeed  The speed which you start moving at (mm/s).
 * @param[in]   endSpeed    The speed which you stop moving at when you reach target (mm/s).
 */
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

/**
 * Prints the details about the current motor.
 * @param[out] motor  The motor you want information about.
 */
void printMotorDetails(struct Motor motor) {
   printf("%s %d / %d\n", motor.name, motor.targetStep, motor.currentStep);
}

/**
 * Finds the current displacement of your motor (mm or degrees).
 * @param[in] motor The motor you want to read from.
 * @return    The motor's displacement (mm or degrees).
 */
double getCurrentDisplacement(struct Motor motor) {
  return motor.currentStep * motor.dpr / NUM_STEPPER_STEPS;
}

/**
 * Converts the displacement of the motor to step number.
 * @param[in] displacement  The displacement you want to convert.
 * @param[in] motor         The motor you wish to examine.
 * @return  The equivalent number of steps taken to move displacement.
 */
double displacement2steps(double displacement, struct Motor motor) {
  // Special number return same
  if (displacement == INF_VAL) {
    return INF_VAL;
  }
  // Finds the number of steps to get as close as possible to displacement
  int steps = round(displacement * NUM_STEPPER_STEPS / motor.dpr);
  return steps;
}

/**
 * Calculates the number of milliseconds before each step.
 * @param[in] motor The motor being examined.
 * @return  The number of milliseconds before each step for the motor.
 */
double msPerStep(struct Motor motor) {
  // Find number of ms required per step (currentSpeed is in steps per second)
  return 1000 / motor.currentSpeed;
}
