/**
  ******************************************************************************
  * File Name          : TIM.c
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

/* Includes ------------------------------------------------------------------*/
#include <stdio.h>
#include <string.h>

#include "tim.h"
#include "main.h"
#include "motor.h"
#include "submachine.h"

/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

TIM_HandleTypeDef htim1;

//#if defined MILL || defined DRILL
//TIM_HandleTypeDef htim4;
//#endif

/* TIM1 init function */
void MX_TIM1_Init(void)
{
  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};
  TIM_BreakDeadTimeConfigTypeDef sBreakDeadTimeConfig = {0};

  htim1.Instance = TIM1;
  htim1.Init.Prescaler = 31;
  htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim1.Init.Period = 65535;
  htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim1.Init.RepetitionCounter = 0;
  htim1.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim1) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim1, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_OC_Init(&htim1) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim1, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_TIMING;
  sConfigOC.Pulse = 0;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCNPolarity = TIM_OCNPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  sConfigOC.OCIdleState = TIM_OCIDLESTATE_RESET;
  sConfigOC.OCNIdleState = TIM_OCNIDLESTATE_RESET;
  if (HAL_TIM_OC_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_OC_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_2) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_OC_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_3) != HAL_OK)
  {
    Error_Handler();
  }
  sBreakDeadTimeConfig.OffStateRunMode = TIM_OSSR_DISABLE;
  sBreakDeadTimeConfig.OffStateIDLEMode = TIM_OSSI_DISABLE;
  sBreakDeadTimeConfig.LockLevel = TIM_LOCKLEVEL_OFF;
  sBreakDeadTimeConfig.DeadTime = 0;
  sBreakDeadTimeConfig.BreakState = TIM_BREAK_DISABLE;
  sBreakDeadTimeConfig.BreakPolarity = TIM_BREAKPOLARITY_HIGH;
  sBreakDeadTimeConfig.AutomaticOutput = TIM_AUTOMATICOUTPUT_DISABLE;
  if (HAL_TIMEx_ConfigBreakDeadTime(&htim1, &sBreakDeadTimeConfig) != HAL_OK)
  {
    Error_Handler();
  }

}

/*#if defined MILL || defined DRILL
// TIM4 init function 
void MX_TIM4_Init(void)
{
  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};

  htim4.Instance = TIM4;
  htim4.Init.Prescaler = 15;
  htim4.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim4.Init.Period = 199;
  htim4.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim4.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim4) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim4, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_PWM_Init(&htim4) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim4, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = 0;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  if (HAL_TIM_PWM_ConfigChannel(&htim4, &sConfigOC, TIM_CHANNEL_2) != HAL_OK)
  {
    Error_Handler();
  }
  HAL_TIM_MspPostInit(&htim4);

}
#endif*/

void HAL_TIM_Base_MspInit(TIM_HandleTypeDef* tim_baseHandle)
{

  if(tim_baseHandle->Instance==TIM1)
  {
  /* USER CODE BEGIN TIM1_MspInit 0 */

  /* USER CODE END TIM1_MspInit 0 */
    /* TIM1 clock enable */
    __HAL_RCC_TIM1_CLK_ENABLE();
  /* USER CODE BEGIN TIM1_MspInit 1 */

  /* USER CODE END TIM1_MspInit 1 */
  }
  else if(tim_baseHandle->Instance==TIM4)
  {
  /* USER CODE BEGIN TIM4_MspInit 0 */

  /* USER CODE END TIM4_MspInit 0 */
    /* TIM4 clock enable */
    __HAL_RCC_TIM4_CLK_ENABLE();
  /* USER CODE BEGIN TIM4_MspInit 1 */

  /* USER CODE END TIM4_MspInit 1 */
  }
}
void HAL_TIM_MspPostInit(TIM_HandleTypeDef* timHandle)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};
  if(timHandle->Instance==TIM4)
  {
  /* USER CODE BEGIN TIM4_MspPostInit 0 */

  /* USER CODE END TIM4_MspPostInit 0 */
  
    __HAL_RCC_GPIOB_CLK_ENABLE();
    /**TIM4 GPIO Configuration    
    PB7     ------> TIM4_CH2 
    */
    GPIO_InitStruct.Pin = ST2EN_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_MEDIUM;
    HAL_GPIO_Init(ST2EN_GPIO_Port, &GPIO_InitStruct);

  /* USER CODE BEGIN TIM4_MspPostInit 1 */

  /* USER CODE END TIM4_MspPostInit 1 */
  }

}

