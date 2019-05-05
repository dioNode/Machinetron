/**
  ******************************************************************************
  * File Name          : I2C.c
  * Description        : This file provides code for the configuration
  *                      of the I2C instances.
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

#include "i2c.h"
#include "main.h"
#include "usart.h"
#include "submachine.h"
#include "motor.h"



/* USER CODE BEGIN 0 */
/*____________________I2C Constant Definitions____________________*/
#define I2C_CLOCKSPEED 			400000
#define I2C_DUTYCYCLE 			I2C_DUTYCYCLE_2
#define I2C_ADDRESS 				0x1F
/* USER CODE END 0 */

I2C_HandleTypeDef hi2c1;

/* I2C1 init function */
void MX_I2C1_Init(void)
{

  hi2c1.Instance 							= I2Cx;
  hi2c1.Init.ClockSpeed 			= I2C_CLOCKSPEED;
  hi2c1.Init.DutyCycle 				= I2C_DUTYCYCLE;
  hi2c1.Init.OwnAddress1 			= I2C_ADDRESS<<1;
  hi2c1.Init.AddressingMode 	= I2C_ADDRESSINGMODE_7BIT;
  hi2c1.Init.DualAddressMode 	= I2C_DUALADDRESS_DISABLE;
  hi2c1.Init.OwnAddress2 			= 0;
  hi2c1.Init.GeneralCallMode 	= I2C_GENERALCALL_ENABLE;
  hi2c1.Init.NoStretchMode 		= I2C_NOSTRETCH_DISABLE;
  if (HAL_I2C_Init(&hi2c1) != HAL_OK)
  {
    Error_Handler();
  }

}

void HAL_I2C_MspInit(I2C_HandleTypeDef* i2cHandle)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};
  if(i2cHandle->Instance==I2C1)
  {
  /* USER CODE BEGIN I2C1_MspInit 0 */

  /* USER CODE END I2C1_MspInit 0 */
  
    __HAL_RCC_GPIOB_CLK_ENABLE();
    /**I2C1 GPIO Configuration    
    PB8     ------> I2C1_SCL
    PB9     ------> I2C1_SDA 
    */
    GPIO_InitStruct.Pin = I2CCLK_Pin|I2CSDA_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_OD;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    __HAL_AFIO_REMAP_I2C1_ENABLE();

    /* I2C1 clock enable */
    __HAL_RCC_I2C1_CLK_ENABLE();
  /* USER CODE BEGIN I2C1_MspInit 1 */

  /* USER CODE END I2C1_MspInit 1 */
  }
}

void HAL_I2C_MspDeInit(I2C_HandleTypeDef* i2cHandle)
{

  if(i2cHandle->Instance==I2C1)
  {
  /* USER CODE BEGIN I2C1_MspDeInit 0 */

  /* USER CODE END I2C1_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_I2C1_CLK_DISABLE();
  
    /**I2C1 GPIO Configuration    
    PB8     ------> I2C1_SCL
    PB9     ------> I2C1_SDA 
    */
    HAL_GPIO_DeInit(GPIOB, I2CCLK_Pin|I2CSDA_Pin);

    /* I2C1 interrupt Deinit */
    HAL_NVIC_DisableIRQ(I2C1_EV_IRQn);
    HAL_NVIC_DisableIRQ(I2C1_ER_IRQn);
  /* USER CODE BEGIN I2C1_MspDeInit 1 */

  /* USER CODE END I2C1_MspDeInit 1 */
  }
} 

/* USER CODE BEGIN 1 */
/**
  * @brief  This function sets up the I2C interface in slave mode for transmit or receive
	*					depending on the read/write bit sent from the master
  * @param  hi2c Pointer to a I2C_HandleTypeDef structure that contains
  *                the configuration information for the specified I2C.
  * @param  TrasnferDirection Data direction request from master (I2C_DIRECTION_RECEIVE, I2C_DIRECTION_TRANSMIT)
  * @param  AddrMatchCode Address match code, corresponding to which dual address was matched
  * @retval HAL status
  */
