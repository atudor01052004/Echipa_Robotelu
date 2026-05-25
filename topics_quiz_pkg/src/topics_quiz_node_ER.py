#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


def callback(msg):
    move = Twist()
    
    front = msg.ranges[0]
    left = msg.ranges[90]
    right = msg.ranges[270]

    if front > 1.0:
        move.linear.x = 0.2
        move.angular.z = 0.0
    
    if front < 1.0:
        move.linear.x = 0.0
        move.angular.z = 0.5

    if right < 1.0:
        move.linear.x = 0.0
        move.angular.z = 0.5

    if left < 1.0:
        move.linear.x = 0.0
        move.angular.z = -0.5

    pub.publish(move)

  
rospy.init_node('topics_quiz_node')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
sub = rospy.Subscriber('/scan', LaserScan, callback)
rospy.spin()
