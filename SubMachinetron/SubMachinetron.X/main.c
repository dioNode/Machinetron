#define FOSC 8000000L
#define FCY (FOSC/2)
#define BAUD_RATE_UART1 9600L

#pragma config ICS = PGD2

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libpic30.h>
#include <xc.h> 
#include <string.h>
#include "statuslights.h"

extern int i2c_rcv, i2c_trn;

void setupI2C()
{
   IEC1bits.SI2C1IE = 1; // enable SI2C1IF interrupt 
   I2C1CONbits.I2CEN = 1; // enable I2C
   I2C1CONbits.A10M = 0; // 7 bit address
   I2C1ADD = 15; // slave address

}

//void i2cSlaveEventHandler()
//{
//    int rcv_buffer;
//    
//    IFS1bits.SI2C1IF = 0; // reset interrupt
//    
//    if (I2C1STATbits.RBF == 1)
//        rcv_buffer = I2C1RCV; // RCV buffer cleared
//    
//    if (I2C1STATbits.ACKSTAT == 1) // NACK received
//        return;
//    
//    
//    if (I2C1STATbits.R_W == 0) // write operation
//
//        if (I2C1STATbits.D_A == 1) // valid data
//            i2c_rcv = rcv_buffer;
//    
//    if (I2C1STATbits.R_W ==1) // read operation
//    {
//        I2C1TRN = i2c_trn; // transmit data
////        I2C1CONbits.SCLREL = 1; ///< release clock
//        
//        //while ( I2C1STATbits.TBF == 1);
//        i2c_trn ++;
//        
//    } 
//          
//}


int main(int argc, char** argv)
{
    setupI2C();
    setupLights();
    
//    U1MODEbits.UARTEN = 1;
//    U1STAbits.UTXEN = 1;
//    
//    I2C1CONbits.I2CEN = 1;
    
    
    
    while (1) {
        turnLightGreen();
        __delay_ms(500);
        turnLightOrange();
        __delay_ms(500);
        turnLightRed();
        __delay_ms(500);
        turnLightOff();
        __delay_ms(500);
    }
    
    return 0;
    
}