void HAL_I2C_AddrCallback(I2C_HandleTypeDef *hi2c, uint8_t TransferDirection, uint16_t AddrMatchCode) {
	
	// If the Transfer Direction is set as I2C_DIRECTION_RECEIVE, set the I2C peripheral in SLAVE mode
	// as a transmitter
	if (TransferDirection == I2C_DIRECTION_RECEIVE) {
		//printf("TransferDirectionReceive\n");
		if(HAL_I2C_Slave_Sequential_Transmit_IT(hi2c, getI2CTransmitBuffer(), TXBUFFERSIZE,I2C_LAST_FRAME) != HAL_OK) {
			// Transfer error in reception process
			Error_Handler();
		}
		
	} 
	else {
		//printf("TransferDirectionTransmit\n");
		if(HAL_I2C_Slave_Sequential_Receive_IT(hi2c, getI2CReceiveBuffer(), RXBUFFERSIZE,I2C_FIRST_FRAME) != HAL_OK) {
			// Transfer error in transmition process
			Error_Handler();
		}
		
	}
	
	// Clear the ADDR Flag
	__HAL_I2C_CLEAR_ADDRFLAG(hi2c);
	
	// Turn on the PC13 LED
	HAL_GPIO_WritePin(PC13LED_GPIO_Port,PC13LED_Pin,GPIO_PIN_SET);

}

/**
  * @brief  This function is called when the I2C is finished Listening
	*					Must reinitialise the Listening
  * @param  hi2c Pointer to a I2C_HandleTypeDef structure that contains
  *                the configuration information for the specified I2C.
  */
void HAL_I2C_ListenCpltCallback(I2C_HandleTypeDef *hi2c) {
	// Reinstate the Listening Mode for the I2C bus
	
	if(HAL_I2C_EnableListen_IT(hi2c) != HAL_OK)
  {
    // Transfer error in reception process
    Error_Handler();        
  }
	
	// Depending on the initial instruction byte put the data in the intruction array 
	// or put the machine into the required state
	
	if(getI2CReceiveBuffer()[0] == NORM_INST) {
		// Standard straight path instruction received
		// For every element in the receive buffer, add it to the First Empty Index of the instructionArray
		//HAL_UART_Transmit(&huart1,(uint8_t *)getI2CReceiveBuffer(),getI2CReceiveSize(),HAL_MAX_DELAY);
	  //HAL_UART_Transmit(&huart1,(uint8_t *)"\n",sizeof("\n"),HAL_MAX_DELAY);
		//printArray(getI2CReceiveBuffer());
		//HAL_UART_Transmit(&huart1,(uint8_t *)"\n",sizeof("\n"),HAL_MAX_DELAY);
		for(int i = 0; i < (getI2CReceiveSize() - 1); i++) {
			setInstructionArrayAtIndex(getI2CReceiveBuffer()[i+1], getInstArrayFirstEmptyIndex(), i);
		}
		//HAL_UART_Transmit(&huart1,(uint8_t *)getInstructionAtIndex(getInstArrayFirstIndex()),getI2CReceiveSize(),HAL_MAX_DELAY);
	  //HAL_UART_Transmit(&huart1,(uint8_t *)"\n",sizeof("\n"),HAL_MAX_DELAY);
		// Increment the first empty index
		incrementFirstEmptyIndex();
	} else if(getI2CReceiveBuffer()[0] == START_INST) {
		//printf("%d", getI2CReceiveBuffer()[0]);
		// A Start instruction was sent, initiate the machine into a running state
		setMachineState(MACHINE_RUNNING);
	} else if(getI2CReceiveBuffer()[0] == PAUSE_INST) {
		// A Pause instruction was sent, set the machine into a pause state
		setMachineState(MACHINE_PAUSED);
	}
	
	
	// Turn off the PC13 LED
	HAL_GPIO_WritePin(PC13LED_GPIO_Port,PC13LED_Pin,GPIO_PIN_RESET);
	//printf("ListenCpltCallback\n");
	//HAL_UART_Transmit(&huart1,(uint8_t *)getI2CReceiveBuffer(),getI2CReceiveSize(),HAL_MAX_DELAY);
	//HAL_UART_Transmit(&huart1,(uint8_t *)"\n",sizeof("\n"),HAL_MAX_DELAY);
	
	//Empty the transmit and receive buffers ready for the next transmission
	Flush_Buffer(getI2CReceiveBuffer(), getI2CReceiveSize());
	Flush_Buffer(getI2CTransmitBuffer(), getI2CTransmitSize());
}

