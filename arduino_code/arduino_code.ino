int green = 12;
int red = 13;
int blue = 11;
int yellow = 2;
String message; 

String msg;
byte parseStart = 0;

void setup() {
  Serial.begin(9600);
  pinMode(green, OUTPUT);
  pinMode(red, OUTPUT);
  pinMode(blue, OUTPUT);
  pinMode(yellow, OUTPUT);


}

void loop() {

  // Мониторим порт и запускам или останавливаем парсинг если видим нужный знак
  if (Serial.available()) {
    char s = Serial.read();
    if (s == '1') {
        digitalWrite(green, HIGH);
      }
      
    if (s == '2') {
        digitalWrite(red, HIGH);      
      } 
      
    if (s == '3') {
        digitalWrite(blue, HIGH);      
      }
    if (s == '4') {
        digitalWrite(yellow, HIGH);      
      }
      
    if (s == '0') {
       digitalWrite(green, LOW);
       digitalWrite(red, LOW);
       digitalWrite(blue, LOW);
       digitalWrite(yellow, LOW);      
      }  
   }
}