void HAL_TIM_Base_MspDeInit(TIM_HandleTypeDef* tim_baseHandle)
{

  if(tim_baseHandle->Instance==TIM1)
  {
  /* USER CODE BEGIN TIM1_MspDeInit 0 */

  /* USER CODE END TIM1_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_TIM1_CLK_DISABLE();

    /* TIM1 interrupt Deinit */
    HAL_NVIC_DisableIRQ(TIM1_UP_IRQn);
    HAL_NVIC_DisableIRQ(TIM1_CC_IRQn);
  /* USER CODE BEGIN TIM1_MspDeInit 1 */

  /* USER CODE END TIM1_MspDeInit 1 */
  }
  else if(tim_baseHandle->Instance==TIM4)
  {
  /* USER CODE BEGIN TIM4_MspDeInit 0 */

  /* USER CODE END TIM4_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_TIM4_CLK_DISABLE();
  /* USER CODE BEGIN TIM4_MspDeInit 1 */

  /* USER CODE END TIM4_MspDeInit 1 */
  }
} 

/* USER CODE BEGIN 1 */
/**
  * @brief  This function is the callback from the timer update event, used to increment the sudo 32 bit timer
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the specified Timer.
  * @retval None
  */
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim) {
	incrementTimerMSHalf();
}

/**
  * @brief  This function is the callback from the timer Output Compare event, used to step the corresponding 
	* 				motor depending on which compare register matched.
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the specified Timer.
  * @retval None
  */
void HAL_TIM_OC_DelayElapsedCallback(TIM_HandleTypeDef *htim) {
	/* Capture compare 1 event */
	if(htim->Channel == HAL_TIM_ACTIVE_CHANNEL_1) {
		if(getTimerMSHalf() == getCompareMSHalf(/*Channel*/ 1)) {
				//Step Motor 1 if motor not yet at target pos
				if(isMotorFinished(getMotorById(&subMachine, /*ID*/ 1)) != 1) {
					//Step Motor 1 (including setting the new speed and uS Delay and addjusting the timePassed
					stepMotor(getMotorById(&subMachine, /*ID*/ 1));
					// Set next Compare Timer Value
					updateCompareRegister(htim, getMotorById(&subMachine, /*ID*/ 1));
				} else {
					setChannelInterrupt(htim, /*Channel*/ 1, /*Enable*/ 0);
					//HAL_TIM_OC_Stop_IT(htim, /*Channel*/ 1);
					// Disable the motor
					//enableStepperDriver(1, 0);
				}
		}
	}
  
  /* Capture compare 2 event */
	if(htim->Channel == HAL_TIM_ACTIVE_CHANNEL_2) {
		if(getTimerMSHalf() == getCompareMSHalf(/*Channel*/ 2)) {
				//Step Motor 2 if motor not yet at target pos
				if(isMotorFinished(getMotorById(&subMachine, /*ID*/ 2)) != 1) {
					//Step Motor 2 (including setting the new speed and uS Delay and addjusting the timePassed
					stepMotor(getMotorById(&subMachine, /*ID*/ 2));
					// Set next Compare Timer Value
					updateCompareRegister(htim, getMotorById(&subMachine, /*ID*/ 2));
				} else {
					setChannelInterrupt(htim, /*Channel*/ 2, /*Enable*/ 0);
					//HAL_TIM_OC_Stop_IT(htim, /*Channel*/ 2);
					// Disable the motor
					//enableStepperDriver(2, 0);
				}
			}
	}
  
  /* Capture compare 3 event */
	if(htim->Channel == HAL_TIM_ACTIVE_CHANNEL_3) {
		if(getTimerMSHalf() == getCompareMSHalf(/*Channel*/ 3)) {
				//Step Motor 3 if motor not yet at target pos
				if(isMotorFinished(getMotorById(&subMachine, /*ID*/ 3)) != 1) {
					//Step Motor 3 (including setting the new speed and uS Delay and addjusting the timePassed
					stepMotor(getMotorById(&subMachine, /*ID*/ 3));
					// Set next Compare Timer Value
					updateCompareRegister(htim, getMotorById(&subMachine, /*ID*/ 3));
				} else {
					setChannelInterrupt(htim, /*Channel*/ 3, /*Enable*/ 0);
					//HAL_TIM_OC_Stop_IT(htim, /*Channel*/ 3);
					// Disable the motor
					//enableStepperDriver(3, 0);
				}
			}
	}
}

