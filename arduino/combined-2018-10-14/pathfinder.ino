double desiredX, desiredZ, currentX, currentZ, currentDir, desiredDir;
boolean arrived = true;
int DISTANCE_THRESHOLD = 7;
boolean need_to_reset_dir = true;
double xMultiplier = 0, zMultiplier = 1; //multiplier for figuring out where the robot travelled 

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

void moveRobotIfNeeded() {
  Serial.println("moveRobotIfNeeded");
  if (arrived) return;
  
  if (distanceToDest() < 100){
    Serial.println("\tdistanceToDest < 100 arrived");
    //we're at destination
    motorBrake();
    currentZ = desiredZ;
    currentX = desiredX;
    arrived = true;
    return;
  }
  
  Serial.println("moveRobotIfNeeded - moving");
  int xPositive = measureSmoothDistance(ULTRASONIC_FRONT);
  int zNegative = measureSmoothDistance(ULTRASONIC_LEFT);
  int zPositive = measureSmoothDistance(ULTRASONIC_RIGHT);
  Serial.print("left: ");
  Serial.print(zNegative);
  Serial.print(" right: ");
  Serial.print(zPositive);
  Serial.print(" front: ");
  Serial.println(xPositive);
  
  Serial.println("need to reset dir " + String(need_to_reset_dir));
  if (need_to_reset_dir) {
    Serial.println("moveRobotIfNeeded - rotate");
    if (desiredDir != 0){
      double desiredDir = atan((desiredX - currentX) / abs(desiredZ - currentZ));
      desiredDir = (desiredZ - currentZ > 0 ? desiredDir : -desiredDir); //set sign
      desiredDir = radToDeg(desiredDir);
      /* Rotate the robot */
      /* Convert robot dir to VAD dir */
      desiredDir = (double) (((int) desiredDir + 90) % 360);
    }
    Serial.println("desiredDir " + String(desiredDir));
    if (currentDir != desiredDir) {
      /* Calculate direction and rotate */

      motorsStandby(); //IMPORTANT
    Serial.println("moveMotors " + String(desiredDir));
      moveMotors(desiredDir);
      xMultiplier = cos(desiredDir) * 100;
      zMultiplier = sin(desiredDir) * 100;
      Serial.println("xMultiplier " + String(xMultiplier));
      Serial.println("zMultiplier " + String(zMultiplier));
      currentDir = 0;
      desiredDir = 0;
      need_to_reset_dir = false;
    }
  } else if (xPositive > DISTANCE_THRESHOLD) {
    Serial.println("moveRobotIfNeeded - forward");
    /* Nothing in front of the robot */
    motorContiuousForward(100); //<- speed is currently fixed
    /* temp */
    currentZ -= desiredZ * zMultiplier;
    currentX -= desiredX * xMultiplier;
    /* end of temp */
  } else if (xPositive <= DISTANCE_THRESHOLD) {
    Serial.println("moveRobotIfNeeded - stop");
    motorBrake();
    need_to_reset_dir = true;
    if (zNegative > DISTANCE_THRESHOLD) {
      Serial.println("turning left");
      //left has space
      desiredDir = -90;
    } else if (zPositive > DISTANCE_THRESHOLD) {
      Serial.println("turning right");
      //right has space
      desiredDir = 90;
    } else {
      //this is when the robot's in a dead end and needs to turn 180 around and go somewhere else
      //lets deal with this later
      
    }
  }

  /*   */
}

double distanceToDest(){
  return sqrt(pow(desiredZ - currentZ, 2) + pow(desiredX - currentX, 2));
}

double radToDeg(double m) {
  return m * 180.0 / 3.14159;
}

/* this would make the robot move towards the goal until either g:0,0; is called or is at the goal.
                         (left)
                        negative
                            ^
               -135 degrees |          -45 degrees
                            |
              negative      |       positive
          (back)  <---------|------------> (front)   0 degrees
                            |          z
             135 degrees    |
                            |             45 degrees
                      x     v
                        positive
                         (right)
                           90 degrees

           For example, g:50,35; means go 50 to z (back and forth) and 35 to the x (left and right).
             In the robot's view, it would need to go forward 50 and right 35.
           Similarly,
           g:-30,0; means go backwards 35.
           g:20,-50; go forwards 20 and left 50.


           With current (2018-09-01) model,
           If there's an obstacle at 20~27cm away,
           it's could possibly get ignored when it gets closer because the front sensor only has a viewing degree of 15~20 degrees

*/
