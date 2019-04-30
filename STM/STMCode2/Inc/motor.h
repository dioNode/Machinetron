/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MOTOR_H_
#define __MOTOR_H_

#ifdef __cplusplus
extern "C" {
#endif

/**
 * A structure to represent a stepper motor
 */
extern struct Motor {
   char* name;          // The name of the motor
	 char* type;					// DC or STEP
   int id;              // ID used to identify in commands
	 int motorRun;				// Variable used to determine if the motor is running or not
	 int direction;				// The current Direction of the motor
	 int duration;				// The duration of the current path in seconds
	 int displacement;    // The displacement of the path in steps
	 int startStep;				// The Start Step 
   int currentStep;     // The current number of steps
   int targetStep;      // The number of steps it needs to reach
	 double startSpeed; 	// The start step speed (steps/s)
   double currentSpeed; // The current step speed (steps/s)
	 double targetSpeed;  // The target step speed (steps/s)
   double acceleration; // The step acceleration (steps/s^2)
   double dpr;          // Displacement per revolution of motor
   int currentuSDelay;  // The Current uS Delay between steps
	 int stepsize;				// Step size: 1/(1,2,4,8,16)
} motor;

/**
 * Initialises the motor stepsize pins
 * @param[out] motor_array An array containing all the motors
 */
void initMotorsStepSize(struct Motor motors_array[], int len);

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
 * Steps the motor towards its target direction once.
 * @param[out] motor_ptr The pointer for the motor.
 */
void pulseStepMotorPins(int motorID, int direction);
	
/**
 * Sets the correct targets for the motor. This requires converting
 * displacement values to number of steps.
 * @param[out]  motor_ptr   The pointer for the motor you want to set targets for.
 * @param[in]   motorRun    Specifies if the motor is running or is not being used
 * @param[in]   dir         The direction of the motor
 * @param[in]   newPos        The displacement you want to reach (mm or degrees). (positive or negative)
 * @param[in]   startSpeed  The speed which you start moving at (mm/s or degrees/s).
 * @param[in]   endSpeed    The speed which you stop moving at when you reach target (mm/s or degrees/s).
 */
void setMotorParams(struct Motor *motor_ptr, int motorRun, int dir, double newPos, double startSpeed, double endSpeed);

/**
 * Prints the details about the current motor.
 * @param[out] motor  The motor you want information about.
 */
void printMotorDetails(struct Motor motor);

/**
 * Finds the current position of the motor (mm or degrees).
 * @param[in] motor The motor you want to read from.
 * @return    The motor's position (mm or degrees).
 */
double getCurrentPosition(struct Motor motor);

/**
* Converts the world units (displacement:mm,deg, speed: mm/s,deg/s, acceleration: mm/s^2,deg/s^2) 
 * of the motor to step units (displacement:steps, speed: steps/s, acceleration: steps/s^2).
 * @param[in] worldUnitValue  The value in World units to be converted
 * @param[in] motor         	The motor for which this conversion is being done
 * @return  The equivalent value in steps Units ot produce the Value Units.
 */
double worldUnitsToStepUnits(double worldUnitValue, struct Motor motor);

/**
 * Calculates the number of milliseconds before each step.
 * @param[in] motor The motor being examined.
 * @return  The number of milliseconds before each step for the motor.
 */
double msPerStep(struct Motor motor);

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
 * start and end speeds in mm/s and the distance to travel in mm.
 * @param[in] startSpeedMM The start speed in mm/s
 * @param[in] endSpeedMM The end speed in mm/s
 * @param[in] distanceMM the distance to travel in mm
 * @return  Double containing the total duration of the entire movement
 */
double calculateDurationMMSEC(int startSpeedMM, int endSpeedMM, int distanceMM);

/**
 * Function to calculate the acceleration (in mm/s^2) of an instruction given the 
 * start and end speeds in mm/s and the distance to travel in mm.
 * @param[in] startSpeedMM The start speed in mm/s
 * @param[in] endSpeedMM The end speed in mm/s
 * @param[in] distanceMM the distance to travel in mm
 * @return  Double containing the constant acceleration of the entire movement
 */
double calculateAccelMMSEC(int startSpeedMM, int endSpeedMM, int distanceMM);

#endif // __MOTOR_H_
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          