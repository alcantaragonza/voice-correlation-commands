//sketch para el reconocimiento

//pines que voy a utilizar
const int PIN_PULSADOR = 2;
const int PIN_RELE = 7;

//variables para detectar cuando se presiona
bool estadoAnterior = HIGH;

void setup() {
    // esta velocidad usare en pyserial
    Serial.begin(9600);

    //el pulsador  con pull-up  interno asi nos ahorramos la resistencia
    pinMode(PIN_PULSADOR, INPUT_PULLUP);

    // Rele para el apagado y el inicio
    pinMode(PIN_RELE, OUTPUT);
    digitalWrite(PIN_RELE, LOW);
}

void loop() {
    // reviso si presionaron el pulsador
    bool estadoActual = digitalRead(PIN_PULSADOR);

    //esto solo si nos interea al momento en que se presiona HIGH -> LOW
    if (estadoAnterior == HIGH && estadoActual == LOW) {
        Serial.println("P"); // para darle se;al a python para empezar a grabar
        delay(50); //peque;o delay para evitar rebote del boton
    }
    estadoAnterior = estadoActual;
    
    //reviso si python me esta mandando algun comando
    if (Serial.available() > 0) {
        char cmd = Serial.read();

        //si llega L enciende la lampara por 3 segundo
        if (cmd == 'L') {
            digitalWrite(PIN_RELE, HIGH);
            delay(3000);
            digitalWrite(PIN_RELE, LOW);
        }
        //si llega L enciende el motor por 1 segundo
        else if (cmd == 'M') {
            digitalWrite(PIN_RELE, LOW);
            delay(1000);
            digitalWrite(PIN_RELE, HIGH);
        }
    }
}