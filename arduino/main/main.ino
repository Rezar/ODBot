#include <Servo.h>
#include <math.h>
#include <NewPing.h>
/* DC Motor Pins */
/* Motor 1 */
const int pinAIN1 = 11; //Direction
const int pinAIN2 = 12; //Direction

/* Motor 2 */
const int pinBIN1 = 7; //Direction
const int pinBIN2 = 8; //Direction

/* Shared */
const int pinPWMAB = 10; //PWM Speed
const int pinSTBY = 9; //Pin for StandBy Mode

/* DC Motor Config */
static boolean turnCW = 0;  //for motorDrive function
static boolean turnCCW = 1; //for motorDrive function
static boolean motor1 = 0;  //for motorDrive, motorStop, motorBrake functions
static boolean motor2 = 1;  //for motorDrive, motorStop, motorBrake functions


/* Servo Pins */
static Servo horizontalServo;
static Servo verticalServo;
const int horizontalCamPin = A9; //PWM
const int verticalCamPin = A8; //PWM

/* Ultrasonic Sensor Pins */
const int frontUltraSonicTrigPin = A0;
const int frontUltraSonicEchoPin = A1;
const int leftUltraSonicTrigPin = A2;
const int leftUltraSonicEchoPin = A3;
const int rightUltraSonicTrigPin = A4;
const int rightUltraSonicEchoPin = A5;

/* Ultrasonic Vars for path finding */
#define ULTRASONIC_LEFT 0
#define ULTRASONIC_RIGHT 1
#define ULTRASONIC_FRONT 2

/* Main */
int idleLoopCount = 0; //Used to count idle cycle

void setup() {
  /* DC Motor Pins */
  pinMode(pinPWMAB, OUTPUT); //PWM pin used to control speed
  pinMode(pinAIN1, OUTPUT); //
  pinMode(pinAIN2, OUTPUT);
  pinMode(pinBIN1, OUTPUT);
  pinMode(pinBIN2, OUTPUT);
  pinMode(pinSTBY, OUTPUT);
  /* End of DC Motor Pins */

  /* Servo Attach */
  horizontalServo.attach(horizontalCamPin);
  verticalServo.attach(verticalCamPin);
  horizontalServo.detach();
  verticalServo.detach();
  /* End of Servo Attach */

  /* Ultrasonic Sensor Pins */
  pinMode(frontUltraSonicTrigPin, OUTPUT);
  pinMode(frontUltraSonicEchoPin, INPUT);
  pinMode(leftUltraSonicTrigPin, OUTPUT);
  pinMode(leftUltraSonicEchoPin, INPUT);
  pinMode(rightUltraSonicTrigPin, OUTPUT);
  pinMode(rightUltraSonicEchoPin, INPUT);
  /* End of Ultrasonic Sensor Pins */
  pinMode(13, OUTPUT);
  /* Serial Preparation */
  Serial.begin(57600);
  Serial.setTimeout(100);
  while (!Serial); //Wait for Serial
  /* End of Serial Preparation */
  delay(50);
  Serial.println("e:ready;"); //Notify RPI that Arduino is ready
}



void loop() { // run over and over
  digitalWrite(13, HIGH);
//  cameraTest();

  //Three lines below output the front sensor distance to Serial
  //long dist = howFar(frontUltraSonicTrigPin,frontUltraSonicEchoPin);
  //Serial.println(dist);
  //delay(100);

//  moveRobotIfNeeded();
  if (Serial.available()) {

    
    digitalWrite(13, LOW);
    idleLoopCount = 0;
    String raw = Serial.readString(); //Read from Serial

    //Check for syntax
    while (raw.indexOf(";") > 0) {
      String serialMsg = raw.substring(0, raw.indexOf(";") + 1); //fetch oldest message first
     
      if (raw.indexOf(";") + 1 < raw.length()) {
        raw = raw.substring(raw.indexOf(";") + 1, raw.length() + 1);
      } else {
        raw = "";
      }

   
      if (serialMsg.length() <= 3) { //although very simple and clumsy, all commands are right now more than 3 letters long
        Serial.println("BadString: " + serialMsg);
        return; //ignore bad string
      }
      
      char type = serialMsg[0]; //type of command
      String msg = serialMsg.substring(2, serialMsg.length() - 1); //command content
      
      float lastSource = -1; //if robot rotate command
      String horizontalVal, verticalVal; //if camera servo (c) command
      int commaIndex;

      int rawx, rawz; //used for g:[z,x]
      /*
       *  Types
       *   d:[f|s]: blindly move forward or stop
       *   g:[z,x]: move towards a relative goal. Units in mm
       *   m:[r]: rotate robot towards a degree
       *   c:[x,y]: move camera mount servo motors
       *   e:[s]: debug
       */ 
      switch (type) {
        default:
          Serial.println("BadString: " + serialMsg);
          break;
        case 'd': //where ODBOT drives forward, then stops in front of an obstacle
          Serial.println(msg);
          if (msg.equals("f")){
            motorContiuousForward(160);

            while (true) {
              int dist = howFar(frontUltraSonicTrigPin,frontUltraSonicEchoPin);
              delay(50);
              Serial.println(dist);
              if (dist < 20) {
                motorBrake();
                break;
                
              }
            }
            
              
            // Code here will stop ODBOT from hitting an obstacle
            
            // avoided?
          } else if (msg.equals("s")){
            motorBrake();
          }
          break;
        case 'g':
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
          commaIndex = lastIndexOf(msg, ',');
          rawz = msg.substring(0, commaIndex).toInt();
          rawx = msg.substring(commaIndex + 1,  msg.length()).toInt();
          moveRobot(rawz,rawx);
          break;
          
        case 'm':
          //case where command is to rotate robot to focus at a certain degree
          //ex: m:270 === move to 270 degree
          //ex: m:13 === move to 13 degree
          
          //Serial.println("r:m " + String(msg.toFloat()) + ";");
          lastSource = msg.toFloat();
          motorsStandby(); //IMPORTANT
          moveMotors(lastSource);
          break;
        case 'c':
          //case where command is to rotate servo motors for camera
          //ex: c:120,90 === move camera to horizontal 120 degree and vertical 90 degree
          //any values beyond the capability of servo motors (0 ~ 180 degrees that is) will be overridden in moveCamera() function
          commaIndex = lastIndexOf(msg, ',');
          horizontalVal = msg.substring(0, commaIndex);
          verticalVal = msg.substring(commaIndex + 1,  msg.length());
          moveRobot(horizontalVal.toInt(), verticalVal.toInt());
          break;
        case 'e':
          //          Serial.println("r:e " + msg + ";");
          //echo?
          break;
        case 't':
          for (int i = 0; i <100; i++){
            readDistances();
            delay(300);
          }
          break;
      } //end of case
    } //end of command loop

    Serial.println("m:done;"); //send RPI that arduino is done with commands
  } else {
    //No serial available
    //sometimes serial messages can get ignored. Because of this reason, RPI can think that Arduino is busy when it's not.
    //this function constantly reminds RPI that it's available
    if (idleLoopCount > 100) {
      Serial.println("e:ready;");
      idleLoopCount = 0;
    } else {
      idleLoopCount++;
    }
    delay(100);
  }
  
}

int lastIndexOf(String s, char c) {
  int out = -1;
  for (int i = 0; i < s.length(); i++) {
    if (s[i] == c) {
      out = i;
    }
  }
  return out;
}
