

int getFrequency(int pinNumber){
  //unsigned long pulseLength = pulseIn(pinNumber, LOW, 10000); //useconds to wait before returning zero
  //float wheelRPM = 1000000*60/(pulseLength*SensorFrequencyConstant);
  //return wheelRPM;
  return 500000/pulseIn(pinNumber, HIGH, 9200);
}

float getAverageFrequency(int pinNumber, int movAverageTable[]){
  int freq = getFrequency(pinNumber);
  //Serial.print(freq, 4);
  //Serial.print(',');
  freq = filterValidValues(freq, movAverageTable);
  return movingAverage(freq, movAverageTable);
}

float movingAverage(float freq, int movAverageTable[]){
  float sum = 0.0;
  for(int i=0;i<movAverageTableSize-1;i++){
    sum += movAverageTable[i];
    movAverageTable[i] = movAverageTable[i+1];
  }
  sum += movAverageTable[movAverageTableSize-1];
  movAverageTable[movAverageTableSize-1] = freq;
  float val = sum / movAverageTableSize;
  return val;
}

float getAverage(int movAverageTable[], int numberOfLastItems){
  if (numberOfLastItems > movAverageTableSize) return -1;
  float sum = 0.0;
  for(int i=numberOfLastItems-1;i<0;i--)sum += movAverageTable[i];
  return sum/numberOfLastItems;
}

void initialiseTable(int table[], int tableSize){
  for (int i=0; i<tableSize; i++){
    table[i] = 0;
  }
}

float filterValidValues(int currentValue, int movAverageTable[]){
  int compValue = getAverage(movAverageTable, 3);
  if (compValue < minFreqMesure){
    compValue = minFreqMesure;
  }
  int tolerance = toleranceDeltaMesure*compValue/100;
   if(currentValue <= maxFreqMesure
        && currentValue >= minFreqMesure){
    return currentValue;
  } else if (currentValue >= maxFreqMesure){
    return maxFreqMesure;
  } else if (currentValue <= minFreqMesure){
    return 0;
  } else{
    return compValue;
  }
}

void setNewCommand(double* command, int newCommand, int commandPin, double* outputVal, int directionPin){
  if(abs(newCommand) >= 0 && abs(newCommand) <= maxFreqMesure){
    *command = abs(newCommand);
  }
  if(newCommand > 0){
    digitalWrite(directionPin, LOW);
  } else {
    digitalWrite(directionPin, HIGH);
  }
  //Serial.print(newCommand);Serial.print(',');
  if(*command < minFreqMesure){
    *outputVal = 0;
    pinMode(commandPin, OUTPUT);
    digitalWrite(commandPin, LOW); 
  }
}














