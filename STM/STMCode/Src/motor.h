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
   int currentStep;     // The current number of steps
   int targetStep;      // The number of steps it needs to reach
   double currentSpeed; // The current step speed (steps/s)
   double acceleration; // The step acceleration (steps/s^2)
   double dpr;          // Displacement per revolution of motor
   int msSinceLastStep; // Number of milliseconds since last step
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
 * Sets the correct targets for the motor. This requires converting
 * displacement values to number of steps.
 * @param[out]  motor_ptr   The pointer for the motor you want to set targets for.
 * @param[in]   disp        The displacement you want to reach (mm).
 * @param[in]   startSpeed  The speed which you start moving at (mm/s).
 * @param[in]   endSpeed    The speed which you stop moving at when you reach target (mm/s).
 */
void setTargets(struct Motor *motor_ptr, double disp, double startSpeed, double endSpeed);

/**
 * Prints the details about the current motor.
 * @param[out] motor  The motor you want information about.
 */
void printMotorDetails(struct Motor motor);

/**
 * Finds the current displacement of your motor (mm or degrees).
 * @param[in] motor The motor you want to read from.
 * @return    The motor's displacement (mm or degrees).
 */
double getCurrentDisplacement(struct Motor motor);

/**
 * Converts the displacement of the motor to step number.
 * @param[in] displacement  The displacement you want to convert.
 * @param[in] motor         The motor you wish to examine.
 * @return  The equivalent number of steps taken to move displacement.
 */
double displacement2steps(double displacement, struct Motor motor);

/**
 * Calculates the number of milliseconds before each step.
 * @param[in] motor The motor being examined.
 * @return  The number of milliseconds before each step for the motor.
 */
double msPerStep(struct Motor motor);

#endif // __MOTOR_H_
