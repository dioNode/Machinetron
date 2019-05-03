#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

#include "submachine.h"
#include "main.h"
#include "motor.h"
#include "config.h"

//#include <windows.h>

/**
 * Generates the handler structure.
 */
struct SubMachine initializeHandler() {
  struct SubMachine handler = {"Handler", 1,
      {{/*Name*/ "Rail motor",/*Type*/ "STEP",/*Mode*/ "NORM",/*ID*/ 1,/*motorRun*/ 0,/*motorHome*/ 0,/*infSpin*/ 0,/*direction*/ 1,/*duration*/ 0,
			/*timePassed*/ 0, /*displacement*/ 0,/*startStep*/ 0,/*currentStep*/ 0,/*targetStep*/ 0,/*startSpeed*/ 0,
			/*currentSpeed*/ 0,/*targetSpeed*/ 0,/*acceleration*/ 0, /*dpr*/ 2,/*currentuSDelay*/ 0,
			/*Step Size*/ 1},
      {/*Name*/ "Spin motor",/*Type*/ "STEP",/*Mode*/ "ROT",/*ID*/ 2,/*motorRun*/ 0,/*motorHome*/ 0,/*infSpin*/ 0,/*direction*/ 1,/*duration*/ 0,
			/*timePassed*/ 0, /*displacement*/ 0,/*startStep*/ 0,/*currentStep*/ 0,/*targetStep*/ 0,/*startSpeed*/ 0,
			/*currentSpeed*/ 0,/*targetSpeed*/ 0,/*acceleration*/ 0, /*dpr*/ 2,/*currentuSDelay*/ 0,
			/*Step Size*/ 1},
      {/*Name*/ "Flip motor",/*Type*/ "STEP",/*Mode*/ "NORM",/*ID*/ 3,/*motorRun*/ 0,/*motorHome*/ 0,/*infSpin*/ 0,/*direction*/ 1,/*duration*/ 0,
			/*timePassed*/ 0, /*displacement*/ 0,/*startStep*/ 0,/*currentStep*/ 0,/*targetStep*/ 0,/*startSpeed*/ 0,
			/*currentSpeed*/ 0,/*targetSpeed*/ 0,/*acceleration*/ 0, /*dpr*/ 2,/*currentuSDelay*/ 0,
			/*Step Size*/ 1}},
   };
   return handler;
}

struct SubMachine initializeDrill() {
  struct SubMachine drill = {"Drill", 1,
      {{/*Name*/ "Pen motor",/*Type*/ "STEP",/*Mode*/ "NORM",/*ID*/ 1,/*motorRun*/ 0,/*motorHome*/ 0,/*infSpin*/ 0,/*direction*/ 1,/*duration*/ 0,
			/*timePassed*/ 0, /*displacement*/ 0,/*startStep*/ 0,/*currentStep*/ 0,/*targetStep*/ 0,/*startSpeed*/ 0,
			/*currentSpeed*/ 0,/*targetSpeed*/ 0,/*acceleration*/ 0, /*dpr*/ 2,/*currentuSDelay*/ 0,
			/*Step Size*/ 1},
      {/*Name*/ "Spin motor",/*Type*/ "DC",/*Mode*/ "NORM",/*ID*/ 2,/*motorRun*/ 0,/*motorHome*/ 0,/*infSpin*/ 0,/*direction*/ 1,/*duration*/ 0,
			/*timePassed*/ 0, /*displacement*/ 0,/*startStep*/ 0,/*currentStep*/ 0,/*targetStep*/ 0,/*startSpeed*/ 0,
			/*currentSpeed*/ 0,/*targetSpeed*/ 0,/*acceleration*/ 0, /*dpr*/ 2,/*currentuSDelay*/ 0,
			/*Step Size*/ 1},
      {/*Name*/ "Vert motor",/*Type*/ "STEP",/*Mode*/ "NORM",/*ID*/ 3,/*motorRun*/ 0,/*motorHome*/ 0,/*infSpin*/ 0,/*direction*/ 1,/*duration*/ 0,
			/*timePassed*/ 0, /*displacement*/ 0,/*startStep*/ 0,/*currentStep*/ 0,/*targetStep*/ 0,/*startSpeed*/ 0,
			/*currentSpeed*/ 0,/*targetSpeed*/ 0,/*acceleration*/ 0, /*dpr*/ 2,/*currentuSDelay*/ 0,
			/*Step Size*/ 1}},
   };
   return drill;
}

