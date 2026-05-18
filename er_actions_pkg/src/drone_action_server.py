#! /usr/bin/env python
import rospy

import actionlib
from std_msgs.msg import Empty
from er_actions_pkg.msg import DroneActionERAction, DroneActionERFeedback, DroneActionERResult

class ServerDronaER(object):
    
  # cream mesajele pentru feedback si rezultat
  er_feedback = DroneActionERFeedback()
  er_result   = DroneActionERResult()

  def __init__(self):
    # publisheri pentru drona
    self.er_takeoff_pub = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
    self.er_land_pub = rospy.Publisher('/ardrone/land', Empty, queue_size=1)

    # cream serverul de actiune
    self.er_as = actionlib.SimpleActionServer("drone_action_server", DroneActionERAction, self.er_goal_callback, False)
    self.er_as.start()
    rospy.loginfo("Serverul  pentru drona echipei Robotelu' a pornit.)")
    
  def er_goal_callback(self, er_goal):
    # acest callback este apelat cand serverul primeste o comanda
    er_rate = rospy.Rate(1)
    er_comanda = er_goal.command.upper()

    if er_comanda == "TAKEOFF":
        self.er_takeoff_pub.publish(Empty())
        rospy.loginfo("Eliberati aerodromul, decoleaza drona.")
        
        while not self.er_as.is_preempt_requested():
            self.er_feedback.status = "TAKING OFF"
            self.er_as.publish_feedback(self.er_feedback)
            er_rate.sleep()
            
        self.er_as.set_preempted()

    elif er_comanda == "LAND":
        self.er_land_pub.publish(Empty())
        rospy.loginfo("Eliberati aerodromul, aterizeaza drona.")
        
        for i in range(4):
            if self.er_as.is_preempt_requested():
                self.er_as.set_preempted()
                return
            self.er_feedback.status = "LANDING"
            self.er_as.publish_feedback(self.er_feedback)
            er_rate.sleep()
            
        self.er_as.set_succeeded(self.er_result)

    else:
        rospy.logwarn("Eroare " + er_comanda)
        self.er_as.set_aborted(self.er_result)
      
if __name__ == '__main__':
  rospy.init_node('drone_action_server_node')
  ServerDronaER()
  rospy.spin()