/**
  * @brief  This function is used to reset the stepper motor interrupt timer. 
	* It disables the timer, and interrupts, sets the timer register to zero 
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the specified Timer.
  * @retval None
  */
void stepperTimerReset(TIM_HandleTypeDef *htim) {
	// Stop the timer
	HAL_TIM_Base_Stop_IT(htim);
	// Disable all channel interrupts
	HAL_TIM_OC_Stop_IT(htim, /*Channel*/ TIM_CHANNEL_1);
	HAL_TIM_OC_Stop_IT(htim, /*Channel*/ TIM_CHANNEL_2);
	HAL_TIM_OC_Stop_IT(htim, /*Channel*/ TIM_CHANNEL_3);
	// Reset the sudo 32 bit timer to zero
	setSudoTimerCounter(htim, /*newValue*/ 0);
}

/**
  * @brief  This function is used to set the required interrupts for the currently running motors
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the specified Timer.
  * @param  submachine_ptr Pointer to the submachine struct 
  * @retval None
  */
void stepperTimerSetUp(TIM_HandleTypeDef *htim, struct SubMachine *submachine_ptr) {
	// Based on which motors are running, set the timer interrupts and compare registers
	for(int i = 0; i < sizeof(submachine_ptr -> motors)/sizeof(*(submachine_ptr -> motors)); i++) {
		struct Motor *motor_ptr = getMotorById(submachine_ptr, i+1);
		
		if((motor_ptr->motorRun) == 1) {
			if(strcmp(motor_ptr -> type, "STEP") == 0) {
				// Enable the motor driver since the motor will be used
				enableStepperDriver(motor_ptr -> id, /*Enable*/ 1);
				// Set the necessary compare register value
				setSudoCompareRegister(htim, motor_ptr -> id, motor_ptr -> currentuSDelay);
				// Enable the timer interrupt on that channel
				setChannelInterrupt(htim, motor_ptr -> id, /*Enable*/ 1);
			}
		} else {
			if(strcmp(motor_ptr -> type, "STEP") == 0) {
				// Disable the timer interrupt on that channel
				setChannelInterrupt(htim, motor_ptr -> id, /*Enable*/ 0);
				// Set the necessary compare register value to zero
				setSudoCompareRegister(htim, motor_ptr -> id, 0);
				// Disable the motor driver to stop current draw.
				// May need to remove this line if holding torque is required
				#ifdef HANDLER
					if((motor_ptr->id) != 3) {
						enableStepperDriver(motor_ptr -> id, /*Enable*/ 0);
					}
				#endif
				#if defined MILL || defined DRILL || defined LATHE
					enableStepperDriver(motor_ptr -> id, /*Enable*/ 0);
				#endif
			}
		}
	}		
}

/**
  * @brief  This function is used to reset the DC motor interrupt timer. 
	* It disables the timer and sets the timer register to zero 
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the specified Timer.
  * @param  submachine_ptr Pointer to the submachine struct 
  * @retval None
  */
/*void DCTimerResetAndSetUp(TIM_HandleTypeDef *htim, struct SubMachine *submachine_ptr) {
	// Stop the timer
	HAL_TIM_PWM_Stop(htim, 2);
	// Reset the timer to zero
	__HAL_TIM_SET_COUNTER(htim, 0);
	// Based on which motors are running, set the timer interrupts and compare registers
	// TODO set these registers
	for(int i = 0; i < sizeof(submachine_ptr -> motors)/sizeof(*(submachine_ptr -> motors)); i++) {
		struct Motor *motor_ptr = getMotorById(submachine_ptr, i+1);
		if(motor_ptr -> motorRun == 1) {
			if(strcmp(motor_ptr -> type, "DC") == 0) {
				// Run the DC Motor
				setDutyCycleofPWM(htim, 2, calculatePWMDutyCycle(motor_ptr, motor_ptr -> currentSpeed));
				//setDutyCycleofPWM(htim, 2, calculatePWMDutyCycle(motor_ptr, 50));
				// Enable the Capture compare channel
				//TIM_CCxChannelCmd(htim->Instance, TIM_CHANNEL_2, TIM_CCx_ENABLE);
				HAL_TIM_PWM_Start(htim, TIM_CHANNEL_2);
			}
		} else {
			if(strcmp(motor_ptr -> type, "DC") == 0) {
				// Disable the DC motor Timer
				// Disable the Capture compare channel
				//TIM_CCxChannelCmd(htim->Instance, TIM_CHANNEL_2, TIM_CCx_DISABLE);
				setDutyCycleofPWM(htim, 2, 0);
			}
		}
	}		
}*/

