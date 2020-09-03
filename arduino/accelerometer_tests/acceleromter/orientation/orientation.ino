#include <Wire.h>                 // Must include Wire library for I2C
#include "SparkFun_MMA8452Q.h"    //http://librarymanager/All#SparkFun_MMA8452Q

MMA8452Q accel;                   // create instance of the MMA8452 class

int Y;
int period(100);
int noise;

void setup() {
  
  
  Serial.begin(9600);
  Serial.println("MMA8452Q Basic Reading Code!");
  Wire.begin();

  if (accel.begin() == false) {
    Serial.println("Not Connected. Please check connections and read the hookup guide.");
    while (1);
  }
  accel.init(); // Default init: +/-2g and 800Hz ODR
}

//int Y = accel.getCalculatedY();

void loop() {
  // put your main code here, to run repeatedly:
  if (accel.available()) {
    noise = abs(noise - Y);
    Serial.print(noise);
    Serial.print('\t');
    Y = accel.getCalculatedY();
    Serial.print(Y);
    Serial.println();
    delay(period);
  }
}
