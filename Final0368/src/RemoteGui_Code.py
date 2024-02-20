#!/usr/bin/env python3
from tkinter import*
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_msgs.msg import Bool
from std_srvs.srv import Trigger 
from turtlesim.srv import SetPen


frame = Tk()
frame.title("REMOTE")
frame.geometry("200x300")


canvas = Canvas(frame ,width=200, height=300)
canvas.pack()
rospy.init_node("Turtle_Control")

class GUI:
	def __init__(self, canvas):
		self.canvas = canvas
		self.pub1 = rospy.Publisher("turtle1/cmd_vel", Twist, queue_size = 10)
		self.pub2 = rospy.Publisher("command", String, queue_size = 10)
		self.pub3 = rospy.Publisher("pen_mode", Bool, queue_size = 10)
		self.arduino_status = False
		
		
		self.connection_label = Label(frame, text = "arduino's status: ")
		self.connection_label.place(x = 0, y = 20)
		
		self.status_light = self.canvas.create_oval(120, 20, 140, 40, fill='red')

		self.B1 = Button(text = "FW", command=self.fw)
		self.B1.place(x=73, y=120)

		self.B2 = Button(text = "BW", command=self.bw)
		self.B2.place(x=73, y=230)

		self.B3 = Button(text = "LT", command=self.lt)
		self.B3.place(x=20, y=180)

		self.B4 = Button(text = "RT", command=self.rt)
		self.B4.place(x=128, y=180)
		
		self.B5 = Button(text = "PenOn", command=self.pen_on)
		self.B5.place(x=10, y=60)
		
		self.B6 = Button(text = "PenOff", command=self.pen_off)
		self.B6.place(x=120, y=60)
		
		self.set_pen = rospy.ServiceProxy('/turtle1/set_pen', SetPen)
		
	def check_arduino_connection(self):
		try:
			trigger_service = rospy.ServiceProxy('/connection_service', Trigger)
			response = trigger_service()
			if(response.success):
				self.canvas.itemconfig(self.status_light, fill="green")
				
			
			else:
				self.canvas.itemconfig(self.status_light, fill="red")
				
				
					
		except rospy.ServiceException as e:
			self.canvas.itemconfig(self.status_light, fill="red")
			
			
		self.canvas.after(250, self.check_arduino_connection)


	def fw(self):
	    cmd = Twist()
	    cmd.linear.x = 1
	    cmd.angular.z= 0.0
	    self.pub1.publish(cmd)
	    self.pub2.publish("Forward")
	   
		
	def bw(self):
	    cmd = Twist()
	    cmd.linear.x = -1
	    cmd.angular.z= 0.0
	    self.pub1.publish(cmd)
	    self.pub2.publish("Backward")

	   
	       
	def lt(self):
	    cmd = Twist()
	    cmd.linear.x = 1
	    cmd.angular.z= 1
	    self.pub1.publish(cmd)
	    self.pub2.publish("Left turn")

	 
	   
	def rt(self):
	    cmd = Twist()
	    cmd.linear.x = 1
	    cmd.angular.z= -1
	    self.pub1.publish(cmd)
	    self.pub2.publish("Right turn")
	    #publish
	    
	def pen_on(self):
            server_response = self.set_pen(0, 0, 0, 0, 0)
            pen = Bool()
            pen.data = True
            self.pub3.publish(pen)
            
	def pen_off(self):
            server_response = self.set_pen(0, 0, 0, 0, 1)
            pen = Bool()
            pen.data = False
            self.pub3.publish(pen)
    
gui = GUI(canvas)
gui.check_arduino_connection()
frame.mainloop()    
    
    
    
