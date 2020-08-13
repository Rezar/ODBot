#include <Wire.h>                 // Must include Wire library for I2C
#include "SparkFun_MMA8452Q.h"    //http://librarymanager/All#SparkFun_MMA8452Q

MMA8452Q accel;                   // create instance of the MMA8452 class

int interval = 250;

int time;

float deltaV;
int v = -1;

void setup() {
  
  
  Serial.begin(9600);
  Serial.println("MMA8452Q Basic Reading Code!");
  Wire.begin();

  if (accel.begin() == false) {
    Serial.println("Not Connected. Please check connections and read the hookup guide.");
    while (1);
  }
}

void loop() {
  if (accel.available()) {      // Wait for new data from accelerometer
    // We need acceleration in Y direction in terms of g units
    time = millis();
    // Attempt to calculate velocity
    deltaV = accel.getCalculatedY() * (interval);
    if (v >= 0) {
      v = v + deltaV;
    } else {
      v = 0;
    }

    //Printing data
    delay(interval);
    Serial.print(accel.getCalculatedY(), 3);
    Serial.print('\t');
    Serial.print(time);
    Serial.print('\t');
    Serial.print(v);
    Serial.println();
    
    
  }
}
