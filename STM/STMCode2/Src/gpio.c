/**
  ******************************************************************************
  * File Name          : gpio.c
  * Description        : This file provides code for the configuration
  *                      of all used GPIO pins.
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
#include "gpio.h"
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/*----------------------------------------------------------------------------*/
/* Configure GPIO                                                             */
/*----------------------------------------------------------------------------*/
/* USER CODE BEGIN 1 */

/* USER CODE END 1 */

/** Configure pins as 
        * Analog 
        * Input 
        * Output
        * EVENT_OUT
        * EXTI
*/
void MX_GPIO_Init(void)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(PC13LED_GPIO_Port, PC13LED_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, ST1DIR_Pin|ST1STEP_Pin|ST1MS3_Pin|ST1MS2_Pin 
                          |ST1MS1_Pin|ST1EN_Pin|ST3DIR_Pin|ST3STEP_Pin 
                          |ST2DIR_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB, ST3MS3_Pin|ST3MS2_Pin|ST3MS1_Pin|ST3EN_Pin 
                          |LEDGREEN_Pin|LEDRED_Pin|ST2STEP_Pin|ST2MS3_Pin 
                          |ST2MS2_Pin|ST2MS1_Pin, GPIO_PIN_RESET);

	//#if defined HANDLER || defined LATHE
	/*Configure GPIO pin Output Level */
	// Used to initialise the enable pin for Motor 2 as a stepper motor
  HAL_GPIO_WritePin(GPIOB, ST2EN_Pin, GPIO_PIN_RESET);
  //#endif
	
  /*Configure GPIO pin : PC13LED_Pin */
  GPIO_InitStruct.Pin = PC13LED_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_MEDIUM;
  HAL_GPIO_Init(PC13LED_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : ST1DIR_Pin ST1STEP_Pin ST3DIR_Pin ST3STEP_Pin 
                           ST2DIR_Pin */
  GPIO_InitStruct.Pin = ST1DIR_Pin|ST1STEP_Pin|ST3DIR_Pin|ST3STEP_Pin 
                          |ST2DIR_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_MEDIUM;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pins : ST1MS3_Pin ST1MS2_Pin ST1MS1_Pin */
  GPIO_InitStruct.Pin = ST1MS3_Pin|ST1MS2_Pin|ST1MS1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_MEDIUM;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pin : ST1EN_Pin */
  GPIO_InitStruct.Pin = ST1EN_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_MEDIUM;
  HAL_GPIO_Init(ST1EN_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : ST3MS3_Pin ST3MS2_Pin ST3MS1_Pin LEDGREEN_Pin 
                           LEDRED_Pin ST2MS3_Pin ST2MS2_Pin ST2MS1_Pin */
  GPIO_InitStruct.Pin = ST3MS3_Pin|ST3MS2_Pin|ST3MS1_Pin|LEDGREEN_Pin 
                          |LEDRED_Pin|ST2MS3_Pin|ST2MS2_Pin|ST2MS1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_MEDIUM;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pin : ST3EN_Pin */
  GPIO_InitStruct.Pin = ST3EN_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_MEDIUM;
  HAL_GPIO_Init(ST3EN_GPIO_Port, &GPIO_InitStruct);

	//#if defined HANDLER || defined LATHE
	/*Configure GPIO pin : ST2EN_Pin */
	
  GPIO_InitStruct.Pin = ST2EN_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(ST3EN_GPIO_Port, &GPIO_InitStruct);
	//#endif
	
  /*Configure GPIO pins : LIMSW1_Pin LIMSW4_Pin LIMSW5_Pin */
  GPIO_InitStruct.Pin = LIMSW1_Pin|LIMSW4_Pin|LIMSW5_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pin : ST2STEP_Pin */
  GPIO_InitStruct.Pin = ST2STEP_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_MEDIUM;
  HAL_GPIO_Init(ST2STEP_GPIO_Port, &GPIO_InitStruct);

}

/* USER CODE BEGIN 2 */

/* USER CODE END 2 */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