/**
  * @brief  This function is used to start or stop the specified timer counting 
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the specified Timer. 
  * @param  newState Integer (0 or 1) indicating whether to start or stop the timer (enable or disable)
  * @retval None
  */
void startOrStopTimer(TIM_HandleTypeDef *htim, int newState) {
	if(newState == 1) {
		/* Enable the Peripheral */
		__HAL_TIM_ENABLE(htim);
	} else {
		/* Disable the Peripheral */
		__HAL_TIM_DISABLE(htim);
	}
}

/**
  * @brief  This function is used to get the sudo 32 bit timer counter. 
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the Least Significant Half of the timer.
  * @param  channel the channel for the capture compare
  * @retval the sudo 32 bit timer value
  */
uint32_t getSudoTimerCounter(TIM_HandleTypeDef *htim, int channel) {
	uint32_t counterValue;
	uint16_t counterValueLSH;
	uint16_t counterValueMSH;
	
	// Get the Least Significant Half of the timer
	//counterValueLSH = __HAL_TIM_GET_COUNTER(htim);
	switch(channel) {
		case 1:
			counterValueLSH = __HAL_TIM_GET_COMPARE(htim, TIM_CHANNEL_1);
			break;
		case 2:
			counterValueLSH = __HAL_TIM_GET_COMPARE(htim, TIM_CHANNEL_2);
			break;
		case 3:
			counterValueLSH = __HAL_TIM_GET_COMPARE(htim, TIM_CHANNEL_3);
			break;
	}
	
	
	// Get the Most Significant Half of the timer
	counterValueMSH = getTimerMSHalf();
	// Set the counterValue to the combination of the MSHalf and LSHalf
	counterValue = (uint32_t)(((counterValueMSH << 16) & 0xFFFF0000) | counterValueLSH);
	return counterValue;
}

/**
  * @brief  This function is used to set the sudo 32 bit timer counter to a specific value. 
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the Least Significant Half of the timer.
  * @param  newValue The new value to be put into the timer 
  * @retval None
  */
void setSudoTimerCounter(TIM_HandleTypeDef *htim, uint32_t newValue) {
	// Set the value of the Least Significant Half of the Timer Counter register 
	// to the lower half of newValue
	__HAL_TIM_SET_COUNTER(htim, (uint16_t)(newValue & 0xFFFF));
	// Set the value of the Most Significant Half of the Timer Counter register 
	// to the upper half of newValue
	setTimerMSHalf((uint16_t)((newValue & 0xFFFF0000) >> 16));
}

/**
  * @brief  This function is used to get the sudo 32 bit timer compare value for a specified channel. 
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the Least Significant Half of the timer. 
  * @param  channel the channel of the compare register
  * @retval the sudo 32 bit timer compare register value
  */
uint32_t getSudoTimerCompare(TIM_HandleTypeDef *htim, int channel) {
	uint32_t compareValue;
	uint16_t compareValueLSH;
	uint16_t compareValueMSH;
	// Get the Least Significant Half of the timer
	switch(channel) {
		case 1:
			compareValueLSH = __HAL_TIM_GET_COMPARE(htim, TIM_CHANNEL_1);
			break;
		case 2:
			compareValueLSH = __HAL_TIM_GET_COMPARE(htim, TIM_CHANNEL_2);
			break;
		case 3:
			compareValueLSH = __HAL_TIM_GET_COMPARE(htim, TIM_CHANNEL_3);
			break;
	}
	// Get the Most Significant Half of the timer
	compareValueMSH = getTimerMSHalf();
	// Set the counterValue to the combination of the MSHalf and LSHalf
	compareValue = (uint32_t)(((compareValueMSH << 16) & 0xFFFF0000) | compareValueLSH);
	return compareValue;
}

/**
  * @brief  This function is used to set the sudo 32 bit timer compare to a specific value. 
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the Least Significant Half of the timer.
	* @param	channel The channel whose compare register is being adjusted
  * @param  newValue The new value to be put into the compare register 
  * @retval None
  */
