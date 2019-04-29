/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
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

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "i2c.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "stm32f1xx_hal_i2c.h"
#include "stdio.h"
#include "string.h"
//#include "config.h"
#include "motor.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

/*____________________Main I2C Receive/Transmit Buffers____________________*/
uint8_t ReceiveBuf[RXBUFFERSIZE] = {NULL};
uint8_t TransmitBuf[TXBUFFERSIZE] = {NULL};

/*____________________Main Instruction Buffer____________________*/
uint8_t instructionArray[200][28];
int instArrNextFree = 0;

/*____________________Creation of Motors for Submachines____________________*/
#ifdef HANDLER
//struct Motor motor1 = {"Rail motor", "STEP", 1, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1};
//struct Motor motor2 = {"Spin motor", "STEP", 2, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1};
//struct Motor motor3 = {"Flip motor", "STEP", 3, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1};
struct SubMachine subMachine = {"Handler", 1,
      {{"Rail motor", "STEP", 1, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1},
      {"Spin motor", "STEP", 2, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1},
      {"Flip motor", "STEP", 3, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1}},
   };
#endif
#ifdef LATHE
//struct Motor motor1 = {"Pen motor", "STEP", 1, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1};
//struct Motor motor2 = {"Spin motor", "STEP", 2, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1};
//struct Motor motor3 = {"Vert motor", "STEP", 3, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1};
struct SubMachine subMachine = {"Lathe", 1,
      {{"Pen motor", "STEP", 1, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1},
      {"Spin motor", "STEP", 2, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1},
      {"Vert motor", "STEP", 3, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1}},
   };
#endif
#ifdef MILL
//struct Motor motor1 = {"Pen motor", "STEP", 1, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1};
//struct Motor motor2 = {"Spin motor", "DC", 2, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1};
//struct Motor motor3 = {"Vert motor", "STEP", 3, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1};
struct SubMachine subMachine = {"Mill", 1,
      {{"Pen motor", "STEP", 1, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1},
      {"Spin motor", "DC", 2, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1},
      {"Vert motor", "STEP", 3, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1}},
   };
#endif
#ifdef DRILL
//struct Motor motor1 = {"Pen motor", "STEP", 1, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1};
//struct Motor motor2 = {"Spin motor", "DC", 2, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1};
//struct Motor motor3 = {"Vert motor", "STEP", 3, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1};
struct SubMachine subMachine = {"Drill", 1,
      {{"Pen motor", "STEP", 1, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1},
      {"Spin motor", "DC", 2, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1},
      {"Vert motor", "STEP", 3, 0, 0, 1, 0, 0, 10, 0, /*Step Size*/ 1}},
   };
#endif

/*____________________Machine State Declaration____________________*/
// Volatile variable used for storing the machine's state
volatile uint8_t machineState;

/*____________________32 bit Sudo Timer MS Half____________________*/
// Volatile variable used for storing the MS Half of the sudo 32 bit Timer
volatile uint16_t timerMSHalf;

uint8_t newline[] = "\n";

uint8_t testvariable = 0;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_NVIC_Init(void);
void Flush_Buffer(uint8_t* pBuffer, uint16_t BufferLength);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
// Code to allow printf to be redirected to UART1
struct __FILE{
  int handle;
  /* Whatever you require here. If the only file you are using is */
  /* standard output using printf() for debugging, no file handling */
  /* is required. */
};

FILE __stdout;

int fputc(int ch, FILE *f){
	HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, 0xFFFF);
  return ch;
}

