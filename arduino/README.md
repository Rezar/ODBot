# ODBot Arduino

## Getting Started
ODBot uses Arduino to power its sensors and motors.

### Serial baud rate
This example uses a baud rate of 57600 to communicate between Raspberry Pi and Arduino. Check [the official Arduino document](https://www.arduino.cc/en/Serial/Begin) and [this article](https://arduino.stackexchange.com/questions/296/how-high-of-a-baud-rate-can-i-go-without-errors) if you wish to change it.
## Components
- [Arduino Uno R3](https://store.arduino.cc/usa/arduino-uno-rev3) - To use other board refer to [this](#using_other_arduino_boards]
- [Adafruit TB6612](https://www.adafruit.com/product/2448) - DC Motor Breakout board
- [HC-SR04](https://www.mouser.com/ds/2/813/HCSR04-1022824.pdf) - Ultrasonic sensors
- 5v DC Motors

## Pins
14 Total pins where
- 6 Digital Pins for 3 Ultrasonic Sensor ([HC-SR04](https://www.mouser.com/ds/2/813/HCSR04-1022824.pdf)) configuration.
- 6 Pins including PWM pins for Motor control
- 2 PWM Pins for Camera Motor Control

|Pin|Type|Use|Variable|Desc|
|--|--|--|--|--|
|0||||
|1||||
|2||||
|3|PWM|Servo|horizontalCam|Control Camera Servo
|4||||
|5|PWM|Servo|verticalCam|Control Camera Servo
|6|PWM|Servo|pinPWMAB|Control Motor Speed
|7||DC|pinSTBY|Control Motor STBY
|8||DC|motor2In2|Control Motor2
|9||DC|motor2In1|Control Motor2
|10||DC|motor1In2|Control Motor1
|11||DC|motor1In1|Control Motor1
|12||||
|13||||
|A0|||frontUltraSonicTrig|Front Ultrasonic Sensor Trig
|A1|||frontUltraSonicEcho|Front Ultrasonic Sensor Echo
|A2|||leftUltraSonicTrig|Left Ultrasonic Sensor Trig
|A3|||leftUltraSonicEcho|Left Ultrasonic Sensor Echo
|A4|||rightUltraSonicTrig|Right Ultrasonic Sensor Trig
|A5|||rightUltraSonicEcho|Right Ultrasonic Sensor Echo


Please refer to [this diagram of Arduino Uno Pinout](https://forum.arduino.cc/index.php?topic=146315.0) for more detail.

## Using other Arduino boards
In this project, Arduino Uno was used for the prototype version. Using other arduino compatible boards such as Teensy is also a valid choice as long as it has enough pins for all sensors and motors. Please refer to [this](#pins) for more detail.
