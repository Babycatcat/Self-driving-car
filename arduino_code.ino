#define Pin_Encoder_Right_A 2          //     E2A----------------2
#define Pin_Encoder_Right_B 3          //     E2B----------------3
#define Pin_Encoder_Left_A 20          //     E1A----------------20
#define Pin_Encoder_Left_B 21          //     E1B----------------21
//M1左輪   M2右輪

long theta_Right = 0, theta_Left = 0;
unsigned long currentMillis;
long previousMillis = 0;    // set up timers
float interval = 100;

//直流馬達----------TB6612腳位----------ArduinoUNO腳位
//                             PWMA-----------------4
//                             AIN1--------------------6
//                             AIN2--------------------5
//                             STBY-------------------7
//                             PWMB-----------------8
//                             BIN1-------------------10
//                             BIN2-------------------9
//
//                             GND-------------------GND
//                             VM--------------------12V
//                             VCC-------------------5V
//                             GND------------------GND
//直流馬達----------TB6612腳位----------ArduinoUNO腳位

#define PWMA 4
#define AIN1 6
#define AIN2 5
#define STBY 7
#define PWMB 8
#define BIN1 10
#define BIN2 9
#define trigPin 13
#define echoPin 12
int Duration;
int Distance;


int PwmA, PwmB;

void initMotor() {
  //控制訊號初始化
  pinMode(AIN1, OUTPUT);//控制馬達A的方向，(AIN1, AIN2)=(1, 0)為正轉，(AIN1, AIN2)=(0, 1)為反轉
  pinMode(AIN2, OUTPUT);
  pinMode(BIN1, OUTPUT);//控制馬達B的方向，(BIN1, BIN2)=(0, 1)為正轉，(BIN1, BIN2)=(1, 0)為反轉
  pinMode(BIN2, OUTPUT);
  pinMode(PWMA, OUTPUT);//A馬達PWM
  pinMode(PWMB, OUTPUT);//B馬達PWM
  pinMode(STBY, OUTPUT);//TB6612致能,設置0則所有馬達停止,設置1才允許控制馬達

  //初始化TB6612馬達驅動模組
  digitalWrite(AIN1, 1);
  digitalWrite(AIN2, 0);
  digitalWrite(BIN1, 1);
  digitalWrite(BIN2, 0);
  digitalWrite(STBY, 1);
  analogWrite(PWMA, 0);
  analogWrite(PWMB, 0);
  
  //ultra distance
  pinMode(trigPin,OUTPUT);
  pinMode(echoPin,INPUT);
  digitalWrite(trigPin,LOW);
}

void SetPWM(int motor, int pwm)
{
  //motor=1代表控制馬達A，pwm>=0則(AIN1, AIN2)=(1, 0)為正轉
  if (motor == 1 && pwm >= 0) {
    digitalWrite(AIN1, 1);
    digitalWrite(AIN2, 0);
    analogWrite(PWMA, pwm);

  }
  //motor=1代表控制馬達A，pwm<0則(AIN1, AIN2)=(0, 1)為反轉
  else if (motor == 1 && pwm < 0) {
    digitalWrite(AIN1, 0);
    digitalWrite(AIN2, 1);
    analogWrite(PWMA, -pwm);
  }
  //motor=2代表控制馬達B，pwm>=0則(BIN1, BIN2)=(0, 1)為正轉
  else if (motor == 2 && pwm >= 0) {
    digitalWrite(BIN1, 0);
    digitalWrite(BIN2, 1);
    analogWrite(PWMB, pwm);
  }
  //motor=2代表控制馬達B，pwm<0則(BIN1, BIN2)=(1, 0)為反轉
  else {
    digitalWrite(BIN1, 1);
    digitalWrite(BIN2, 0);
    analogWrite(PWMB, -pwm);
  }
}
//定義前進、後退、左轉、右轉、停止
//前進
void forward(int s1, int s2) {
  SetPWM(1, s1);
  SetPWM(2, -s2);

}
//右轉
void right(int s1, int s2) {
  SetPWM(1, s1);
  SetPWM(2, -s2);
}
//左轉
void left(int s1, int s2) {
  SetPWM(1, s1);
  SetPWM(2, -s2);

}
//後退
void back(int s1, int s2) {
  SetPWM(1, -s1);
  SetPWM(2, s2);

}
//停止
void stopp() {
  SetPWM(1, 0);
  SetPWM(2, 0);

}


void setup() {
  Serial.begin(57600);
  initMotor();
  previousMillis = millis();

}


void loop() {
 
  if(Serial.available()>0) {
    char c = Serial.read();
    if(c == '6') { //left triangle
      forward(15,35);
      Serial.print(c);
    }
    else if(c == '5') {
      forward(14,36);
      Serial.print(c);
    }
    else if(c == '4') {
      forward(17,33);
      Serial.print(c);
    }
    else if(c == '3') {
      forward(19,39);
      Serial.print(c);
    }
    else if(c == '2') {
      forward(21,39);
      Serial.print(c);
    }
    else if(c == '1') {
      forward(23,37);
      Serial.print(c);
    }
    else if(c == '0') { //直走
      forward(25,25);
      Serial.print(c);
    }
    else if(c == '-1') {
      forward(32,28);
      Serial.print(c);
    }
    else if(c == '-2') {
      forward(34,26);
      Serial.print(c);
    }
    else if(c == '-3') {
      forward(36,24);
      Serial.print(c);
    }
    else if(c == '-4') {
      forward(33,17);
      Serial.print(c);
    }
    else if(c == '-5') {
      forward(35,15);
      Serial.print(c);
    }
    else if(c == '-6') {//right triangle
      forward(35,16);
      Serial.print(c);
    }

   
    
  }
  
  
}
