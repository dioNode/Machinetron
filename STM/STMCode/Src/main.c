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

// Definitions used to define what submachine is currently loaded
#define HANDLER
//#define LATHE
//#define MILL
//#define DRILL

/* I2C Definitions */
#define I2C_ADDRESS        	0x1F
#define I2C_CLOCKSPEED   		400000
#define I2C_DUTYCYCLE    		I2C_DUTYCYCLE_2

/* UART Definitions */
#define UART_BAUDRATE				921000

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
I2C_HandleTypeDef hi2c1;

#if defined MILL || defined DRILL
TIM_HandleTypeDef htim4;
#endif

UART_HandleTypeDef huart1;

/* USER CODE BEGIN PV */
// Receive and Transmit Data Buffer declarations
uint8_t ReceiveBuf[RXBUFFERSIZE] = {NULL};
uint8_t TransmitBuf[] = "Test Data How is the weather? 12";

uint8_t newline[] = "\n";

uint8_t testvariable = 0;

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_I2C1_Init(void);
static void MX_USART1_UART_Init(void);
#if defined MILL || defined DRILL
static void MX_TIM4_Init(void);
#endif
static void MX_NVIC_Init(void);
/* USER CODE BEGIN PFP */
static void Flush_Buffer(uint8_t* pBuffer, uint16_t BufferLength);
static void Error_Handler(void);
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
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
	
  /* Initialize interrupts */
  MX_NVIC_Init();
  /* USER CODE BEGIN 2 */
	if(HAL_I2C_EnableListen_IT(&hi2c1) != HAL_OK)
  {
    /* Transfer error in reception process */
    Error_Handler();        
  }
	
	
	// Indicate start of program
	printf("Started Program\n");
	
	// Creation of motor structure for each submachine
	#ifdef HANDLER
	struct Motor railMotor = {"Rail motor", "STEP", 1, 0, 0, 1, 0, 10, 0, 1};
	struct Motor flipMotor = {"Flip motor", "STEP", 2, 0, 0, 1, 0, 10, 0, 1};
	struct Motor spinMotor = {"Spin motor", "STEP", 3, 0, 0, 1, 0, 10, 0, 1};
	
	// Create an array of the motors
	struct Motor motors_array[3] = {railMotor, flipMotor, spinMotor};
	// Initialise the step size for the motors if they are step motors
	initMotorsStepSize(motors_array, sizeof(motors_array)/sizeof(*motors_array));
	#endif
	
	#ifdef LATHE
	struct Motor vertMotor = {"Vert motor", "STEP", 1, 0, 0, 1, 0, 10, 0, 1};
	//struct Motor spinMotor = {"Spin motor", "STEP", 2, 0, 0, 1, 0, 10, 0, 1};
	struct Motor penMotor = {"Pen motor", "STEP", 3, 0, 0, 1, 0, 10, 0, 1};
	
	// Create an array of the motors
	struct Motor motors_array[2] = {vertMotor, penMotor};
	// Initialise the step size for the motors if they are step motors
	initMotorsStepSize(motors_array, sizeof(motors_array)/sizeof(*motors_array));
	#endif
	
	#ifdef MILL
	struct Motor vertMotor = {"Vert motor", "STEP", 1, 0, 0, 1, 0, 10, 0, 1};
	struct Motor spinMotor = {"Spin motor", "DC", 2, 0, 0, 1, 0, 10, 0, 1};
	struct Motor penMotor = {"Pen motor", "STEP", 3, 0, 0, 1, 0, 10, 0, 1};
	
	// Create an array of the motors
	struct Motor motors_array[3] = {vertMotor, spinMotor, penMotor};
	// Initialise the step size for the motors if they are step motors
	initMotorsStepSize(motors_array, sizeof(motors_array)/sizeof(*motors_array));
	#endif
	
	#ifdef DRILL
	struct Motor vertMotor = {"Vert motor", "STEP", 1, 0, 0, 1, 0, 10, 0, 1};
	struct Motor spinMotor = {"Spin motor", "DC", 2, 0, 0, 1, 0, 10, 0, 1};
	struct Motor penMotor = {"Pen motor", "STEP", 3, 0, 0, 1, 0, 10, 0, 1};
	
	// Create an array of the motors
	struct Motor motors_array[3] = {vertMotor, spinMotor, penMotor};
	// Initialise the step size for the motors if they are step motors
	initMotorsStepSize(motors_array, sizeof(motors_array)/sizeof(*motors_array));
	#endif
	
	//Initialise motors
	
	
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
		
		//Test Stepper Motor Two
		//Enable Stepper
		
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
}

/**
  * @brief I2C1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_I2C1_Init(void)
{

  /* USER CODE BEGIN I2C1_Init 0 */

  /* USER CODE END I2C1_Init 0 */

  /* USER CODE BEGIN I2C1_Init 1 */

  /* USER CODE END I2C1_Init 1 */
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
  /* USER CODE BEGIN I2C1_Init 2 */

  /* USER CODE END I2C1_Init 2 */

}

#if defined MILL || defined DRILL
/**
  * @brief TIM4 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM4_Init(void)
{

  /* USER CODE BEGIN TIM4_Init 0 */

  /* USER CODE END TIM4_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};

  /* USER CODE BEGIN TIM4_Init 1 */

  /* USER CODE END TIM4_Init 1 */
  htim4.Instance = TIM4;
  htim4.Init.Prescaler = 0;
  htim4.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim4.Init.Period = 65535;
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
  /* USER CODE BEGIN TIM4_Init 2 */

  /* USER CODE END TIM4_Init 2 */
  HAL_TIM_MspPostInit(&htim4);

}
#endif

