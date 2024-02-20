#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_msgs.msg import Bool

rospy.init_node("arduino_comand")


class ArduinoControl:
	def __init__(self):
		self.reverse = False 
		
		self.pub1 = rospy.Publisher("turtle1/cmd_vel", Twist, queue_size = 10)
		self.pub2 = rospy.Publisher("command", String, queue_size = 10)
		
		self.sub1 = rospy.Subscriber("botton_left", Bool, self.leftCb)
		self.sub2 = rospy.Subscriber("botton_middle", Bool, self.middleCb)
		self.sub3 = rospy.Subscriber("botton_right", Bool, self.rightCb)
		
		self.button_left_pressed =False
		self.button_middle_pressed =False
		self.button_right_pressed =False
		
	def leftCb(self, msg):
		self.button_left_pressed = msg.data
		
	def middleCb(self, msg):
		self.button_middle_pressed = msg.data
	
	def rightCb(self, msg):
		self.button_right_pressed = msg.data
		
	def check_input(self):
		if self.button_left_pressed and not self.button_middle_pressed and not self.button_right_pressed: 
			#left
			cmd = Twist()
			cmd.linear.x = 1
			cmd.angular.z= 1
			self.pub1.publish(cmd)
			self.pub2.publish("Left turn")
			
		elif not self.button_left_pressed and not self.button_middle_pressed and self.button_right_pressed: 
			#right
			cmd = Twist()
			cmd.linear.x = 1
			cmd.angular.z= -1
			self.pub1.publish(cmd)
			self.pub2.publish("Right turn")
			
		elif not self.button_left_pressed and self.button_middle_pressed and not self.button_right_pressed:
			#toggle reverse
			self.reverse = not self.reverse
			
		elif self.button_left_pressed and not self.button_middle_pressed and self.button_right_pressed:
			if self.reverse:
				cmd = Twist()
				cmd.linear.x = -1
				cmd.angular.z= 0.0
				self.pub1.publish(cmd)
				self.pub2.publish("Backward")
			else:
				cmd = Twist()
				cmd.linear.x = 1
				cmd.angular.z= 0.0
				self.pub1.publish(cmd)
				self.pub2.publish("Forward")
				
arduino_control = ArduinoControl()

rate = rospy.Rate(1)
   
while (not rospy.is_shutdown()):
	arduino_control.check_input()
	rate.sleep()


			 
		
		
