
const int LEFT_ENABLE_PIN = 8; // EN
const int LEFT_STEP_PIN = 9; // STEP
const int LEFT_DIRECTION_PIN = 7; // DIR

const int RIGHT_ENABLE_PIN = 6; // EN
const int RIGHT_STEP_PIN = 5; // STEP
const int RIGHT_DIRECTION_PIN = 4; // DIR


String commandBuffer;

void setup() {
  Serial.begin(9600);

  pinMode(LEFT_ENABLE_PIN, OUTPUT); 
  pinMode(LEFT_STEP_PIN, OUTPUT); 
  pinMode(LEFT_DIRECTION_PIN, OUTPUT);
  
  pinMode(RIGHT_ENABLE_PIN, OUTPUT); 
  pinMode(RIGHT_STEP_PIN, OUTPUT); 
  pinMode(RIGHT_DIRECTION_PIN, OUTPUT);

  digitalWrite(LEFT_ENABLE_PIN, LOW);
  delayMicroseconds(300);
  digitalWrite(RIGHT_ENABLE_PIN, LOW);
  delayMicroseconds(300);
}

void loop() {
  if (Serial.available() > 0) {
    commandBuffer = Serial.readString();

    if (commandBuffer.charAt(0) == 'M'){
      char targetMotor = commandBuffer.charAt(1);
      char motorDirection = commandBuffer.charAt(2);
      char steps_char = commandBuffer.charAt(3);
      int steps = steps_char - 48;
  
      int motorPin = -1;
      int directionPin = -1;

      int UP = HIGH;
      int DOWN = LOW;
  
      if (targetMotor == 'R') {
        motorPin = RIGHT_STEP_PIN;
        directionPin = RIGHT_DIRECTION_PIN;
      } else if (targetMotor == 'L') {
        motorPin = LEFT_STEP_PIN;
        directionPin = LEFT_DIRECTION_PIN;
        UP = LOW;
        DOWN = HIGH;
      }
  
      if (motorPin > -1){
        if (motorDirection == '+') {
          digitalWrite(directionPin, UP); 
        } else {
          digitalWrite(directionPin, DOWN); 
        }
        for (int i=0; i< 5 * steps; i++){
          digitalWrite(motorPin, HIGH); 
          delayMicroseconds(300); 
          digitalWrite(motorPin, LOW); 
          delayMicroseconds(10000);
        }
      }
    }
    else if (commandBuffer.charAt(0) == 'S') {
        digitalWrite(LEFT_ENABLE_PIN, LOW);
        delayMicroseconds(300);
        digitalWrite(RIGHT_ENABLE_PIN, LOW);
        delayMicroseconds(300);
    }
    Serial.print(commandBuffer);
    Serial.flush();
  }
}