struct SubMachine initializeMill() {
  struct SubMachine mill = {"Mill", 1,
      {{/*Name*/ "Pen motor",/*Type*/ "STEP",/*Mode*/ "NORM",/*ID*/ 1,/*motorRun*/ 0,/*motorHome*/ 0,/*infSpin*/ 0,/*direction*/ 1,/*duration*/ 0,
			/*timePassed*/ 0, /*displacement*/ 0,/*startStep*/ 0,/*currentStep*/ 0,/*targetStep*/ 0,/*startSpeed*/ 0,
			/*currentSpeed*/ 0,/*targetSpeed*/ 0,/*acceleration*/ 0, /*dpr*/ 2,/*currentuSDelay*/ 0,
			/*Step Size*/ 1},
      {/*Name*/ "Spin motor",/*Type*/ "DC",/*Mode*/ "NORM",/*ID*/ 2,/*motorRun*/ 0,/*motorHome*/ 0,/*infSpin*/ 0,/*direction*/ 1,/*duration*/ 0,
			/*timePassed*/ 0, /*displacement*/ 0,/*startStep*/ 0,/*currentStep*/ 0,/*targetStep*/ 0,/*startSpeed*/ 0,
			/*currentSpeed*/ 0,/*targetSpeed*/ 0,/*acceleration*/ 0, /*dpr*/ 2,/*currentuSDelay*/ 0,
			/*Step Size*/ 1},
      {/*Name*/ "Vert motor",/*Type*/ "STEP",/*Mode*/ "NORM",/*ID*/ 3,/*motorRun*/ 0,/*motorHome*/ 0,/*infSpin*/ 0,/*direction*/ 1,/*duration*/ 0,
			/*timePassed*/ 0, /*displacement*/ 0,/*startStep*/ 0,/*currentStep*/ 0,/*targetStep*/ 0,/*startSpeed*/ 0,
			/*currentSpeed*/ 0,/*targetSpeed*/ 0,/*acceleration*/ 0, /*dpr*/ 2,/*currentuSDelay*/ 0,
			/*Step Size*/ 1}},
   };
   return mill;
}

struct SubMachine initializeLathe() {
  struct SubMachine lathe = {"Lathe", 1,
      {{/*Name*/ "Pen motor",/*Type*/ "STEP",/*Mode*/ "NORM",/*ID*/ 1,/*motorRun*/ 0,/*motorHome*/ 0,/*infSpin*/ 0,/*direction*/ 1,/*duration*/ 0,
			/*timePassed*/ 0, /*displacement*/ 0,/*startStep*/ 0,/*currentStep*/ 0,/*targetStep*/ 0,/*startSpeed*/ 0,
			/*currentSpeed*/ 0,/*targetSpeed*/ 0,/*acceleration*/ 0, /*dpr*/ 2,/*currentuSDelay*/ 0,
			/*Step Size*/ 1},
      {/*Name*/ "Spin motor",/*Type*/ "STEP",/*Mode*/ "ROT",/*ID*/ 2,/*motorRun*/ 0,/*motorHome*/ 0,/*infSpin*/ 0,/*direction*/ 1,/*duration*/ 0,
			/*timePassed*/ 0, /*displacement*/ 0,/*startStep*/ 0,/*currentStep*/ 0,/*targetStep*/ 0,/*startSpeed*/ 0,
			/*currentSpeed*/ 0,/*targetSpeed*/ 0,/*acceleration*/ 0, /*dpr*/ 2,/*currentuSDelay*/ 0,
			/*Step Size*/ 1},
      {/*Name*/ "Vert motor",/*Type*/ "STEP",/*Mode*/ "NORM",/*ID*/ 3,/*motorRun*/ 0,/*motorHome*/ 0,/*infSpin*/ 0,/*direction*/ 1,/*duration*/ 0,
			/*timePassed*/ 0, /*displacement*/ 0,/*startStep*/ 0,/*currentStep*/ 0,/*targetStep*/ 0,/*startSpeed*/ 0,
			/*currentSpeed*/ 0,/*targetSpeed*/ 0,/*acceleration*/ 0, /*dpr*/ 2,/*currentuSDelay*/ 0,
			/*Step Size*/ 1}},
   };
   return lathe;
}

void printSubMachineDetails(struct SubMachine submachine) {
  //printf("%s: %d/%d %d/%d %d/%d\n", submachine.name, 
    //submachine.motors[0].currentStep, submachine.motors[0].targetStep,
    //submachine.motors[1].currentStep, submachine.motors[1].targetStep,
    //submachine.motors[2].currentStep, submachine.motors[2].targetStep);
}

/*
void tickSubMachine(struct SubMachine *submachine_ptr, double delay) {
  for (int motorNum = 0; motorNum < 3; motorNum++) {
    // Update time for motor
    struct Motor * motor_ptr = &submachine_ptr -> motors[motorNum];
    motor_ptr -> msSinceLastStep += delay;
    motor_ptr -> currentSpeed += motor_ptr -> acceleration * (delay/1000);
    // Check if enough time has passed for new tick
    double msPerStepVal = msPerStep(*motor_ptr);
    if (motor_ptr -> msSinceLastStep > msPerStepVal) {
      // Step motor
      stepMotor(motor_ptr);
      motor_ptr -> msSinceLastStep -= msPerStepVal;
    }
  }
}
*/

