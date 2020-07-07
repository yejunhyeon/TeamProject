int ledPin = 13;

void setup()
{
  pinMode(ledPin, OUTPUT);
  
  Serial.begin(9600); // print
}

void loop()
{
  digitalWrite(ledPin, LOW);
  delay(1000);
  
  Serial.println("hello");
  delay(1000);
}
