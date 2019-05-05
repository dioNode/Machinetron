#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>


#include "motor.h"
#include "main.h"
#include "config.h"
//#include "stm32f1xx_hal.h"
#include "usart.h"


/**
 * Initialises the motor stepsize pins
 * @param[out] motor_array An array containing all the motors
 */
void initMotorsStepSize(struct Motor *motors_array, int len) {
	//printf("initMotorsStepSize");
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
	int dir;
	int motorHome = motor_ptr -> motorHome;
	if(motor_ptr -> infSpin != 1) {
		dir = motor_ptr -> direction;
	} else if(motorHome == 1){
		dir = 0;
	} else {
		//if(((targetStep - (motor_ptr->currentStep))/abs(targetStep - (motor_ptr->currentStep))) == 1) {
			dir = 1;
		//} else {
			//dir = 0;
		//}
	}
	// Step the motor in the specified direction
	if (dir == 1) {
		motor_ptr -> currentStep += 1;
		motor_ptr -> timePassed += ((double)(motor_ptr->currentuSDelay))/((double)1000000);
		// Calculate the new speed based on the time increment
		setSpeedStepsAnduSDelay(motor_ptr);
		pulseStepMotorPins(motorID, /*direction*/ 1);
	} else if(dir == 0) {
		motor_ptr -> currentStep -= 1;
		motor_ptr -> timePassed += ((double)(motor_ptr->currentuSDelay))/((double)1000000);
		// Calculate the new speed based on the time increment
		setSpeedStepsAnduSDelay(motor_ptr);
		pulseStepMotorPins(motorID, /*direction*/ 0);
	}
}

/**
 * Fuction to pulse the necessary motor pins based on ID and direction
 * @param motorID The ID for the motor.
 * @param direction The direction to step the motor
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
 * Enables or disables the stepper driver of the stepper that is being pointed to
 * @param motorID The ID for the motor.
 * @param enable Value of 1 indicates enable, Value of 0 indicates Disable
 */
void enableStepperDriver(int motorID, int enable) {
	switch(motorID) {
		case 1:
			if(enable == 1) {
				HAL_GPIO_WritePin(ST1EN_GPIO_Port, ST1EN_Pin, GPIO_PIN_RESET);
			} else if(enable == 0) {
				HAL_GPIO_WritePin(ST1EN_GPIO_Port, ST1EN_Pin, GPIO_PIN_SET);
			}
			break;
		case 2:
			if(enable == 1) {
				HAL_GPIO_WritePin(ST2EN_GPIO_Port, ST2EN_Pin, GPIO_PIN_RESET);
			} else if(enable == 0) {
				HAL_GPIO_WritePin(ST2EN_GPIO_Port, ST2EN_Pin, GPIO_PIN_SET);
			}
			break;
		case 3:
			if(enable == 1) {
				HAL_GPIO_WritePin(ST3EN_GPIO_Port, ST3EN_Pin, GPIO_PIN_RESET);
			} else if(enable == 0) {
				HAL_GPIO_WritePin(ST3EN_GPIO_Port, ST3EN_Pin, GPIO_PIN_SET);
			}
			break;
		default:
			Error_Handler();
	}
}

/**
 * Sets the correct targets for the motor. This requires converting
 * displacement values to number of steps.
 * @param[out]  motor_ptr   The pointer for the motor you want to set targets for.
 * @param[in]   motorRun    Specifies if the motor is running or is not being used
 * @param[in]		motorHome		Specifies if the motor is to home is position
 * @param[in]		motorInfSpin Used to determine of the motor is to spin indefinitely
 * @param[in]   dir         The direction of the motor
 * @param[in]   newPos      The displacement you want to reach (steps). (positive or negative)
 * @param[in]   startSpeed  The speed which you start moving at (steps/s).
 * @param[in]   endSpeed    The speed which you stop moving at when you reach target (steps/s).
 */