void setSudoCompareRegister(TIM_HandleTypeDef *htim, int channel, uint32_t newValue) {
	// Set the value of the Least Significant Half of the Timer compare register 
	// to the lower half of newValue
	switch(channel) {
		case 1:
			__HAL_TIM_SET_COMPARE(htim, TIM_CHANNEL_1, (uint16_t)(newValue & 0xFFFF));
			break;
		case 2:
			__HAL_TIM_SET_COMPARE(htim, TIM_CHANNEL_2, (uint16_t)(newValue & 0xFFFF));
			break;
		case 3:
			__HAL_TIM_SET_COMPARE(htim, TIM_CHANNEL_3, (uint16_t)(newValue & 0xFFFF));
			break;
	}
	// Set the value of the Most Significant Half of the compare register 
	// to the upper half of newValue
	setCompareMSHalf(channel,(uint16_t)((newValue & 0xFFFF0000) >> 16));
}

/**
  * @brief  This function is used to enable or diable timer output compare channel interrupts 
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the Least Significant Half of the timer.
	* @param	channel The channel whose interrupt is being adjusted
  * @param  enable The indication of whether the interrupt should be enable or disabled
  * @retval None
  */
void setChannelInterrupt(TIM_HandleTypeDef *htim, int channel, int enable) {
	// Based on which channel is selected, choose the corresponding interrupt to enable or disable
	switch(channel) {
		case 1: if(enable == 1) {
				__HAL_TIM_ENABLE_IT(htim, TIM_IT_CC1);
			} else {
				__HAL_TIM_DISABLE_IT(htim, TIM_IT_CC1);
			}
			break;
		case 2: if(enable == 1) {
				__HAL_TIM_ENABLE_IT(htim, TIM_IT_CC2);
			} else {
				__HAL_TIM_DISABLE_IT(htim, TIM_IT_CC2);
			}
			break;
		case 3: if(enable == 1) {
				__HAL_TIM_ENABLE_IT(htim, TIM_IT_CC3);
			} else {
				__HAL_TIM_DISABLE_IT(htim, TIM_IT_CC3);
			}
			break;
	}
}

/**
  * @brief  This function is used to calculate and set the new compare register value for the specified motor
	* 				based on the current speed and uS Delay
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for the Least Significant Half of the timer.
	* @param	motor_ptr the motor that for which the compare reister is being changed
  * @retval None
  */
void updateCompareRegister(TIM_HandleTypeDef *htim, struct Motor *motor_ptr) {
	// Based on which motor is used, get the motor ID
	int motorID = getMotorID(motor_ptr);
	
	/* ___One of the following is used, either the previous compare register value or the current timer value___ */
	// Get the current count of the timer specified by htim
	uint32_t timerCount = getSudoTimerCounter(htim,/* Channel*/ motorID);
	// Get the previous compare register value
	//uint32_t prevCompareValue = getSudoTimerCompare(htim, motorID);
	// Set the new compare value based off the current timer value
	uint32_t newCompareValue = timerCount + getMotoruSDelay(motor_ptr);
	// Set the new compare value based off the old compare value
	//uint32_t newCompareValue = prevCompareValue + getMotoruSDelay(motor_ptr);
	/* ______ */
	
	// Set the new timer compare register value for the specified channel (motorID)
	setSudoCompareRegister(htim, /*Channel*/ motorID, /*newValue*/ newCompareValue);
}

/**
  * @brief  This function is used to set the PWM duty cycle by setting the output compare register value
  * @param  htim Pointer to a TIM_HandleTypeDef structure that contains
  *                the configuration information for timer.
	* @param	channel the channel for which the DutyCycle is being set
	* @param	dutyCycle the dutyCycle of the PWM (percentage from 0 to 100)
  * @retval None
  */
/*void setDutyCycleofPWM(TIM_HandleTypeDef *htim, int channel, int dutyCycle) {
	// Calculate the required compare value
	uint16_t newCompareValue = (uint16_t)(200*dutyCycle/100);
	// Determine which channel is being set
	switch(channel) {
		case 1: 
			__HAL_TIM_SET_COMPARE(htim, TIM_CHANNEL_1, newCompareValue); 
			break;
		case 2: 
			__HAL_TIM_SET_COMPARE(htim, TIM_CHANNEL_2, newCompareValue); 
			break;
		case 3: 
			__HAL_TIM_SET_COMPARE(htim, TIM_CHANNEL_3, newCompareValue); 
			break;
		case 4: 
			__HAL_TIM_SET_COMPARE(htim, TIM_CHANNEL_4, newCompareValue); 
			break;
	}
}*/
/* USER CODE END 1 */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
