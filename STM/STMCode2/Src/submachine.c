#include "submachine.h"
#include "motor.h"
#include "config.h"
#include <stdio.h>
#include <string.h>
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
	int motorByteLocations[3] = {0,7,14};
	/*
	uint8_t motor1Byte = instData[MOTOR1_BYTE_LOC];
	uint8_t motor2Byte = instData[MOTOR2_BYTE_LOC];
	uint8_t motor3Byte = instData[MOTOR3_BYTE_LOC];
	*/
	for(int i = 0; i < sizeof(motorByteLocations)/sizeof(*motorByteLocations); i++) {
		uint8_t motorByte = instData[motorByteLocations[i]];
		int motorID = (int)((motorByte & MOTOR_BITS_MASK) >> MOTOR_BITS_SHIFT);
		int direction = (int)((motorByte & DIR_BIT_MASK) >> DIR_BIT_SHIFT);
		int motorRun = (int)((motorByte & MOTOR_RUN_BIT_MASK) >> MOTOR_RUN_BIT_SHIFT);
		int motorHome = (int)((motorByte & HOME_MOTOR_BIT_MASK) >> HOME_MOTOR_BIT_SHIFT);
		int motorInfSpin = (int)((motorByte & INF_SPIN_BIT_MASK) >> INF_SPIN_BIT_SHIFT);
		
		uint8_t newPosMSH = instData[motorByteLocations[i] + 1];
		uint8_t newPosLSH = instData[motorByteLocations[i] + 2];
		uint8_t startSpeedMSH = instData[motorByteLocations[i] + 3];
		uint8_t startSpeedLSH = instData[motorByteLocations[i] + 4];
		uint8_t endSpeedMSH = instData[motorByteLocations[i] + 5];
		uint8_t endSpeedLSH = instData[motorByteLocations[i] + 6];
		int newPos = (int)((newPosMSH << 8) | newPosLSH);
		int startSpeed = (int)((startSpeedMSH << 8) | startSpeedLSH);
		int endSpeed = (int)((endSpeedMSH << 8) | endSpeedLSH);
		
		// Based on whether the motor is Homing or In Infinite Spin mode or normal mode 
		// set the parameters accordingly
		setMotorParams(getMotorById(submachine_ptr,motorID), motorRun, motorHome, motorInfSpin, direction, newPos, startSpeed, endSpeed);
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
