void moveCamera(int hor, int vert) {
  //hor = 75 = 90degree
  //hor = 160 = -90degree
  if (vert > 95) vert = 95;
  if (hor > 160) hor = 160;
  if (vert < 0) vert = 0;
  if (hor < 0) hor = 0;
  horizontalServo.attach(3);
  verticalServo.attach(5);
  horizontalServo.write(hor);
  verticalServo.write(vert);
  delay(280);
  horizontalServo.detach();
  verticalServo.detach();
}

//movement test
void cameraTest(){
  while(true){
    moveCamera(random(-180, 720), random(-180, 720));
    delay(300);
  }
}

