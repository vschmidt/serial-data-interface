#define pinoEntrada A0

void setup() {
  pinMode(pinoEntrada, INPUT); //Configuração do pino de Entrada do sensor
  Serial.begin(9600);              //Inicialização da Interface Serial
}

void loop() {
  float quant_agua=0;
  bool sucesso=true;
  
  quant_agua = analogRead(pinoEntrada);
  enviaDado(quant_agua);
  
  delay(1000);
}

void enviaDado(float dado){
  Serial.println(dado);//Envio dos dados para o computador
}
