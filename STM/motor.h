#ifndef MOTOR_H_
#define MOTOR_H_

struct Motor {
   char* name;
   int id;
   int currentStep;
   int targetStep;
   double currentSpeed;
   double acceleration; 
   double dpr;
} motor;

void stepMotor(struct Motor *motor_ptr);
void setTargets(struct Motor *motor_ptr, double disp, double startSpeed, double endSpeed);
void setTargetSteps(struct Motor *motor_ptr, int numSteps);
void printMotorDetails(struct Motor motor);
double getCurrentDisplacement(struct Motor motor);
double displacement2steps(double displacement, struct Motor motor);

#endif // MOTOR_H_