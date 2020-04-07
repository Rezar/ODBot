void moveMotors2(int lastSource) {
  if (lastSource >= 0) {
    //We're running motors
    //Serial.println(String(lastSource) + " is greater than 0 " );
    int dir = (int) lastSource; //1 = right, 0 = center, -1 = left;
    int motorMove = 0;

    int diff;

    if (lastSource <= 90) {
      diff = 90 + (int)lastSource;

    } else {
      diff = abs((int)lastSource - 268);
    }

    if (diff > 10) {

      if (dir > 270 || dir <= 90) {
        dir = 1; //RIGHT
      } else if (dir < 270 && dir >= 90) {
        dir = -1; ///LEFT
      }

      if (dir == 1) {
        turnL(diff * 2 + 50);
      } else if (dir == -1) {
        turnR(diff * 2 + 50);
      }
      delay(300);// + diff * 8);
    }
  }
}

void moveMotors(int lastSource) {
  if (lastSource >= 0) {
    //We're running motors
    //Serial.println(String(lastSource) + " is greater than 0 " );
    int dir = (int) lastSource; //1 = right, 0 = center, -1 = left;
    int motorMove = 0;

    int diff;
    //face towards 90
    if (lastSource <= 90){
      //left
      dir = -1;
      diff = 90 - lastSource;
    } else if (lastSource > 270) {
      //left
      dir = -1;
      diff = 90 + (360 - lastSource); 
    } else {
      //right
      dir = 1;
      diff = lastSource - 90;
    }
    /*
      Serial.print("diff: " );
      Serial.print(diff);
      Serial.print(" Dir: ");
      Serial.print(dir);
    */
    if (diff > 10) {
      if (dir == 1) {
        turnL(diff * 2.5 + 60);
//        Serial.println("Turn left by" + String(diff * 2.5 + 60));
      } else if (dir == -1) {
        turnR(diff * 2.5 + 60);
//        Serial.println("Turn right by" + String(diff * 2.5 + 60));
      }
      delay(300);// + diff * 8);
    }
  }
}
void turnL(int t) {
  //Do a tight turn towards motor1: Motor2 forward, Motor1 reverse
  motorDrive(motor1, turnCCW, 160);
  motorDrive(motor2, turnCW, 160);
  delay(t);
  motorBrake();
  //  motorsStandby();
  delay(80);
}

void turnR(int t) {
  //Do a tight turn towards motor1: Motor2 forward, Motor1 reverse
  motorDrive(motor1, turnCW, 160);
  motorDrive(motor2, turnCCW, 160);
  delay(t);
  motorBrake();
  //  motorsStandby();
  delay(80);
}
void motorDrive(boolean motor, boolean dir, int mSpeed) {

  boolean pinIn1;
  if (dir == turnCW) {
    pinIn1 = HIGH;
  } else {
    pinIn1 = LOW;
  }
  if (motor == motor1)  {
    digitalWrite(pinAIN1, pinIn1);
    digitalWrite(pinAIN2, !pinIn1);
  } else {
    digitalWrite(pinBIN1, pinIn1);
    digitalWrite(pinBIN2, !pinIn1);
  }
  analogWrite(pinPWMAB, mSpeed);

  //Finally , make sure STBY is disabled - pull it HIGH
  digitalWrite(pinSTBY, HIGH);

}

void continuousMotorDrive(boolean motor, boolean dir, int mSpeed) {

  boolean pinIn1;
  if (dir == turnCW) {
    pinIn1 = HIGH;
  } else {
    pinIn1 = LOW;
  }
  if (motor == motor1)  {
    digitalWrite(pinAIN1, pinIn1);
    digitalWrite(pinAIN2, !pinIn1);
  } else {
    digitalWrite(pinBIN1, pinIn1);
    digitalWrite(pinBIN2, !pinIn1);
  }

}

void motorContiuousForward(int mSpeed){
 //Do a tight turn towards motor1: Motor2 forward, Motor1 reverse
  motorDrive(motor1, turnCCW, 100);
  motorDrive(motor2, turnCCW, 100);
}

void motorForward(int mSpeed, int duration) {
  //Do a tight turn towards motor1: Motor2 forward, Motor1 reverse
  motorDrive(motor1, turnCW, 100);
  motorDrive(motor2, turnCW, 100);
  delay(duration);
  motorBrake();
  delay(80);
}

void motorBrake() {
  analogWrite(pinPWMAB, 0);
  motorsStandby();
}


void motorStop(boolean motor) {
  if (motor == motor1) {
    digitalWrite(pinAIN1, LOW);
    digitalWrite(pinAIN2, LOW);
    motorsStandby();
  } else {
    digitalWrite(pinBIN1, LOW);
    digitalWrite(pinBIN2, LOW);
    motorsStandby();
  }
}


void motorsStandby() {
  digitalWrite(pinSTBY, LOW);
}
