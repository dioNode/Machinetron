/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MOTOR_H_
#define __MOTOR_H_

#ifdef __cplusplus
extern "C" {
#endif

#include "main.h"

/**
 * A structure to represent a stepper motor
 */
extern struct Motor {
   char name[11];       // The name of the motor
	 char type[5];				// DC or STEP
	 char mode[5];				// Mode defines whether the stepper motor is infinitely rotational ("ROT" or "NORM")
   int id;              // ID used to identify in commands
	 int motorRun;				// Variable used to determine if the motor is running or not
	 int motorHome;				// Variable used to determine if the motor is to home its position
	 int infSpin;					// Variable used to determine if the motor is to spin indefinitely or not
	 int direction;				// The current Direction of the motor
	 double duration;			// The duration of the current path in seconds
	 double timePassed;		// Variable to store the time that has passed in the current path (in sec)
	 int displacement;    // The displacement of the path in steps
	 int startStep;				// The Start Step 
   int currentStep;     // The current number of steps
   int targetStep;      // The number of steps it needs to reach
	 int startSpeed; 	// The start step speed (steps/s) (rev/s if a DC Motor)
   double currentSpeed; // The current step speed (steps/s) (rev/s if a DC Motor)
	 int targetSpeed;  // The target step speed (steps/s) (rev/s if a DC Motor)
   double acceleration; // The step acceleration (steps/s^2)
   int dpr;          // Displacement per revolution of motor
   int currentuSDelay;  // The Current uS Delay between steps
	 int stepsize;				// Step size: 1/(1,2,4,8,16)
} motor;

/**
 * Initialises the motor stepsize pins
 * @param[out] motor_array An array containing all the motors
 */
void initMotorsStepSize(struct Motor *motors_array, int len);

/**
 * Function to return the MS3,MS2,MS1, number based on the stepsize selected for the motor
 * @param[out] stepSize The size of the step inverted (1,2,4,8,16)
 */
int getStepSizeSelector(int stepSize);

/**
 * Steps the motor towards its target direction once.
 * @param[out] motor_ptr The pointer for the motor.
 */
void stepMotor(struct Motor *motor_ptr);

/**
 * Fuction to pulse the necessary motor pins based on ID and direction
 * @param motorID The ID for the motor.
 * @param direction The direction to step the motor
 */
void pulseStepMotorPins(int motorID, int direction);
	
/**
 * Enables or disables the stepper driver of the stepper that is being pointed to
 * @param motorID The ID for the motor.
 * @param enable Value of 1 indicates enable, Value of 0 indicates Disable
 */
void enableStepperDriver(int motorID, int enable);
	
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
void setMotorParams(struct Motor *motor_ptr, int motorRun, int motorHome, int motorInfSpin, int dir, int newPos, int startSpeed, int endSpeed);

/**
 * Prints the details about the current motor.
 * @param[out] motor  The motor you want information about.
 */
void printMotorDetails(struct Motor motor);

/**
 * Finds the current position of the motor (steps).
 * @param[in] motor The motor you want to read from.
 * @return    The motor's position (steps).
 */
int getCurrentPositionSteps(struct Motor *motor);

/**
 * Calculates the number of milliseconds before each step.
 * @param[in] motor The motor being examined.
 * @return  The number of milliseconds before each step for the motor.
 */
double msPerStep(struct Motor *motor);

/*____________________Motor Retrieve and Set Functions___________________*/
/**
 * Function to return the Name of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The motor name
 */
char* getMotorName(struct Motor *motor);

/**
 * Function to return the type of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The motor type
 */
char* getMotorType(struct Motor *motor);

/**
 * Function to return the ID of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The motor ID
 */
int getMotorID(struct Motor *motor);

/**
 * Function to return the Current Step of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The Current Step of the motor
 */
double getMotorCurrentStep(struct Motor *motor);

/**
 * Function to return the target Step of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The Target Step of the motor
 */
int getMotorTargetStep(struct Motor *motor);

/**
 * Function to return the Current Speed of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The Current Speed of the motor
 */
double getMotorCurrentSpeed(struct Motor *motor);


/**
 * Function to return the Target Speed of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The Target Speed of the motor
 */
double getMotorTargetSpeed(struct Motor *motor);

/**
 * Function to return the current Acceleration of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The current Acceleration of the motor
 */
double getMotorAccel(struct Motor *motor);

/**
 * Function to return the Displacement per Revolution of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The motor DPR
 */
double getMotorDPR(struct Motor *motor);

/**
 * Function to return current uS Delay between steps of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The current uS Delay of the motor
 */
int getMotoruSDelay(struct Motor *motor);

/**
 * Function to return the Step Size of the specific motor
 * @param[in] motor The motor being examined.
 * @return  The motor Step Size
 */
int getMotorStepSize(struct Motor *motor);

/**
 * Function to check if the motor is at its target step
 * @param[in] motor The motor being examined.
 * @return  The 1 if the motor has reached its target else return zero
 */
int isMotorFinished(struct Motor *motor);

/**
 * Function to calculate the duration (in Sec) of an instruction given the 
 * start and end speeds in steps/s and the distance to travel in steps.
 * @param[in] startSpeedSteps The start speed in steps/s
 * @param[in] endSpeedSteps The end speed in steps/s
 * @param[in] distanceSteps the distance to travel in steps
 * @return  Double containing the total duration of the entire movement
 */
double calculateDurationSteps(int startSpeedSteps, int endSpeedSteps, int displacementSteps);

/**
 * Function to calculate the acceleration (in mm/s^2) of an instruction given the 
 * start and end speeds in mm/s and the distance to travel in mm.
 * @param[in] startSpeedMM The start speed in mm/s
 * @param[in] endSpeedMM The end speed in mm/s
 * @param[in] distanceMM the distance to travel in mm
 * @return  Double containing the constant acceleration of the entire movement
 */
double calculateAccelMMSEC(int startSpeedMM, int endSpeedMM, int distanceMM);

/**
 * Function to calculate the required uS Delay between motor steps based on the current speed 
 * @param[in] currentSpeed The current speed of the stepper motor in steps/sec
 * @return  int containing the required step delay in uS
 */
double calculateuSDelay(double currentSpeed);

/**
 * Function to calculate the new speed based on the time Passed in the instruction 
 * and adjust the motor's parameters accordingly
 * @param[in] timePassed The current speed of the stepper motor in steps/sec
 * @return  None
 */
void setSpeedStepsAnduSDelay(struct Motor *motor);

/**
 * Function to calculate the duty Cycle of PWM for the DC motor based on the speed input
 * @param[in] motor_ptr The pointer to the motor
 * @param[in] desiredSpeed The required speed of the motor as percentage of max speed
 * @return  PWM Duty Cycle as a value from 0 to 100
 */
int calculatePWMDutyCycle(struct Motor *motor_ptr, double desiredSpeed);

/**
 * Function to determine if the limit switch specified by the motor ID is closed or open
 * @param[in] motorID The ID for the motor
 * @return  The state of the Limit Switch (1 indicating closed, 0 indicating open)
 */
int isLimitSwitchClosed(int motorID);
#endif // __MOTOR_H_
