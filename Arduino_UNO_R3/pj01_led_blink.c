int result = 0;
void setup() {
  // open the serial port:
  Serial.begin(9600);
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(2, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(2, HIGH);
  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  delay(5000);
  digitalWrite(2, LOW);
  digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
  delay(5000);
  if (Serial.available() > 0) {
    int brightness = Serial.parseInt();
    result += brightness;
    Serial.println(result);
  }
  
}