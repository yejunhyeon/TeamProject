#include <Servo.h>
  
Servo servo1;
Servo servo2;

int a = 30;
int b = 90;
  
boolean UD = false;
boolean RL = true;

void setup() 
{
  servo1.attach(3);
  servo2.attach(5);
  Serial.begin(9600);
}
  
void loop()
{
  if ( a<30 ) UD = false;
  if ( a>80 ) UD = true;
  if ( b<10 ){
    RL = true;
    if ( UD ) a = a-5;
    else a = a+5;
  }
  if ( b>170 ){
    RL = false;
    if ( UD ) a = a-5;
    else a = a+5;
  }
  if ( RL ) b = b+2;
  else b = b-2;
  
  servo1.write(a);
  servo2.write(b);

  delay(100);  
  Serial.println('a = ', a);
  Serial.println('b = ', b);
}
  
