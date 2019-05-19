/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
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
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"


/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */
/* Definition for I2Cx clock resources */
#define I2Cx                            I2C1
#define I2Cx_CLK_ENABLE()               __HAL_RCC_I2C1_CLK_ENABLE()
#define I2Cx_SDA_GPIO_CLK_ENABLE()      __HAL_RCC_GPIOB_CLK_ENABLE()
#define I2Cx_SCL_GPIO_CLK_ENABLE()      __HAL_RCC_GPIOB_CLK_ENABLE() 

#define I2Cx_FORCE_RESET()              __HAL_RCC_I2C1_FORCE_RESET()
#define I2Cx_RELEASE_RESET()            __HAL_RCC_I2C1_RELEASE_RESET()

/* Definition for I2Cx Pins */
#define I2Cx_SCL_PIN                    GPIO_PIN_8
#define I2Cx_SCL_GPIO_PORT              GPIOB
#define I2Cx_SDA_PIN                    GPIO_PIN_9
#define I2Cx_SDA_GPIO_PORT              GPIOB

/* Definition for I2Cx's NVIC */
#define I2Cx_EV_IRQn                    I2C1_EV_IRQn
#define I2Cx_ER_IRQn                    I2C1_ER_IRQn
#define I2Cx_EV_IRQHandler              I2C1_EV_IRQHandler
#define I2Cx_ER_IRQHandler              I2C1_ER_IRQHandler


/*____________________User Exported Defines____________________*/
/* Size of Transmission buffer */
#define RXBUFFERSIZE     								28

/* Size of Reception buffer */
#define TXBUFFERSIZE                    2

/* Size of Debug buffer */
#define DEBUGBUFFERSIZE                 16

/* Total number of instructions that can be stored */
#define INST_ARRAY_LENGTH               200

/* Length of One Instruction */
#define INST_LENGTH               			28

/* Intruction Type Byte Constants */
#define NORM_INST												0x00
#define START_INST											0x01
#define PAUSE_INST											0x02
#define STOP_INST												0x03

#define READ_INST_SPEED_M1							0x04
#define READ_INST_SPEED_M2							0x05
#define READ_INST_SPEED_M3							0x06

#define READ_INST_POS_M1								0x07
#define READ_INST_POS_M2								0x08
#define READ_INST_POS_M3								0x09

#define READ_MACHINE_STATE							0x0A
//#define READ_INST_MOTORS_RUNNING				0x0B


/* Motor Identifier Byte Constants */
#define MOTOR_BITS_SHIFT								6
#define MOTOR1													0x01 << MOTOR_BITS_SHIFT							
#define MOTOR2													0x02 << MOTOR_BITS_SHIFT
#define MOTOR3													0x03 << MOTOR_BITS_SHIFT
#define MOTOR_BITS_MASK									0xC0

#define DIR_BIT_SHIFT										5
#define DIR_FORWARD											0x01 << DIR_BIT_SHIFT
#define DIR_REVERSE											0x00 << DIR_BIT_SHIFT
#define DIR_BIT_MASK										0x01 << DIR_BIT_SHIFT

#define MOTOR_RUN_BIT_SHIFT							4
#define MOTOR_RUN												0x01 << MOTOR_RUN_BIT_SHIFT
#define MOTOR_STOP											0x00 << MOTOR_RUN_BIT_SHIFT
#define MOTOR_RUN_BIT_MASK							0x01 << MOTOR_RUN_BIT_SHIFT

#define HOME_MOTOR_BIT_SHIFT						3
#define HOME_MOTOR											0x01 << HOME_MOTOR_BIT_SHIFT
#define HOME_MOTOR_BIT_MASK							0x01 << HOME_MOTOR_BIT_SHIFT

#define INF_SPIN_BIT_SHIFT							2
#define INF_SPIN												0x01 << INF_SPIN_BIT_SHIFT
#define INF_SPIN_BIT_MASK								0x01 << INF_SPIN_BIT_SHIFT

// Constants defining the state of the Submachine
#define MACHINE_READY										0x01
#define MACHINE_RUNNING									0x02
#define MACHINE_PAUSED									0x03

// Constant to define the location of various Bytes in the Instruction Array
#define MOTOR1_BYTE_LOC										0
#define MOTOR2_BYTE_LOC										7
#define MOTOR3_BYTE_LOC										14

#define M1_TARGET_POS_MSHALF_LOC					1				
#define M1_TARGET_POS_LSHALF_LOC					2
#define M1_START_SPEED_MSHALF_LOC					3
#define M1_START_SPEED_LSHALF_LOC					4
#define M1_END_SPEED_MSHALF_LOC						5
#define M1_END_SPEED_LSHALF_LOC						6

#define M2_TARGET_POS_MSHALF_LOC					8				
#define M2_TARGET_POS_LSHALF_LOC					9
#define M2_START_SPEED_MSHALF_LOC					10
#define M2_START_SPEED_LSHALF_LOC					11
#define M2_END_SPEED_MSHALF_LOC						12
#define M2_END_SPEED_LSHALF_LOC						13

