
#include <xc.h> 



void setupLights() {
    TRISBbits.TRISB0 = 0; 
    TRISBbits.TRISB1 = 0;
}

void turnLightGreen() {
    PORTBbits.RB0 = 1;
//    PORTBbits.RB1 = 0;
}

void turnLightOrange() {
//    PORTBbits.RB1 = 1;
//    PORTBbits.RB0 = 1;
    PORTB = (1<<0) | (1<<1);
}

void turnLightRed() {
    PORTBbits.RB0 = 0;
    PORTBbits.RB1 = 1;
}

void turnLightOff() {
    PORTBbits.RB0 = 0;
    PORTBbits.RB1 = 0;
}