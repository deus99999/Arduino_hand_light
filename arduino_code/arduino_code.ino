int green = 12;
int red = 10;
int blue = 13;
String message; 

String msg;
byte parseStart = 0;

void setup() {
  Serial.begin(9600);
  pinMode(green, OUTPUT);
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
      
    if (s == '0') {
       digitalWrite(red, LOW);
       digitalWrite(green, LOW);
      }
   }
    
//    if (parseStart == 1) {
//      message = msg.toInt();
//      //Serial.println(message);
//      parseStart = 0;
//      msg = "";
//      }
     
}
