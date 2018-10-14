void avoidBump(){
int DISTANCE_THRESHOLD = 7; 
//  int distf = measureSmoothDistance(ULTRASONIC_FRONT);
//  int distl = measureSmoothDistance(ULTRASONIC_LEFT);
//  int distr = measureSmoothDistance(ULTRASONIC_RIGHT);
  int distf = measureDistance(frontUltraSonicTrigPin, frontUltraSonicEchoPin);
  delay(6);
  int distl = measureDistance(leftUltraSonicTrigPin, leftUltraSonicEchoPin);
  delay(6);
  int distr = measureDistance(rightUltraSonicTrigPin, rightUltraSonicEchoPin);
  delay(6);
  Serial.println(String(distf) + " " + String(distl) + " " + String(distr));
  if (distf < DISTANCE_THRESHOLD){
    if (distl > DISTANCE_THRESHOLD){
      //look at right to see if it's free
      moveMotors(0);
      isMotorOn = true;
      motorContiuousForward(100);
    } else if (distr > DISTANCE_THRESHOLD){
      //look at right to see if it's free
      moveMotors(180);
      isMotorOn = true;
      motorContiuousForward(100);
    } else {
      //back off
      motorContiuousBack(100);
      motorBrake();
    }
  }
}