/**
  * @brief USART1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART1_UART_Init(void)
{

  /* USER CODE BEGIN USART1_Init 0 */

  /* USER CODE END USART1_Init 0 */

  /* USER CODE BEGIN USART1_Init 1 */

  /* USER CODE END USART1_Init 1 */
  huart1.Instance 						= USART1;
  huart1.Init.BaudRate 				= UART_BAUDRATE;
  huart1.Init.WordLength 			= UART_WORDLENGTH_8B;
  huart1.Init.StopBits 				= UART_STOPBITS_1;
  huart1.Init.Parity 					= UART_PARITY_NONE;
  huart1.Init.Mode 						= UART_MODE_TX_RX;
  huart1.Init.HwFlowCtl 			= UART_HWCONTROL_NONE;
  huart1.Init.OverSampling 		= UART_OVERSAMPLING_16;
  
	if (HAL_UART_Init(&huart1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART1_Init 2 */

  /* USER CODE END USART1_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
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

	#if defined HANDLER || defined LATHE
	/*Configure GPIO pin Output Level */
	// Used to initialise the enable pin for Motor 2 as a stepper motor
  HAL_GPIO_WritePin(GPIOB, ST2EN_Pin, GPIO_PIN_RESET);
  #endif
	
	/*Configure GPIO pin : PC13LED_Pin */
  GPIO_InitStruct.Pin = PC13LED_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(PC13LED_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : ST1DIR_Pin ST1STEP_Pin ST3DIR_Pin ST3STEP_Pin 
                           ST2DIR_Pin */
													 
  GPIO_InitStruct.Pin = ST1DIR_Pin|ST1STEP_Pin|ST3DIR_Pin|ST3STEP_Pin 
                          |ST2DIR_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pins : ST1MS3_Pin ST1MS2_Pin ST1MS1_Pin */
	
  GPIO_InitStruct.Pin = ST1MS3_Pin|ST1MS2_Pin|ST1MS1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pin : ST1EN_Pin */
	
  GPIO_InitStruct.Pin = ST1EN_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(ST1EN_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : ST3MS3_Pin ST3MS2_Pin ST3MS1_Pin LEDGREEN_Pin 
                           LEDRED_Pin ST2MS3_Pin ST2MS2_Pin ST2MS1_Pin */
													 
  GPIO_InitStruct.Pin = ST3MS3_Pin|ST3MS2_Pin|ST3MS1_Pin|LEDGREEN_Pin 
                          |LEDRED_Pin|ST2MS3_Pin|ST2MS2_Pin|ST2MS1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pin : ST3EN_Pin */
	
  GPIO_InitStruct.Pin = ST3EN_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(ST3EN_GPIO_Port, &GPIO_InitStruct);
	
	#if defined HANDLER || defined LATHE
	/*Configure GPIO pin : ST2EN_Pin */
	
  GPIO_InitStruct.Pin = ST2EN_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(ST3EN_GPIO_Port, &GPIO_InitStruct);
	#endif
	
  /*Configure GPIO pins : LIMSW1_Pin LIMSW4_Pin LIMSW5_Pin */
	
  GPIO_InitStruct.Pin = LIMSW1_Pin|LIMSW4_Pin|LIMSW5_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pin : ST2STEP_Pin */
	
  GPIO_InitStruct.Pin = ST2STEP_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(ST2STEP_GPIO_Port, &GPIO_InitStruct);

}

/* USER CODE BEGIN 4 */
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
		if(HAL_I2C_Slave_Sequential_Transmit_IT(hi2c, (uint8_t *)TransmitBuf, RXBUFFERSIZE,I2C_LAST_FRAME) != HAL_OK) {
			// Transfer error in reception process
			Error_Handler();
		}
		
	} 
	else {
		//printf("TransferDirectionTransmit\n");
		if(HAL_I2C_Slave_Sequential_Receive_IT(hi2c, (uint8_t *)ReceiveBuf, TXBUFFERSIZE,I2C_FIRST_FRAME) != HAL_OK) {
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
	
	// Turn off the PC13 LED
	HAL_GPIO_WritePin(PC13LED_GPIO_Port,PC13LED_Pin,GPIO_PIN_RESET);
	//printf("ListenCpltCallback\n");
	//printf("Really long piece of text to test a theory on interrupts being interrupted_
	//HAL_UART_Transmit(&UartDebugHandle,(uint8_t *)hi2c->pBuffPtr,sizeof(hi2c->pBuffPtr),HAL_MAX_DELAY);
	HAL_UART_Transmit(&huart1,(uint8_t *)ReceiveBuf,sizeof(ReceiveBuf),HAL_MAX_DELAY);
	HAL_UART_Transmit(&huart1,(uint8_t *)newline,sizeof(newline),HAL_MAX_DELAY);
	Flush_Buffer(ReceiveBuf,sizeof(ReceiveBuf));
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
void HAL_I2C_SlaveRxCpltCallback(I2C_HandleTypeDef *I2cHandle)
{
  // Turn on PC13 LED
	HAL_GPIO_WritePin(PC13LED_GPIO_Port,PC13LED_Pin,GPIO_PIN_SET);
	//printf("SlaveRxCpltCallback\n");
}

/**
  * @brief  Flushes the buffer
  * @param  pBuffer: buffers to be flushed.
  * @param  BufferLength: buffer's length
  * @retval None
  */
static void Flush_Buffer(uint8_t* pBuffer, uint16_t BufferLength)
{
  while (BufferLength--)
  {
    *pBuffer = 0;

    pBuffer++;
  }
}

uint8_t Get_First_Byte_of_Receive(void) {
	return ReceiveBuf[0];
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
  /* Error if INBUILT LED is slowly blinking (1 sec. period) */
  while(1)
  {    
    HAL_GPIO_TogglePin(PC13LED_GPIO_Port,PC13LED_Pin); 
    HAL_Delay(1000);
  } 
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