void setMotorParams(struct Motor *motor_ptr, int motorRun, int motorHome, int motorInfSpin, int dir, int newPos, int startSpeed, int endSpeed) {
  //printf("got here\n");
	/*
	
	char *name = motor_ptr -> name;
	char *type = motor_ptr -> type; 	
	char *mode = motor_ptr -> mode;
	int motorId = motor_ptr -> id; 
	int currentMotorRun = motor_ptr -> motorRun;
	int currentMotorHome = motor_ptr -> motorHome; 
	int currentInfSpin = motor_ptr -> infSpin;
	int currentDir = motor_ptr -> direction; 
	double currentDuration = motor_ptr -> duration;
	double currentTimePassed = motor_ptr -> timePassed; 
	int currentDisplacement = motor_ptr -> displacement;
	int currentStartStep = motor_ptr -> startStep;
	int currentStep = motor_ptr -> currentStep;
	int currentTargetStep = motor_ptr -> targetStep;
	double currentStartSpeed = motor_ptr -> startSpeed;
	double currentSpeed = motor_ptr -> currentSpeed;
	double currentTargetSpeed = motor_ptr -> targetSpeed;
  double currentAcceleration = motor_ptr -> acceleration;
  double motorDPR = motor_ptr -> dpr;
  int currentuSDelay = motor_ptr -> currentuSDelay;  // The Current uS Delay between steps
	int motorStepSize = motor_ptr -> stepsize;	
	*/
	
	// First check if the motor is in NORM or ROT mode
	//HAL_UART_Transmit(&huart1, (uint8_t *)motorRun, sizeof(motorRun), HAL_MAX_DELAY);
	//printInteger("Test if it works", 16, motorRun);
	//double displacementWU;
	int displacementSteps;
	//double targetPos;
	int targetPos;
	
	if(strcmp(motor_ptr -> mode, "ROT") == 0) {
		// Motor is in ROT mode meaning displacement and newPos need to be calculated based on input data
		int modPos = getCurrentPositionSteps(motor_ptr) % (motor_ptr -> dpr);
		int newPosNegRev = newPos - motor_ptr -> dpr;
		if(abs(newPos-modPos) <= abs(newPosNegRev-modPos)) {
			displacementSteps = newPos-modPos;
			targetPos = getCurrentPositionSteps(motor_ptr) + displacementSteps;
		} else {
			displacementSteps = newPosNegRev-modPos;
			targetPos = getCurrentPositionSteps(motor_ptr) + displacementSteps;
		}
	} else if(strcmp(motor_ptr -> mode, "NORM") == 0){
		displacementSteps = newPos - getCurrentPositionSteps(motor_ptr); //Calculates the displacement in steps
		targetPos = newPos;
	}
	
	//int displacementStep = worldUnitsToStepUnits(displacementWU, motor_ptr);
	//double startStepSpeed;
	//double endStepSpeed;
	int startStepSpeed;
	int endStepSpeed;
	// Set the speeds as negative or positive depending on the direction of travel
	if(displacementSteps >= 0) {
		//startStepSpeed = worldUnitsToStepUnits(startSpeed, motor_ptr);
		//endStepSpeed = worldUnitsToStepUnits(endSpeed, motor_ptr);
		startStepSpeed = startSpeed;
		endStepSpeed = endSpeed;
	} else {
		//startStepSpeed = worldUnitsToStepUnits(-1 * startSpeed, motor_ptr);
		//endStepSpeed = worldUnitsToStepUnits(-1 * endSpeed, motor_ptr);
		startStepSpeed = -1*startSpeed;
		endStepSpeed = -1*endSpeed;
	}
	
	double accelerationStep = (pow(endStepSpeed, 2) - pow(startStepSpeed, 2)) / (2*displacementSteps);
	
	// Set all motor parameters
	motor_ptr -> motorRun = motorRun;
	motor_ptr -> motorHome = motorHome;
	motor_ptr -> infSpin = motorInfSpin;
	motor_ptr -> direction = dir;
	motor_ptr -> duration = calculateDurationSteps(startStepSpeed, endStepSpeed, displacementSteps);
	motor_ptr -> timePassed = 0;
	motor_ptr -> displacement = displacementSteps;
	motor_ptr -> startStep = motor_ptr -> currentStep;
	//motor_ptr -> targetStep = worldUnitsToStepUnits(targetPos, motor_ptr);
	motor_ptr -> targetStep = targetPos;
	motor_ptr -> startSpeed = startStepSpeed;
	motor_ptr -> currentSpeed = (double)startStepSpeed;
	motor_ptr -> targetSpeed = endStepSpeed;
  motor_ptr -> acceleration = accelerationStep;
	
	int uSDelay = calculateuSDelay(motor_ptr->currentSpeed);
	
	motor_ptr -> currentuSDelay = uSDelay;
  // Deal with speeds
  // v^2 = u^2 + 2as --> a = (v^2-u^2)/(2s)
	/*
  if (newPos != 0){
		double accelerationStep = (pow(endStepSpeed, 2) - pow(startStepSpeed, 2)) / (2*displacementStep);
    motor_ptr -> currentSpeed = startStepSpeed;
		motor_ptr -> targetSpeed = endStepSpeed;
    motor_ptr -> acceleration = accelerationStep;
  }
	*/
}

