#include <ros.h>
#include <std_msgs/Bool.h>
#include <std_srvs/Trigger.h>

const int button_pin_left = 2;
const int button_pin_middle = 4;
const int button_pin_right = 7;

unsigned long previousMillis = 0;
const unsigned long interval = 500; 

ros::NodeHandle  nh;

std_msgs::Bool button_left_pressed; 
std_msgs::Bool button_middle_pressed; 
std_msgs::Bool button_right_pressed;
 
void connectionCallback(const std_srvs::Trigger::Request &req, std_srvs::Trigger::Response &res)
{
  res.success = true;
  res.message = "Service triggered successfully";
}

void penCallback(const std_msgs::Bool& msg)
{
  if (msg.data)
  {
    digitalWrite(13, HIGH);
  }
  else
  {
    digitalWrite(13, LOW);
  }
}

ros::Publisher pub1("botton_left", &button_left_pressed);
ros::Publisher pub2("botton_middle", &button_middle_pressed);
ros::Publisher pub3("botton_right", &button_right_pressed);

ros::Subscriber<std_msgs::Bool> sub1("pen_mode", &penCallback); // led control  

ros::ServiceServer<std_srvs::Trigger::Request, std_srvs::Trigger::Response> service("/connection_service", &connectionCallback);

void setup() 
{
  // put your setup code here, to run once:
  pinMode(13, OUTPUT);
  nh.initNode();
  
  nh.advertise(pub1);
  nh.advertise(pub2);
  nh.advertise(pub3);
  
  nh.subscribe(sub1);

  nh.advertiseService(service);
  digitalWrite(13, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  bool left_reading = digitalRead(button_pin_left);
  bool middle_reading = digitalRead(button_pin_middle);
  bool right_reading = digitalRead(button_pin_right);
  
  unsigned long currentMillis = millis();
  
  if(currentMillis - previousMillis >= interval)
  {
    previousMillis = currentMillis;
    button_left_pressed.data = left_reading;
    button_middle_pressed.data = middle_reading;
    button_right_pressed.data = right_reading;
    
    pub1.publish(&button_left_pressed);
    pub2.publish(&button_middle_pressed);
    pub3.publish(&button_right_pressed);
  }
  nh.spinOnce();
  delay(1);
}