/**
  * @brief  This function is called when the I2C is finished transmitting all data in Slave mode
  * @param  hi2c Pointer to a I2C_HandleTypeDef structure that contains
  *                the configuration information for the specified I2C.
  */
void HAL_I2C_SlaveTxCpltCallback(I2C_HandleTypeDef *hi2c) {
	// Turn off PC13 LED
	HAL_GPIO_WritePin(PC13LED_GPIO_Port,PC13LED_Pin,GPIO_PIN_RESET);
	//HAL_UART_Transmit(&UartDebugHandle,TransmitBuf,RXBUFFERSIZE,HAL_MAX_DELAY);
	//HAL_UART_Transmit(&UartDebugHandle,newline,RXBUFFERSIZE,HAL_MAX_DELAY);
	//printf("SlaveTxCpltCallback\n");
}

/**
  * @brief  This function is called when the I2C is finished receiving all data in Slave mode
  * @param  hi2c Pointer to a I2C_HandleTypeDef structure that contains
  *                the configuration information for the specified I2C.
  */
void HAL_I2C_SlaveRxCpltCallback(I2C_HandleTypeDef *hi2c)
{
	// If the first byte written is requesting a read then put the respective data in the transmit buffer
	switch(getI2CReceiveBuffer()[0]) {
		case READ_INST_SPEED_M1:
			setI2CTransmitBufferAtIndex((uint8_t)(((int)(getMotorCurrentSpeed(getMotorById(&subMachine, 1))) >> 8) & 0xFF), 0);
			setI2CTransmitBufferAtIndex((uint8_t)((int)(getMotorCurrentSpeed(getMotorById(&subMachine, 1))) & 0xFF), 1);
			break;
		case READ_INST_SPEED_M2:
			setI2CTransmitBufferAtIndex((uint8_t)(((int)(getMotorCurrentSpeed(getMotorById(&subMachine, 2))) >> 8) & 0xFF), 0);
			setI2CTransmitBufferAtIndex((uint8_t)((int)(getMotorCurrentSpeed(getMotorById(&subMachine, 2))) & 0xFF), 1);
			break;
		case READ_INST_SPEED_M3:
			setI2CTransmitBufferAtIndex((uint8_t)(((int)(getMotorCurrentSpeed(getMotorById(&subMachine, 3))) >> 8) & 0xFF), 0);
			setI2CTransmitBufferAtIndex((uint8_t)((int)(getMotorCurrentSpeed(getMotorById(&subMachine, 3))) & 0xFF), 1);
			break;
		case READ_INST_POS_M1:
			setI2CTransmitBufferAtIndex((uint8_t)(((int)(getMotorCurrentStep(getMotorById(&subMachine, 1))) >> 8) & 0xFF), 0);
			setI2CTransmitBufferAtIndex((uint8_t)((int)(getMotorCurrentStep(getMotorById(&subMachine, 1))) & 0xFF), 1);
			break;
		case READ_INST_POS_M2:
			setI2CTransmitBufferAtIndex((uint8_t)(((int)(getMotorCurrentStep(getMotorById(&subMachine, 2))) >> 8) & 0xFF), 0);
			setI2CTransmitBufferAtIndex((uint8_t)((int)(getMotorCurrentStep(getMotorById(&subMachine, 2))) & 0xFF), 1);
			break;
		case READ_INST_POS_M3:
			setI2CTransmitBufferAtIndex((uint8_t)(((int)(getMotorCurrentStep(getMotorById(&subMachine, 3))) >> 8) & 0xFF), 0);
			setI2CTransmitBufferAtIndex((uint8_t)((int)(getMotorCurrentStep(getMotorById(&subMachine, 3))) & 0xFF), 1);
			break;
		case READ_MACHINE_STATE:
			setI2CTransmitBufferAtIndex((uint8_t)(((int)(getMachineState()) >> 8) & 0xFF), 0);
			setI2CTransmitBufferAtIndex((uint8_t)((int)(0x00) & 0xFF), 1);
			break;
	}
	
	// Turn on PC13 LED
	HAL_GPIO_WritePin(PC13LED_GPIO_Port,PC13LED_Pin,GPIO_PIN_SET);
	//printf("SlaveRxCpltCallback\n");
}
/* USER CODE END 1 */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
