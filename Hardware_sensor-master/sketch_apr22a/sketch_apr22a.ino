int led = 0;
int state = 0;
void setup() {
    Serial.begin(9600);

    pinMode(8, OUTPUT);
    pinMode(7, INPUT);
    pinMode(9, OUTPUT);
}
 

void loop() {
int readValue = digitalRead(7);

if(readValue == HIGH) {
  state = 1 -state;
}
if(led <20){
  digitalWrite(8, HIGH);
  delay(250);
  digitalWrite(8, LOW);
  delay(250);
  tone(9 , 261, 2000);
  Serial.println(state);
  led++;

 if(state == 1 ) // 운전자 의식있음
    {
          digitalWrite(8, LOW);
          noTone(9);
    }
    
  else //운전자 의식없음 신고모드
  {
          digitalWrite(8, HIGH);
  }
  
}


  
 
}
