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

void readDistances() {
  Serial.print("Front: ");
  Serial.print(measureDistance(frontUltraSonicTrigPin, frontUltraSonicEchoPin));
  Serial.print(" Left: ");
  Serial.print(measureDistance(leftUltraSonicTrigPin, leftUltraSonicEchoPin));
  Serial.print(" Right: ");
  Serial.println(measureDistance(rightUltraSonicTrigPin, rightUltraSonicEchoPin));
  delay(100);
}

