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

/* Size of Transmission buffer */
#define RXBUFFERSIZE     								32

/* Size of Reception buffer */
#define TXBUFFERSIZE                    32

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */
uint8_t Get_First_Byte_of_Receive(void);

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
#define LEDGREEN_Pin GPIO_PIN_14
#define LEDGREEN_GPIO_Port GPIOB
#define LEDRED_Pin GPIO_PIN_15
#define LEDRED_GPIO_Port GPIOB

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

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