int ferror(FILE *f){
  /* Your implementation of ferror(). */
  return 0;
}
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_I2C1_Init();
  MX_USART1_UART_Init();
	#if defined MILL || defined DRILL
  MX_TIM4_Init();
	#endif
  MX_TIM1_Init();

  /* Initialize interrupts */
  MX_NVIC_Init();
  /* USER CODE BEGIN 2 */
	#if defined MILL || defined DRILL
  MX_TIM4_Init();
	#endif
	
	
	if(HAL_I2C_EnableListen_IT(&hi2c1) != HAL_OK)
  {
    /* Transfer error in reception process */
    Error_Handler();        
  }
	
	// Indicate start of program
	printf("Started Program\n");
	
	// Create an array of the motors
	struct Motor motors_array[3] = {*getMotorById(&subMachine, 1), *getMotorById(&subMachine, 2), *getMotorById(&subMachine, 3)};
	// Initialise the step size for the motors if they are step motors
	initMotorsStepSize(motors_array, sizeof(motors_array)/sizeof(*motors_array));
	
	// Set the machine to a ready state
	machineState = MACHINE_READY;

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
		//Test Stepper Motor Two
		//Enable Stepper
		// HAL_GPIO_WritePin(ST2EN_GPIO_Port,ST2EN_Pin, GPIO_PIN_SET);
		
		HAL_GPIO_WritePin(ST2EN_GPIO_Port,ST2EN_Pin, GPIO_PIN_RESET);
		// Set direction
		HAL_GPIO_WritePin(ST2DIR_GPIO_Port,ST2DIR_Pin, GPIO_PIN_SET);
		// for loop to run the stepper in this direction for 50 steps
		for(int a = 0; a < 525; a = a + 1 ){
      HAL_GPIO_WritePin(ST2STEP_GPIO_Port,ST2STEP_Pin,(GPIO_PinState)1);
			HAL_GPIO_WritePin(ST2STEP_GPIO_Port,ST2STEP_Pin,(GPIO_PinState)0);
			HAL_Delay(1);
		}
		HAL_GPIO_WritePin(ST2EN_GPIO_Port,ST2EN_Pin,(GPIO_PinState)1);
		HAL_Delay(200);
		
		HAL_GPIO_WritePin(ST2EN_GPIO_Port,ST2EN_Pin,(GPIO_PinState)0);
		HAL_GPIO_WritePin(ST2DIR_GPIO_Port,ST2DIR_Pin,(GPIO_PinState)0);
		for(int a = 0; a < 525; a = a + 1 ){
      HAL_GPIO_WritePin(ST2STEP_GPIO_Port,ST2STEP_Pin,(GPIO_PinState)1);
			HAL_GPIO_WritePin(ST2STEP_GPIO_Port,ST2STEP_Pin,(GPIO_PinState)0);
			HAL_Delay(1);
		}
		HAL_GPIO_WritePin(ST2EN_GPIO_Port,ST2EN_Pin,(GPIO_PinState)1);
		HAL_Delay(200);
		
		HAL_GPIO_WritePin(ST2EN_GPIO_Port,ST2EN_Pin, GPIO_PIN_SET);
		
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
		//HAL_Delay(2000);
		HAL_UART_Transmit(&huart1,(uint8_t *)instructionArray[instArrNextFree],28,HAL_MAX_DELAY);
	  HAL_UART_Transmit(&huart1,(uint8_t *)newline,sizeof(newline),HAL_MAX_DELAY);
		HAL_UART_Transmit(&huart1,(uint8_t *)instructionArray[instArrNextFree-1],28,HAL_MAX_DELAY);
	  HAL_UART_Transmit(&huart1,(uint8_t *)newline,sizeof(newline),HAL_MAX_DELAY);
		HAL_UART_Transmit(&huart1,(uint8_t *)ReceiveBuf,sizeof(ReceiveBuf),HAL_MAX_DELAY);
	  HAL_UART_Transmit(&huart1,(uint8_t *)newline,sizeof(newline),HAL_MAX_DELAY);
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI_DIV2;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL8;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_1) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief NVIC Configuration.
  * @retval None
  */
