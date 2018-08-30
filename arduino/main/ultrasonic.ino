
int raw_distances[3][3] = {{0,0,0},{0,0,0},{0,0,0}}; //used to store previous 3 distances

long duration;
int distance;

int measureDistance(int trigPin, int echoPin) {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2;
  // Prints the distance on the Serial Monitor
  return distance;
}

int measureSmoothDistance(int dir){
  //found out what distance is
  int dist = -9999;
  if (dir == ULTRASONIC_LEFT){
    dist = measureDistance(leftUltraSonicTrigPin, leftUltraSonicEchoPin);
  } else if (dir = ULTRASONIC_RIGHT){
    dist = measureDistance(rightUltraSonicTrigPin, rightUltraSonicTrigPin);
  } else if (dir = ULTRASONIC_FRONT){
    dist = measureDistance(frontUltraSonicTrigPin, frontUltraSonicEchoPin);
  } else {
    Serial.print("Wrong dir measureSmoothDistance()");
  }
  //record distance
  raw_distances[dir][2] = raw_distances[dir][1];
  raw_distances[dir][1] = raw_distances[dir][0];
  raw_distances[dir][0] = dist;

  return ((raw_distances[dir][2] + raw_distances[dir][1] + raw_distances[dir][0])/3);
}

void readDistances() {
  Serial.print("Front: ");
  Serial.print(measureDistance(frontUltraSonicTrigPin, frontUltraSonicEchoPin));
  Serial.print(" Left: ");
  Serial.print(measureDistance(leftUltraSonicTrigPin, leftUltraSonicEchoPin));
  Serial.print(" Right: ");
  Serial.println(measureDistance(rightUltraSonicTrigPin, rightUltraSonicEchoPin));
  delay(10);
}