/**
 * Prints the details about the current motor.
 * @param[out] motor  The motor you want information about.
 */
void printMotorDetails(struct Motor motor) {
   //printf("%s %d / %d\n", motor.name, motor.targetStep, motor.currentStep);
}

/**
 * Finds the current position of the motor (steps).
 * @param[in] motor The motor you want to read from.
 * @return    The motor's position (steps).
 */
int getCurrentPositionSteps(struct Motor *motor) {
  return motor->currentStep;
}

/**
 * Finds the current position of the motor (mm or degrees).
 * @param[in] motor The motor you want to read from.
 * @return    The motor's position (mm or degrees).
 */
/*
double getCurrentPosition(struct Motor *motor) {
  return motor->currentStep * motor->dpr / (NUM_STEPPER_STEPS * motor->stepsize);
}
*/

/**
* Converts the world units (displacement:mm,deg, speed: mm/s,deg/s, acceleration: mm/s^2,deg/s^2) 
 * of the motor to step units (displacement:steps, speed: steps/s, acceleration: steps/s^2).
 * @param[in] worldUnitValue  The value in World units to be converted
 * @param[in] motor         	The motor for which this conversion is being done
 * @return  The equivalent value in steps Units ot produce the Value Units.
 */
/*
int worldUnitsToStepUnits(double worldUnitValue, struct Motor *motor) {
  //Extract variables from motor
	int stepSize = motor->stepsize;
	int dpr = motor->dpr;
	// Special number return same
  if (worldUnitValue == INF_VAL) {
    return INF_VAL;
  }
  // Finds the equivalent number of step units to get as close as possible to the world units
  double temp = (double)NUM_STEPPER_STEPS*(double)stepSize;
	double stepUnitValueDbl = worldUnitValue*(temp)/(double)dpr;
	int stepUnitValue = round(stepUnitValueDbl);
  return stepUnitValue;
}
*/

/**
 * Calculates the number of milliseconds before each step.
 * @param[in] motor The motor being examined.
 * @return  The number of milliseconds before each step for the motor.
 */
double msPerStep(struct Motor *motor) {
  // Find number of ms required per step (currentSpeed is in steps per second)
  return 1000 / motor->currentSpeed;
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
	int uSDelayTemp = motor -> currentuSDelay;
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
	int isComplete = 1;
	if(motor -> motorRun != 0) {
		if(motor -> motorHome == 1) {
			if(isLimitSwitchClosed(motor -> id) == 1) {
				isComplete = 1;
				motor -> motorHome = 0;
			} else {
				isComplete = 0;
			}
		} else {
			if(motor -> infSpin == 1) {
				isComplete = 0;
			} else {
				if(motor -> currentStep == motor -> targetStep) {
					isComplete = 1;
				} else {
					isComplete = 0;
				}
			}
		}
	} else {
		isComplete = 1;
	}
	return isComplete;
}

/**
 * Function to calculate the duration (in Sec) of an instruction given the 
 * start and end speeds in steps/s and the distance to travel in steps.
 * @param[in] startSpeedSteps The start speed in steps/s
 * @param[in] endSpeedSteps The end speed in steps/s
 * @param[in] distanceSteps the distance to travel in steps
 * @return  Double containing the total duration of the entire movement
 */
double calculateDurationSteps(int startSpeedSteps, int endSpeedSteps, int displacementSteps) {
	double duration = 0;
	duration = 2*(double)displacementSteps/((double)startSpeedSteps+(double)endSpeedSteps);
	return duration;
}

