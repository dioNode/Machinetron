/**
  ******************************************************************************
  * File Name          : TIM.h
  * Description        : This file provides code for the configuration
  *                      of the TIM instances.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2019 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __tim_H
#define __tim_H
#ifdef __cplusplus
 extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "motor.h"

/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

extern TIM_HandleTypeDef htim1;
extern TIM_HandleTypeDef htim4;

/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

void MX_TIM1_Init(void);
void MX_TIM4_Init(void);
                        
void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);
                    
/* USER CODE BEGIN Prototypes */
/**
  * @brief  This function is the callback from the timer update event, used to increment the sudo 32 bit timer
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the specified Timer.
  * @retval None
  */
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim);

/**
  * @brief  This function is the callback from the timer Output Compare event, used to step the corresponding 
	* 				motor depending on which compare register matched.
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the specified Timer.
  * @retval None
  */
void HAL_TIM_OC_DelayElapsedCallback(TIM_HandleTypeDef *htim);

/**
  * @brief  This function is used to reset the stepper motor interrupt timer. 
	* It disables the timer, and interrupts, sets the timer register to zero 
	* and sets the required interrupts for the currently running motors
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the specified Timer.
  * @param  submachine_ptr Pointer to the submachine struct 
  * @retval None
  */
void stepperTimerResetAndSetUp(TIM_HandleTypeDef *htim, struct SubMachine *submachine_ptr);
	
/**
  * @brief  This function is used to reset the DC motor interrupt timer. 
	* It disables the timer and sets the timer register to zero 
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the specified Timer.
  * @param  submachine_ptr Pointer to the submachine struct 
  * @retval None
  */
void DCTimerResetAndSetUp(TIM_HandleTypeDef *htim, struct SubMachine *submachine_ptr);
	
/**
  * @brief  This function is used to start or stop the specified timer counting 
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the specified Timer. 
  * @param  newState Integer (0 or 1) indicating whether to start or stop the timer (enable or disable)
  * @retval None
  */
void startOrStopTimer(TIM_HandleTypeDef *htim, int newState);

/**
  * @brief  This function is used to get the sudo 32 bit timer counter. 
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the Least Significant Half of the timer.
  * @param  channel the channel for the capture compare
  * @retval the sudo 32 bit timer value
  */
uint32_t getSudoTimerCounter(TIM_HandleTypeDef *htim, int channel);

/**
  * @brief  This function is used to set the sudo 32 bit timer counter to a specific value. 
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the Least Significant Half of the timer.
  * @param  newValue The new value to be put into the timer 
  * @retval None
  */
void setSudoTimerCounter(TIM_HandleTypeDef *htim, uint32_t newValue);

/**
  * @brief  This function is used to get the sudo 32 bit timer compare value for a specified channel. 
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the Least Significant Half of the timer. 
  * @param  channel the channel of the compare register
  * @retval the sudo 32 bit timer compare register value
  */
uint32_t getSudoTimerCompare(TIM_HandleTypeDef *htim, int channel);
	
/**
  * @brief  This function is used to set the sudo 32 bit timer compare to a specific value. 
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the Least Significant Half of the timer.
	* @param	channel The channel whose compare register is being adjusted
  * @param  newValue The new value to be put into the compare register 
  * @retval None
  */
void setSudoCompareRegister(TIM_HandleTypeDef *htim, int channel, uint32_t newValue);

/**
  * @brief  This function is used to enable or diable timer output compare channel interrupts 
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the Least Significant Half of the timer.
	* @param	channel The channel whose interrupt is being adjusted
  * @param  enable The indication of whether the interrupt should be enable or disabled
  * @retval None
  */
void setChannelInterrupt(TIM_HandleTypeDef *htim, int channel, int enable);

/**
  * @brief  This function is used to calculate and set the new compare register value for the specified motor
	* 				based on the current speed and uS Delay
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the Least Significant Half of the timer.
	* @param	motor_ptr the motor that for which the compare reister is being changed
  * @retval None
  */
void updateCompareRegister(TIM_HandleTypeDef *htim, struct Motor *motor_ptr);

/**
  * @brief  This function is used to set the PWM duty cycle by setting the output compare register value
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for timer.
	* @param	channel the channel for which the DutyCycle is being set
	* @param	dutyCycle the dutyCycle of the PWM (percentage from 0 to 100)
  * @retval None
  */
void setDutyCycleofPWM(TIM_HandleTypeDef *htim, int channel, int dutyCycle);
/* USER CODE END Prototypes */

#ifdef __cplusplus
}
#endif
#endif /*__ tim_H */

/**
  * @}
  */

/**
  * @}
  */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
