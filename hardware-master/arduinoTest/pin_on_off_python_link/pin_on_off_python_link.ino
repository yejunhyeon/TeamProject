int ledPin = 13;

void setup()
{
  pinMode(ledPin, OUTPUT);
  
  Serial.begin(9600); // print
}

void loop()
{
  while (Serial.available() > 0){
    Serial.println("Serial On");
    delay(1000);
    
    char c = Serial.read();
    
    if(c=='1'){
      digitalWrite(13, HIGH);
      Serial.println("Pin On");
      delay(1000);
    } else if(c=='0'){
      digitalWrite(13, LOW);
      Serial.println("Pin Off");
      delay(1000);
    }
  }
  Serial.println("hello");
  delay(1000);
}
