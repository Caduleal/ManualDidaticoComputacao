int pinoRele = 13;  // Fio amarelo conectado ao módulo relé
int pinoPir = A0;   // Fio verde conectado ao sinal do sensor PIR
int val = 0;        // Variável para armazenar a leitura do sensor

void setup() { 
  pinMode(pinoRele, OUTPUT);
  pinMode(pinoPir, INPUT);        
  Serial.begin(9600);                 
} 

void loop() { 
  val = digitalRead(pinoPir); // Lê o estado digital do sensor PIR
  
  if (val == HIGH) { 
    digitalWrite(pinoRele, HIGH); // Aciona o relé, ligando a lâmpada
    Serial.println("Movimento detectado - Lampada LIGADA");
    delay(100); 
  } else { 
    digitalWrite(pinoRele, LOW);  // Desaciona o relé, desligando a lâmpada
    delay(300);   
  } 
}