#define M3_TARGET_POS_MSHALF_LOC					15				
#define M3_TARGET_POS_LSHALF_LOC					16
#define M3_START_SPEED_MSHALF_LOC					17
#define M3_START_SPEED_LSHALF_LOC					18
#define M3_END_SPEED_MSHALF_LOC						19
#define M3_END_SPEED_LSHALF_LOC						20
/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

void Flush_Buffer(uint8_t* pBuffer, uint16_t BufferLength);

uint8_t* getI2CReceiveBuffer(void);

int getI2CReceiveSize(void);

void setI2CReceiveBufferAtIndex(uint8_t value, int index);

uint8_t* getI2CTransmitBuffer(void);

int getI2CTransmitSize(void);

void setI2CTransmitBufferAtIndex(uint8_t value, int index);
	
uint8_t getMachineState(void);

void setMachineState(int newState);
	
uint8_t* getInstructionArray(void);

uint8_t* getInstructionAtIndex(int index);

void setInstructionArrayAtIndex(uint8_t value, int intrIndex, int byteIndex);

int getInstArrayFirstIndex(void);

int getInstArrayFirstEmptyIndex(void);

void incrementFirstEmptyIndex(void);

void incrementFirstIndex(void);

uint16_t getTimerMSHalf(void);

void setTimerMSHalf(uint16_t newValue);
	
void incrementTimerMSHalf(void);

uint16_t getCompareMSHalf(int channel);

void setCompareMSHalf(int channel, uint16_t value);

void setLEDColour(char* colour);

void printInteger(char* leadingString, int len, int intNum);

int roundNumToInt(double number);

void stopCurrentInstruction(void);

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define PC13LED_Pin GPIO_PIN_13
#define PC13LED_GPIO_Port GPIOC
#define ST1DIR_Pin GPIO_PIN_0
#define ST1DIR_GPIO_Port GPIOA
#define ST1STEP_Pin GPIO_PIN_1
#define ST1STEP_GPIO_Port GPIOA
#define ST1MS3_Pin GPIO_PIN_2
#define ST1MS3_GPIO_Port GPIOA
#define ST1MS2_Pin GPIO_PIN_3
#define ST1MS2_GPIO_Port GPIOA
#define ST1MS1_Pin GPIO_PIN_4
#define ST1MS1_GPIO_Port GPIOA
#define ST1EN_Pin GPIO_PIN_5
#define ST1EN_GPIO_Port GPIOA
#define ST3DIR_Pin GPIO_PIN_6
#define ST3DIR_GPIO_Port GPIOA
#define ST3STEP_Pin GPIO_PIN_7
#define ST3STEP_GPIO_Port GPIOA
#define ST3MS3_Pin GPIO_PIN_0
#define ST3MS3_GPIO_Port GPIOB
#define ST3MS2_Pin GPIO_PIN_1
#define ST3MS2_GPIO_Port GPIOB
#define ST3MS1_Pin GPIO_PIN_10
#define ST3MS1_GPIO_Port GPIOB
#define ST3EN_Pin GPIO_PIN_11
#define ST3EN_GPIO_Port GPIOB
#define LEDRED_Pin GPIO_PIN_14
#define LEDRED_GPIO_Port GPIOB
#define LEDGREEN_Pin GPIO_PIN_15
#define LEDGREEN_GPIO_Port GPIOB
#define LIMSW1_Pin GPIO_PIN_8
#define LIMSW1_GPIO_Port GPIOA
#define USARTTX_Pin GPIO_PIN_9
#define USARTTX_GPIO_Port GPIOA
#define USARTRX_Pin GPIO_PIN_10
#define USARTRX_GPIO_Port GPIOA
#define LIMSW4_Pin GPIO_PIN_11
#define LIMSW4_GPIO_Port GPIOA
#define LIMSW5_Pin GPIO_PIN_12
#define LIMSW5_GPIO_Port GPIOA
#define ST2DIR_Pin GPIO_PIN_15
#define ST2DIR_GPIO_Port GPIOA
#define ST2STEP_Pin GPIO_PIN_3
#define ST2STEP_GPIO_Port GPIOB
#define ST2MS3_Pin GPIO_PIN_4
#define ST2MS3_GPIO_Port GPIOB
#define ST2MS2_Pin GPIO_PIN_5
#define ST2MS2_GPIO_Port GPIOB
#define ST2MS1_Pin GPIO_PIN_6
#define ST2MS1_GPIO_Port GPIOB
#define ST2EN_Pin GPIO_PIN_7
#define ST2EN_GPIO_Port GPIOB
#define I2CCLK_Pin GPIO_PIN_8
#define I2CCLK_GPIO_Port GPIOB
#define I2CSDA_Pin GPIO_PIN_9
#define I2CSDA_GPIO_Port GPIOB
/* USER CODE BEGIN Private defines */
/*___________________Definition of current submachine____________________*/
//#define HANDLER
//#define LATHE
#define MILL
//#define DRILL

// Define the submachine variable as global across files
extern struct SubMachine subMachine;
/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
