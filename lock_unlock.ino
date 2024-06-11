#include <Servo.h>

Servo myServo;
const int servoPin = 9;
const int redPin = 10;
const int greenPin = 11;
const int bluePin = 12;

String command;

void setup() {
  Serial.begin(9600);
  myServo.attach(servoPin);
  myServo.write(90); // Initial position, locked
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.readStringUntil('\n');
    command.trim();
    
    if (command == "unlock") {
      myServo.write(0); // Move to 0 degrees
      Serial.println("Unlocked");
    } 
    else if (command == "lock") {
      myServo.write(90); // Move back to 90 degrees
      Serial.println("Locked");
    }
    else if (command.startsWith("color")) {
      // Extract RGB values from the command
      int r, g, b;
      sscanf(command.c_str(), "color %d %d %d", &r, &g, &b);
      // Set the RGB LED color
      analogWrite(redPin, r);
      analogWrite(greenPin, g);
      analogWrite(bluePin, b);
      Serial.println("Color changed");
    }
    else if (command == "red") {
      // Extract RGB values from the command
      int r, g, b;
      r = 255;
      g = 0;
      b = 0;
      analogWrite(redPin, r);
      analogWrite(greenPin, g);
      analogWrite(bluePin, b);
      Serial.println("Color changed");
    }
    else if (command == "blue") {
      // Extract RGB values from the command
      int r, g, b;
      b = 255;
      r = 0;
      g = 0;
      analogWrite(redPin, r);
      analogWrite(greenPin, g);
      analogWrite(bluePin, b);
      Serial.println("Color changed");
    }
    else if (command == "green") {
      // Extract RGB values from the command
      int r, g, b;
      g = 255;
      r = 0;
      b = 0;
      analogWrite(redPin, r);
      analogWrite(greenPin, g);
      analogWrite(bluePin, b);
      Serial.println("Color changed");
    }
    else if (command == "led on") {
      // Turn on the RGB LED with white color
      analogWrite(redPin, 255);
      analogWrite(greenPin, 255);
      analogWrite(bluePin, 255);
      Serial.println("LED on");
    } 
    else if (command == "led off") {
      // Turn off the RGB LED
      analogWrite(redPin, 0);
      analogWrite(greenPin, 0);
      analogWrite(bluePin, 0);
      Serial.println("LED off");
    }
  }
}