struct Motor * getMotorById(struct SubMachine *submachine_ptr, int id) {
  struct Motor *motor_ptr;
  for (int motorNum = 0; motorNum < 3; motorNum++) {
    motor_ptr = &submachine_ptr -> motors[motorNum];
    if (motor_ptr -> id == id) {
      return motor_ptr;
    }
  }
  //printf("Motor not found\n");
  return NULL;
}

//TODO Set up processInstruction to handle Stepper/DC motors and different variables plus do not rely
// on definitie positions for each motor

void processInstruction(uint8_t instData[28], struct SubMachine *submachine_ptr) {
  // Extract important variables
	
	
	
	///////Problematic Line
	printf("ProcessInstructionEntered\n\r");
	
	
	
	//printf("SubmachineID: %d", submachine_ptr -> id);
	int motorByteLocations[3] = {0,7,14};
	/*
	uint8_t motor1Byte = instData[MOTOR1_BYTE_LOC];
	uint8_t motor2Byte = instData[MOTOR2_BYTE_LOC];
	uint8_t motor3Byte = instData[MOTOR3_BYTE_LOC];
	*/
	//printf("SIze of motor Id Locs %d",sizeof(motorByteLocations)/sizeof(*motorByteLocations));
	for(int i = 0; i < sizeof(motorByteLocations)/sizeof(*motorByteLocations); i++) {
		uint8_t motorByte = instData[motorByteLocations[i]];
		int motorID = (int)((motorByte & MOTOR_BITS_MASK) >> MOTOR_BITS_SHIFT);
		int direction = (int)((motorByte & DIR_BIT_MASK) >> DIR_BIT_SHIFT);
		int motorRun = (int)((motorByte & MOTOR_RUN_BIT_MASK) >> MOTOR_RUN_BIT_SHIFT);
		int motorHome = (int)((motorByte & HOME_MOTOR_BIT_MASK) >> HOME_MOTOR_BIT_SHIFT);
		int motorInfSpin = (int)((motorByte & INF_SPIN_BIT_MASK) >> INF_SPIN_BIT_SHIFT);
		//printf("motorID %d, direction %d, motorRun %d, motorHome %d, motorInfSpin %d\n\r", 
		//motorID,direction,motorRun,motorHome,motorInfSpin);
		
		uint8_t newPosMSH = instData[motorByteLocations[i] + 1];
		uint8_t newPosLSH = instData[motorByteLocations[i] + 2];
		//printf("newPosMSH %d, newPosLSH %d\n\r", newPosMSH,newPosLSH);
		
		uint8_t startSpeedMSH = instData[motorByteLocations[i] + 3];
		uint8_t startSpeedLSH = instData[motorByteLocations[i] + 4];
		//printf("startSpeedMSH %d, startSpeedLSH %d\n\r", startSpeedMSH,newPosLSH);
		
		uint8_t endSpeedMSH = instData[motorByteLocations[i] + 5];
		uint8_t endSpeedLSH = instData[motorByteLocations[i] + 6];
		//printf("endSpeedMSH %d, endSpeedLSH %d\n\r", endSpeedMSH,endSpeedLSH);
		
		//printf("newPosMSH %d, newPosLSH %d, startSpeedMSH %d, startSpeedLSH %d, endSpeedMSH %d, endSpeedLSH %d\n\r", 
		//newPosMSH,newPosLSH,startSpeedMSH,startSpeedLSH,endSpeedMSH,endSpeedLSH);
		
		int newPos = (int)((newPosMSH << 8) | newPosLSH);
		int startSpeed = (int)((startSpeedMSH << 8) | startSpeedLSH);
		int endSpeed = (int)((endSpeedMSH << 8) | endSpeedLSH);
		
		//printf("newPos %d\n\r", startSpeed);
		//printf("newPos %d, startSpeed %d, endSpeed %d\n\r", 
		//newPos,startSpeed,endSpeed);
		
		//printf("newPosMSH %d, newPosLSH %d, startSpeedMSH %d, startSpeedLSH %d, endSpeedMSH %d, endSpeedLSH %d,newPos %d, startSpeed %d, endSpeed %d\n\r", 
		//newPosMSH,newPosLSH,startSpeedMSH,startSpeedLSH,endSpeedMSH,endSpeedLSH,newPos,startSpeed,endSpeed);
		
		// Based on whether the motor is Homing or In Infinite Spin mode or normal mode 
		// set the parameters accordingly
		// As a test only set the motor parameters if the motor is running
		if(motorRun == 1) {
			printf("Test stufff \n");
			struct Motor * motor_ptr = getMotorById(submachine_ptr, motorID);
			//printf("Motor run: %d, motor home: %d, motorInfSpin: %d, direction: %d, newPos: %d, startSpeed: %d, endSpeed: %d\n\r", motorRun, motorHome, motorInfSpin, direction, newPos, startSpeed, endSpeed);
			
			//setMotorParams2(motor_ptr, motorRun, motorHome, motorInfSpin, direction, newPos, startSpeed, endSpeed);
			setMotorParams(motor_ptr, motorRun, motorHome, motorInfSpin, direction, newPos, startSpeed, endSpeed);
			//printf("TestmotorRunAfter");
			
		}
	}
}

