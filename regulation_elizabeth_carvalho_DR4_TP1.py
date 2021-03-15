#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy, math, angles
from geometry_msgs.msg import Pose2D, Twist
from turtlesim.msg import Pose

def callback_turtle_pose(msg):
	#print("Entrei em callback_turtle_pose")
	#print(msg)
	global turtle_odom
	turtle_odom.x = msg.x
	turtle_odom.y = msg.y
	turtle_odom.theta = msg.theta
	

def callback_goal(msg):
	#print("Entrei em callback_goal")
	#print(msg)
	global goal
	goal = msg


def turtle_command(turtle_odom, goal, gain):
	print("Entrei em turtle_command")
	print(turtle_odom)
	print(goal)
	#print(gain)
	
	#Coordenadas da pose atual da tartaruga
	x = turtle_odom.x
	y = turtle_odom.y
	theta = turtle_odom.theta
	
	#Coordenadas de destino da tartaruga
	x_d = goal.x
	y_d = goal.y
	theta_d = goal.theta
	
	#Ganhos
	#K_v = gain[0]
	#K_w = gain[1]
	#K_i = gain[2]
	K_rho = gain[3]
	K_alfa = gain[4]
	K_beta = gain[5]
	
	#Calculando diferença entre distancia de destino e atual (slide 16 - pdf 'controle de veículos')
	e_x = x_d-x
	e_y = y_d-y
		
	#Calculando coordenadas polares para regulação de postura (slide 20,21,22,24 - pdf 'controle de veículos')
	rho = round(math.sqrt(e_x**2 + e_y**2),3) #distância até o destino
	arco_tan = round(math.atan2(e_y,e_x),3) #calculo de arco tangente do heading
	#alfa = round(-theta+arco_tan,3) #direção da trejetória (heading)
	alfa = angles.shortest_angular_distance(theta,arco_tan)
	beta = -round(theta,3)-round(alfa,3)+round(theta_d,3) #orientação final

	#Calculando sinal de controle para velocidade linear (slide 24 - pdf 'controle de veículos')
	v = K_rho*rho
	
	#Calculando sinal de controle para orientação (velocidade angular) 
	w = K_alfa*alfa+K_beta*beta
	
	#Construindo o objeto para publicação
	turtle_vel = Twist()
	turtle_vel.linear.x = v
	turtle_vel.angular.z = w
	
	return turtle_vel
	

def main_regulation():
	#print("Entrei em main_regulation")
	global turtle_odom
	global goal
	
	rospy.init_node('turtle_regulation', anonymous=True) #Nome do nó de controle
	turtle_pose = rospy.Subscriber('/turtle1/pose', Pose, callback_turtle_pose)
	turtle_goal = rospy.Subscriber('/goal',Pose2D,callback_goal)
	pub_cmd_vel = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10) 
	
	rate = rospy.Rate(10)
	cmd_vel = Twist()
	
	while not rospy.is_shutdown():
		cmd_vel = turtle_command(turtle_odom, goal, gain)
		#print(cmd_vel)
		pub_cmd_vel.publish(cmd_vel)
		rate.sleep()
		

########## Main Code #########
turtle_odom = Pose2D()
goal = Pose2D()

k_v = 1.5
k_w = 0.8
k_i = 0.1
k_rho = 0.8
k_alfa = 2
k_beta = -0.6
gain = [k_v, k_w, k_i, k_rho, k_alfa, k_beta]

if __name__ == '__main__':
	main_regulation()
