#include "motor.h"
#include "config.h"
#include "stm32f1xx_hal.h"
#include "main.h"
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>

#include "usart.h"


/**
 * Initialises the motor stepsize pins
 * @param[out] motor_array An array containing all the motors
 */
void initMotorsStepSize(struct Motor motors_array[], int len) {
	int stepSelector;
	for(int i = 0; i < len; i++) {
		if(strcmp(motors_array[i].type, "STEP") == 0) {
			stepSelector = getStepSizeSelector(motors_array[i].stepsize);
			switch(motors_array[i].id) {
			case 1:
				HAL_GPIO_WritePin(ST1MS1_GPIO_Port,ST1MS1_Pin, (GPIO_PinState)((stepSelector & (1 << 0)) >> 0));
				HAL_GPIO_WritePin(ST1MS2_GPIO_Port,ST1MS2_Pin, (GPIO_PinState)((stepSelector & (1 << 1)) >> 1));
				HAL_GPIO_WritePin(ST1MS3_GPIO_Port,ST1MS3_Pin, (GPIO_PinState)((stepSelector & (1 << 2)) >> 2));
				break;
			case 2:
				HAL_GPIO_WritePin(ST2MS1_GPIO_Port,ST2MS1_Pin, (GPIO_PinState)((stepSelector & (1 << 0)) >> 0));
				HAL_GPIO_WritePin(ST2MS2_GPIO_Port,ST2MS2_Pin, (GPIO_PinState)((stepSelector & (1 << 1)) >> 1));
				HAL_GPIO_WritePin(ST2MS3_GPIO_Port,ST2MS3_Pin, (GPIO_PinState)((stepSelector & (1 << 2)) >> 2));
				break;
			case 3:
				HAL_GPIO_WritePin(ST3MS1_GPIO_Port,ST3MS1_Pin, (GPIO_PinState)((stepSelector & (1 << 0)) >> 0));
				HAL_GPIO_WritePin(ST3MS2_GPIO_Port,ST3MS2_Pin, (GPIO_PinState)((stepSelector & (1 << 1)) >> 1));
				HAL_GPIO_WritePin(ST3MS3_GPIO_Port,ST3MS3_Pin, (GPIO_PinState)((stepSelector & (1 << 2)) >> 2));
				break;	
			//default:
				//Error_Handler();
			}
		} else {
			// Set the spinning direction for the DC motors
			HAL_GPIO_WritePin(ST2MS1_GPIO_Port,ST2MS1_Pin, GPIO_PIN_RESET);
			HAL_GPIO_WritePin(ST2MS2_GPIO_Port,ST2MS2_Pin, GPIO_PIN_SET);
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
	int motorID = motor_ptr -> id;
  // Step towards the direction of target
  if (motor_ptr -> currentStep < targetStep || motor_ptr -> targetStep == INF_VAL) {
    motor_ptr -> currentStep += 1;
		pulseStepMotorPins(motorID, /*direction*/ 1);
	}
    
  else if (motor_ptr -> currentStep > targetStep)
    motor_ptr -> currentStep -= 1;
    pulseStepMotorPins(motorID, /*direction*/ 0);
}

/**
 * Steps the motor towards its target direction once.
 * @param[out] motor_ptr The pointer for the motor.
 */
void pulseStepMotorPins(int motorID, int direction) {
	switch(motorID) {
		case 1:
			if(direction == 1) {
				HAL_GPIO_WritePin(ST1DIR_GPIO_Port, ST1DIR_Pin, GPIO_PIN_SET);
			} else if(direction == 0) {
				HAL_GPIO_WritePin(ST1DIR_GPIO_Port, ST1DIR_Pin, GPIO_PIN_RESET);
			}
			HAL_GPIO_WritePin(ST1STEP_GPIO_Port, ST1STEP_Pin, GPIO_PIN_SET);
			HAL_GPIO_WritePin(ST1STEP_GPIO_Port, ST1STEP_Pin, GPIO_PIN_RESET);
			break;
		case 2:
			if(direction == 1) {
				HAL_GPIO_WritePin(ST2DIR_GPIO_Port, ST2DIR_Pin, GPIO_PIN_SET);
			} else if(direction == 0) {
				HAL_GPIO_WritePin(ST2DIR_GPIO_Port, ST2DIR_Pin, GPIO_PIN_RESET);
			}
			HAL_GPIO_WritePin(ST2STEP_GPIO_Port, ST2STEP_Pin, GPIO_PIN_SET);
			HAL_GPIO_WritePin(ST2STEP_GPIO_Port, ST2STEP_Pin, GPIO_PIN_RESET);
			break;
		case 3:
			if(direction == 1) {
				HAL_GPIO_WritePin(ST3DIR_GPIO_Port, ST3DIR_Pin, GPIO_PIN_SET);
			} else if(direction == 0) {
				HAL_GPIO_WritePin(ST3DIR_GPIO_Port, ST3DIR_Pin, GPIO_PIN_RESET);
			}
			HAL_GPIO_WritePin(ST3STEP_GPIO_Port, ST3STEP_Pin, GPIO_PIN_SET);
			HAL_GPIO_WritePin(ST3STEP_GPIO_Port, ST3STEP_Pin, GPIO_PIN_RESET);
			break;
		default:
			Error_Handler();
	}
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

/*____________________Motor Retrieve and Set Functions___________________*/
/**
 * Function to return the Name of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The motor name
 */
char* getMotorName(struct Motor *motor) {
	// Return the motor's Name
	return motor -> name;
}

/**
 * Function to return the type of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The motor type
 */
char* getMotorType(struct Motor *motor) {
	// Return the motor's Type
	return motor -> type;
}

/**
 * Function to return the ID of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The motor ID
 */
int getMotorID(struct Motor *motor) {
	// Return the motor's ID
	int IDTemp = motor ->id;
  return IDTemp;
}

/**
 * Function to return the Current Step of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The Current Step of the motor
 */
double getMotorCurrentStep(struct Motor *motor) {
  // Return the motor's current step
	double currentStepTemp = motor -> currentStep;
  return currentStepTemp;
}

/**
 * Function to return the target Step of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The Target Step of the motor
 */
int getMotorTargetStep(struct Motor *motor) {
	// Return the motor's Target Step
	double targetStepTemp = motor -> targetStep;
  return targetStepTemp;
}

/**
 * Function to return the Current Speed of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The Current Speed of the motor
 */
double getMotorCurrentSpeed(struct Motor *motor) {
  // Return the motor's current speed
	double currentSpeedTemp = motor -> currentSpeed;
  return currentSpeedTemp;
}


/**
 * Function to return the Target Speed of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The Target Speed of the motor
 */
double getMotorTargetSpeed(struct Motor *motor) {
	// Return the motor's Target Speed
	double currentTargetTemp = motor -> targetSpeed;
	return currentTargetTemp;
}

/**
 * Function to return the current Acceleration of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The current Acceleration of the motor
 */
double getMotorAccel(struct Motor *motor) {
	// Return the motor's Acceleration
	double accelTemp = motor -> acceleration;
  return accelTemp;
}

/**
 * Function to return the Displacement per Revolution of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The motor DPR
 */
double getMotorDPR(struct Motor *motor) {
	// Return the motor's Displacement per Revolution
	double dprTemp = motor -> dpr;
  return dprTemp;
}

/**
 * Function to return current uS Delay between steps of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The current uS Delay of the motor
 */
int getMotoruSDelay(struct Motor *motor) {
	// Return the motor's current uS Delay
	int uSDelayTemp = motor -> usSinceLastStep;
  return uSDelayTemp;
}

/**
 * Function to return the Step Size of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The motor Step Size
 */
int getMotorStepSize(struct Motor *motor) {
	// Return the motor's Step Size
	int stepSizeTemp = motor -> stepsize;
  return stepSizeTemp;
}

/**
 * Function to check if the motor is at its target step
 * @param[in] motor The motor being examined.
 * @return  The 1 if the motor has finished its entire movement
 */
int isMotorFinished(struct Motor *motor) {
	// Return a 1 if the motor has finished moving else return a 0
	int isComplete = 0;
	if(motor -> currentStep == motor -> targetStep) {
		isComplete = 1;
	}
	return isComplete;
}

/**
 * Function to calculate the duration (in Sec) of an instruction given the 
 * start and end speeds in mm/s and the distance to travel in mm.
 * @param[in] startSpeedMM The start speed in mm/s
 * @param[in] endSpeedMM The end speed in mm/s
 * @param[in] distanceMM the distance to travel in mm
 * @return  Double containing the total duration of the entire movement
 */
double calculateDurationMMSEC(int startSpeedMM, int endSpeedMM, int distanceMM) {
	double duration = 0;
	duration = 2 * distanceMM/(startSpeedMM+endSpeedMM);
	return duration;
}

/**
 * Function to calculate the acceleration (in mm/s^2) of an instruction given the 
 * start and end speeds in mm/s and the distance to travel in mm.
 * @param[in] startSpeedMM The start speed in mm/s
 * @param[in] endSpeedMM The end speed in mm/s
 * @param[in] distanceMM the distance to travel in mm
 * @return  Double containing the constant acceleration of the entire movement
 */
double calculateAccelMMSEC(int startSpeedMM, int endSpeedMM, int distanceMM) {
	double accel = 0;
	accel = (endSpeedMM^2-startSpeedMM^2)/(2*distanceMM);
	return accel;
}
