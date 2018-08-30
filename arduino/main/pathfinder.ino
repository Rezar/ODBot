double desiredX, desiredZ, currentX, currentZ, currentDir;
boolean arrived = true;
void moveRobot(int z, int x) {
  Serial.println("got "  + String(z) + " , " + String(x));
  desiredX = (double) x;
  desiredZ = (double) z;
  currentX = 0;
  currentZ = 0;
  currentDir = 0;
  arrived = false;
}

//didn't think about when x is negative for now - 2018/08/29

void moveRobotIfNeeded(){
  if (arrived) return;
  if (desiredX == currentX && desiredZ == currentZ){
    arrived = true;
    return;
  }
  Serial.println("moveRobotIfNeeded");
  int xPositive = measureSmoothDistance(ULTRASONIC_FRONT);
  int zNegative = measureSmoothDistance(ULTRASONIC_LEFT);
  int zPositive = measureSmoothDistance(ULTRASONIC_RIGHT);
  
  /* Calculate direction and rotate */
  
    double desiredDir = atan((desiredX - currentX)/abs(desiredZ-currentZ));
    desiredDir = (desiredZ - currentZ > 0 ? desiredDir : -desiredDir); //set sign
    desiredDir = radToInt(desiredDir);
     Serial.println(desiredDir);
    /* Rotate the robot */
      /* Convert robot dir to VAD dir */
      desiredDir = (double) (((int) desiredDir + 90) % 360);
      
  if (currentDir != desiredDir){ //we need to fix this . temp. remove it possibly. just for testing direction turning
      motorsStandby(); //IMPORTANT
      Serial.println(desiredDir);
    moveMotors(desiredDir);
    currentDir = desiredDir;
  }
  /* Nothing in front of the robot */

  /*   */
}

double radToInt(double m){
  return m * 180.0 / 3.14159;
}

   /* this would make the robot move towards the goal until either g:0,0; is called or is at the goal.
           *                (left)
           *               negative
           *                   ^
           *      -135 degrees |          -45 degrees
           *                   |      
           *     negative      |       positive
           * (back)  <---------|------------> (front)   0 degrees
           *                   |          z
           *    135 degrees    |
           *                   |             45 degrees
           *             x     v
           *               positive
           *                (right)  
           *                  90 degrees
           * 
           *  For example, g:50,35; means go 50mm to z (back and forth) and 35mm to the x (left and right).
           *    In the robot's view, it would need to go forward 50mm and right 35mm.
           *  Similarly, 
           *  g:-30,0; means go backwards 35mm.  
           *  g:20,-50; go forwards 20mm and left 50mm.
           *  
           */
