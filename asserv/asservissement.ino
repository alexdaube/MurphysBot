#include <PID_v1.h>
#include <TimerOne.h>


//############ I/O definitions #################

#define capteurRoueA 13
#define capteurRoueB 12
#define capteurRoueC 8
#define capteurRoueD 7
#define CommandeRoueA 11 
#define CommandeRoueB 5
#define CommandeRoueC 3
#define CommandeRoueD 6
#define DirectionA 10
#define DirectionB 4
#define DirectionC 9
#define DirectionD 2

//############ GLOBAL VARIABLES #################
// variation maximale des capteurs au dela de laquelle la valeur est rejetée.
const int toleranceDeltaMesure = 100; // (en % de la dernière mesure)

// mesure de fréquence minimale considérée valide
const int minFreqMesure = 130;

// mesure de fréquence maximale considérée valide
const int maxFreqMesure = 2400;

// Nombre de pulsations émisent par le capteur de position par tour de roue.
const int SensorFrequencyConstant = 1600;

// Taille des tableaux servant à moyenner la valeur de vitesse des roues.
const int movAverageTableSize = 16;

// Bit de lecture du port serie
int incomingByte = 0, incomingCommand = 0;

// Tableaux de moyennage.
int movAverageRoueA[movAverageTableSize];
int movAverageRoueB[movAverageTableSize];
int movAverageRoueC[movAverageTableSize];
int movAverageRoueD[movAverageTableSize];

// PIDs Parameters:
double A_Kp=0.8, A_Ki=0, A_Kd=0;
double B_Kp=0.8, B_Ki=0, B_Kd=0;
double C_Kp=0.8, C_Ki=0, C_Kd=0;
double D_Kp=0.8, D_Ki=0, D_Kd=0;

double A_command, A_Input, A_Output;
double B_command, B_Input, B_Output;
double C_command, C_Input, C_Output;
double D_command, D_Input, D_Output;

PID PID_A(&A_Input, &A_Output, &A_command, A_Kp, A_Ki, A_Kd, DIRECT);
PID PID_B(&B_Input, &B_Output, &B_command, B_Kp, B_Ki, B_Kd, DIRECT);
PID PID_C(&C_Input, &C_Output, &C_command, C_Kp, C_Ki, C_Kd, DIRECT);
PID PID_D(&D_Input, &D_Output, &D_command, D_Kp, D_Ki, D_Kd, DIRECT);

//PID Timer interrupt settings:
int PIDComputeFrequency = 20; // Hz
int select = 0;

//############# SETUP #####################


void setup() {
  pinMode(capteurRoueA, INPUT);
  pinMode(capteurRoueB, INPUT);
  pinMode(capteurRoueC, INPUT);
  pinMode(capteurRoueD, INPUT);
  pinMode(DirectionA, OUTPUT);
  pinMode(DirectionB, OUTPUT);
  pinMode(DirectionC, OUTPUT);
  pinMode(DirectionD, OUTPUT);

  //populate the arrays with zeros.
  initialiseTable(movAverageRoueA, movAverageTableSize);
  initialiseTable(movAverageRoueB, movAverageTableSize);
  initialiseTable(movAverageRoueC, movAverageTableSize);
  initialiseTable(movAverageRoueD, movAverageTableSize);

  //PIDs setup
  A_Input = 0;
  B_Input = 0;
  C_Input = 0;
  D_Input = 0;
  A_command = 0; //  [5 RPM -> 90 RPM]
  B_command = 0;
  C_command = 0;
  D_command = 0;
  PID_A.SetMode(AUTOMATIC);
  PID_A.SetOutputLimits(0,maxFreqMesure);
  PID_B.SetMode(AUTOMATIC);
  PID_B.SetOutputLimits(0,maxFreqMesure);
  PID_C.SetMode(AUTOMATIC);
  PID_C.SetOutputLimits(0,maxFreqMesure);
  PID_D.SetMode(AUTOMATIC);
  PID_D.SetOutputLimits(0,maxFreqMesure);

  Timer1.initialize(1000000/PIDComputeFrequency);
  Timer1.attachInterrupt(PIDCompute);

  Serial.begin(9600);
  //Serial.println("setup completed");
}

//############# LOOP #####################

void loop() {
  if (Serial.available() > 0) {
    incomingCommand = Serial.read();
    if (incomingCommand == 64) { // char '@'
      incomingByte = Serial.parseInt();
      setNewCommand(&A_command, incomingByte, CommandeRoueA, &A_Output, DirectionA);
      incomingByte = Serial.parseInt();
      setNewCommand(&B_command, incomingByte, CommandeRoueB, &B_Output, DirectionB);
      incomingByte = Serial.parseInt();
      setNewCommand(&C_command, incomingByte, CommandeRoueC, &C_Output, DirectionC);
      incomingByte = Serial.parseInt();
      setNewCommand(&D_command, incomingByte, CommandeRoueD, &D_Output, DirectionD);
    }
  }
  if(A_command > 0){
    A_Input = getAverageFrequency(capteurRoueA, movAverageRoueA);
    analogWrite(CommandeRoueA,A_Output*255/maxFreqMesure);
  }
  if(B_command > 0){
    B_Input = getAverageFrequency(capteurRoueB, movAverageRoueB);
    analogWrite(CommandeRoueB,B_Output*255/maxFreqMesure);
  }
  if(C_command > 0){
    C_Input = getAverageFrequency(capteurRoueC, movAverageRoueC);
    analogWrite(CommandeRoueC,C_Output*255/maxFreqMesure);
  }
  if(B_command > 0){
    D_Input = getAverageFrequency(capteurRoueD, movAverageRoueD);
    analogWrite(CommandeRoueD,D_Output*255/maxFreqMesure);
  }
}

void PIDCompute(){
  if(A_command > 0){
    PID_A.Compute();
  }
  if(B_command > 0){
    PID_B.Compute();
  }
  if(C_command > 0){
    PID_C.Compute();
  }
  if(B_command > 0){
    PID_D.Compute();
  }
}