int getDirectionBit(int initByte) {
  // Need to read the 5th bit
  initByte = initByte >> 4;
  initByte = initByte & 1;
  return initByte;
}

int getMotorIdBits(int initByte) {
  // Return the leftmost 3 bits
  return initByte >> 5;
}

int isComplete(struct SubMachine submachine) {
  int complete = 1;
  for (int motorNum = 0; motorNum < 3; motorNum++) {
    struct Motor motor = submachine.motors[motorNum];
    if (((motor.currentStep != motor.targetStep) && (motor.infSpin != 1) 
			&& (motor.motorRun == 1) && (strcmp(motor.type, "DC") != 0)) || (motor.motorHome == 1)){
      complete = 0;
    }
  }
  return complete;
}

// Temp function
void setMotorParams2(struct Motor *motor_ptr, int motorRun, int motorHome, int motorInfSpin, int dir, int newPos, int startSpeed, int endSpeed) {
  printf("got here\n");
	// First extract all the parameters from the motor
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
	
	int displacementWU =10;
	int targetPos = 10;
	/*
	
	if(strcmp(motor_ptr -> mode, "ROT") == 0) {
		// Motor is in ROT mode meaning displacement and newPos need to be calculated based on input data
		int modPos = ((int)getCurrentPosition(*motor_ptr) % (int)(motor_ptr -> dpr));
		int newPosNegRev = newPos - motor_ptr -> dpr;
		
		if(abs(newPos-modPos) <= abs(newPosNegRev-modPos)) {
			displacementWU = newPos-modPos;
			targetPos = (int)getCurrentPosition(*motor_ptr) + displacementWU;
		} else {
			displacementWU = newPosNegRev-modPos;
			targetPos = (int)getCurrentPosition(*motor_ptr) + displacementWU;
		}
	} else if(strcmp(motor_ptr -> mode, "NORM") == 0){
		displacementWU = newPos - (int)getCurrentPosition(*motor_ptr); //Calculates the displacement in mm or degrees
		targetPos = newPos;
	}*/
	
	//int displacementStep = (int)worldUnitsToStepUnits((double)displacementWU, *motor_ptr);
	//int id = motor_ptr -> id;
	double startStepSpeed;
	double endStepSpeed;
	/*
	// Set the speeds as negative or positive depending on the direction of travel
	if(displacementStep >= 0) {
		startStepSpeed = worldUnitsToStepUnits((double)startSpeed, *motor_ptr);
		endStepSpeed = worldUnitsToStepUnits((double)endSpeed, *motor_ptr);
	} else {
		startStepSpeed = worldUnitsToStepUnits(-1 * startSpeed, *motor_ptr);
		endStepSpeed = worldUnitsToStepUnits(-1 * endSpeed, *motor_ptr);
	}
	
	double accelerationStep = (pow(endStepSpeed, 2) - pow(startStepSpeed, 2)) / (2*displacementStep);
	
	
	// Set all motor parameters
	motor_ptr -> motorRun = motorRun;
	motor_ptr -> motorHome = motorHome;
	motor_ptr -> infSpin = motorInfSpin;
	motor_ptr -> direction = dir;
	motor_ptr -> duration = calculateDurationMMSEC(startSpeed, endSpeed, displacementWU);
	motor_ptr -> timePassed = 0;
	motor_ptr -> displacement = displacementStep;
	motor_ptr -> startStep = motor_ptr -> currentStep;
	motor_ptr -> targetStep = worldUnitsToStepUnits((double)targetPos, *motor_ptr);
	motor_ptr -> startSpeed = startStepSpeed;
	motor_ptr -> currentSpeed = startStepSpeed;
	motor_ptr -> targetSpeed = endStepSpeed;
  motor_ptr -> acceleration = accelerationStep;
	
	int uSDelay = calculateuSDelay(motor_ptr -> currentSpeed);
	
	motor_ptr -> currentuSDelay = uSDelay;*/
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