static void MX_NVIC_Init(void)
{
  /* I2C1_EV_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(I2C1_EV_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(I2C1_EV_IRQn);
  /* I2C1_ER_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(I2C1_ER_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(I2C1_ER_IRQn);
  /* TIM1_UP_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(TIM1_UP_IRQn, 1, 0);
  HAL_NVIC_EnableIRQ(TIM1_UP_IRQn);
  /* TIM1_CC_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(TIM1_CC_IRQn, 1, 1);
  HAL_NVIC_EnableIRQ(TIM1_CC_IRQn);
}

/* USER CODE BEGIN 4 */
/*____________________Static Functions____________________*/

/*____________________Global/Exported Functions____________________*/
/**
  * @brief  Flushes the buffer
  * @param  pBuffer: buffers to be flushed.
  * @param  BufferLength: buffer's length
  * @retval None
  */
void Flush_Buffer(uint8_t* pBuffer, uint16_t BufferLength) {
  while (BufferLength--)
  {
    *pBuffer = 0;

    pBuffer++;
  }
}

/**
  * @brief  Function to retrieve the I2C Receive Buffer 
  * @retval The pointer to the Receive Buffer
  */
uint8_t* Get_I2C_Receive_Buffer(void) {
	return ReceiveBuf;
}

/**
  * @brief  Function to retrieve the size of the I2C Receive Buffer 
  * @retval The pointer to the Receive Buffer
  */
int Get_I2C_Receive_Size(void) {
	//return sizeof(ReceiveBuf)/sizeof(*ReceiveBuf);
	return RXBUFFERSIZE;
}

/**
  * @brief  Function to set a value to the I2C Receive Buffer at a specific index
  * @param  The value to put in the index
	* @param  The index of the array
  */
void Set_I2C_Receive_Buffer_At_Index(uint8_t value, int index) {
	ReceiveBuf[index] = value;
}

/**
  * @brief  Function to retrieve the I2C Transmit Buffer 
  * @retval The pointer to the Transmit Buffer
  */
uint8_t* Get_I2C_Transmit_Buffer(void) {
	return TransmitBuf;
}

/**
  * @brief  Function to retrieve the size of the I2C Transmit Buffer 
  * @retval The pointer to the Receive Buffer
  */
int Get_I2C_Transmit_Size(void) {
	//return sizeof(TransmitBuf)/sizeof(*TransmitBuf);
	return TXBUFFERSIZE;
}

/**
  * @brief  Function to set a value to the I2C Transmit Buffer at a specific index
  * @param  The value to put in the index
	* @param  The index of the array
  */
void Set_I2C_Transmit_Buffer_At_Index(uint8_t value, int index) {
	TransmitBuf[index] = value;
}

/**
  * @brief  Function to retrieve the current state of the submachine 
  * @retval The value of machineState
  */
uint8_t Get_Machine_State(void) {
	return machineState;
}

/**
  * @brief  Function to set the current state of the submachine 
  * @param  The new value of machineState
  */
void Set_Machine_State(int newState) {
	machineState = newState;
}

/**
  * @brief  Function to retrieve the Instruction Array 
  * @retval The value of instructionArray
  */
uint8_t* Get_Instruction_Array(void) {
	return *instructionArray;
}

/**
  * @brief  Function to set a value in the Instruction Array at a specific index
  * @param  The value of the byte at the specific index
	* @param	The instruction index
	* @param	The byte index
  */
void Set_Instruction_Array_At_Index(uint8_t value, int intrIndex, int byteIndex) {
	instructionArray[intrIndex][byteIndex] = value;
}

/**
  * @brief  Function to retrieve the next free row of the Instruction Array 
  * @retval The value of instArrNextFree
  */
int Get_Inst_Array_Next_Free(void) {
	return instArrNextFree;
}

/**
  * @brief  Function to set the next free row of the Instruction Array 
  * @param  The new value of instArrNextFree
  */
void Set_Inst_Array_Next_Free(int newValue) {
	instArrNextFree = newValue;
}

/**
  * @brief  Function to retrieve the Motor struct instance (not pointer) based on the supplied motorNum 
  * @retval The value of instArrNextFree
  */
/*
struct Motor Get_Motor_Struct(int motorNum) {
	struct Motor tempMotor;
	switch(motorNum) {
		case 1:
			tempMotor = motor1;
			break; 
		case 2:
			tempMotor = motor2;
			break;
		case 3:
			tempMotor = motor3;
			break;
	}
	return tempMotor;
}
*/
/**
  * @brief  Function to retrieve the Motor struct pointer based on the supplied motorNum 
  * @retval The value of instArrNextFree
  */
	/*
struct Motor *Get_Motor_Pointer(int motorNum) {
	struct Motor *tempMotorPointer;
	switch(motorNum) {
		case 1:
			tempMotorPointer = &motor1;
			break; 
		case 2:
			tempMotorPointer = &motor2;
			break;
		case 3:
			tempMotorPointer = &motor3;
			break;
	}
	return tempMotorPointer;
}
*/
/**
  * @brief  Function to return the upper half of the sudo 32 bit timer 
	* @retval The value of the sudo 32bit timer MS Half
  */
uint16_t Get_Timer_Upper_Half(void) {
	return timerMSHalf;
}

/**
  * @brief  Function to increment the upper half of the sudo 32 bit timer
	* @retval None
  */
void Increment_Timer_Upper_Half(void) {
	if(timerMSHalf == 0xFFFF) {
		timerMSHalf = 0x0000;
	} else {
		timerMSHalf += 1;
	}
}
/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
	HAL_GPIO_TogglePin(PC13LED_GPIO_Port,PC13LED_Pin); 
  HAL_Delay(1000);
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{ 
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