/**
 * Function to calculate the duration (in Sec) of an instruction given the 
 * start and end speeds in mm/s and the distance to travel in mm.
 * @param[in] startSpeedMM The start speed in mm/s
 * @param[in] endSpeedMM The end speed in mm/s
 * @param[in] distanceMM the distance to travel in mm
 * @return  Double containing the total duration of the entire movement
 */
/*
double calculateDurationMMSEC(int startSpeedMM, int endSpeedMM, int displacementMM) {
	double duration = 0;
	duration = 2*(double)displacementMM/((double)startSpeedMM+(double)endSpeedMM);
	return duration;
}
*/

/**
 * Function to calculate the acceleration (in mm/s^2) of an instruction given the 
 * start and end speeds in mm/s and the distance to travel in mm.
 * @param[in] startSpeedMM The start speed in mm/s
 * @param[in] endSpeedMM The end speed in mm/s
 * @param[in] distanceMM the distance to travel in mm
 * @return  Double containing the constant acceleration of the entire movement in mm/s^2
 */
double calculateAccelMMSEC(int startSpeedMM, int endSpeedMM, int distanceMM) {
	double accel = 0;
	accel = (pow(endSpeedMM, 2) - pow(startSpeedMM, 2)) / (2*distanceMM);
	return accel;
}

/**
 * Function to calculate the required uS Delay between motor steps based on the current speed 
 * @param[in] currentSpeed The current speed of the stepper motor in steps/sec
 * @return  int containing the required step delay in uS
 */
double calculateuSDelay(double currentSpeed) {
	double temp = ((double)(1000000))/currentSpeed;
	//int retTemp = (int)ceil(temp);
	//int retTemp = roundNumToInt(temp);
	//double retTemp = (int)temp;
	return temp;
	//return 47619;
}

/**
 * Function to calculate the new speed based on the time Passed in the instruction 
 * and adjust the motor's parameters accordingly
 * @param[in] timePassed The current speed of the stepper motor in steps/sec
 * @return  None
 */
void setSpeedStepsAnduSDelay(struct Motor *motor) {
	double newSpeed = (double)(motor->startSpeed) + (motor->acceleration)*(motor->timePassed);
	motor -> currentSpeed = newSpeed;
	//motor -> currentuSDelay = (calculateuSDelay(newSpeed));
	motor->currentuSDelay = ((double)(1000000))/newSpeed;
	//motor -> currentuSDelay = 1000;
}

/**
 * Function to calculate the duty Cycle of PWM for the DC motor based on the speed input
 * @param[in] motor_ptr The pointer to the motor
 * @param[in] desiredSpeed The required speed of the motor in revs/s
 * @return  PWM Duty Cycle as a value from 0 to 100
 */
int calculatePWMDutyCycle(struct Motor *motor_ptr, double desiredSpeed) {
	// Make sure that the motor is a DC Motor
	// Assume max rps is 83.333 revs/s (5000rpm) which equates to 4.5V on the motor
	double PWMDutyCycle;
	if(strcmp(motor_ptr -> type, "DC") == 0) {
		//Take the current speed in the motor struct
		double percentOfMaxSpeed = desiredSpeed/83.333;
		PWMDutyCycle = 4.5/12*percentOfMaxSpeed*100;
	} else {
		PWMDutyCycle = 0;
	}
	return (int)round(PWMDutyCycle);
}

/**
 * Function to determine if the limit switch specified by the motor ID is closed or open
 * @param[in] motorID The ID for the motor
 * @return  The state of the Limit Switch (1 indicating closed, 0 indicating open)
 */
int isLimitSwitchClosed(int motorID) {
	int limSwitchState;
	switch(motorID) {
		case 1:
			limSwitchState = HAL_GPIO_ReadPin(LIMSW1_GPIO_Port,LIMSW1_Pin);
			break;
		case 2:
			limSwitchState = HAL_GPIO_ReadPin(LIMSW4_GPIO_Port,LIMSW4_Pin);
			break;
		case 3:
			limSwitchState = HAL_GPIO_ReadPin(LIMSW5_GPIO_Port,LIMSW5_Pin);
			break;
	}
	return limSwitchState;
}
