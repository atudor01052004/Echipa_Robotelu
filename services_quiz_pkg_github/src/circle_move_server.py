#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from services_quiz_pkg.srv import CircleMove, CircleMoveResponse
from tf.transformations import euler_from_quaternion


er_pozitie_x = 0.0
er_pozitie_y = 0.0
er_unghi_yaw = 0.0
er_odom_primit = False


def er_callback_odom(er_msg):
    global er_pozitie_x, er_pozitie_y, er_unghi_yaw, er_odom_primit

    er_pozitie_x = er_msg.pose.pose.position.x
    er_pozitie_y = er_msg.pose.pose.position.y

    er_orientare = er_msg.pose.pose.orientation
    (_, _, er_yaw) = euler_from_quaternion([er_orientare.x, er_orientare.y, er_orientare.z, er_orientare.w])
    er_unghi_yaw = er_yaw

    er_odom_primit = True


def er_normalizeaza_unghi(er_unghi):
    while er_unghi > math.pi:
        er_unghi -= 2.0 * math.pi
    while er_unghi < -math.pi:
        er_unghi += 2.0 * math.pi
    return er_unghi


def er_executa_cerc(er_pub, er_rata, er_raza):
    global er_unghi_yaw

    er_yaw_start = er_unghi_yaw
    er_unghi_total_parcurs = 0.0
    er_yaw_anterior = er_yaw_start

    er_viteza_angulara = 0.3
    er_viteza_liniara = er_viteza_angulara * er_raza

    er_comanda = Twist()
    er_comanda.linear.x = er_viteza_liniara
    er_comanda.angular.z = er_viteza_angulara

    rospy.loginfo("Echipa Robotelu incepe sa faca cercul cu raza {} m".format(er_raza))

    while not rospy.is_shutdown():
        er_diferenta = er_normalizeaza_unghi(er_unghi_yaw - er_yaw_anterior)
        er_unghi_total_parcurs += abs(er_diferenta)
        er_yaw_anterior = er_unghi_yaw

        if er_unghi_total_parcurs >= 2.0 * math.pi:
            break

        er_pub.publish(er_comanda)
        er_rata.sleep()

    er_pub.publish(Twist())
    rospy.sleep(0.5)
    rospy.loginfo("Echipa Robotelu a terminat un cerc complet!")


def er_handle_circle_move(er_req):
    global er_odom_primit

    rospy.loginfo("Echipa Robotelu a primit cererea pentru cerc: raza={}, repetitii={}".format(er_req.side, er_req.repetitions))

    while not er_odom_primit and not rospy.is_shutdown():
        rospy.loginfo("Echipa Robotelu asteapta date de la /odom...")
        rospy.sleep(1.0)

    er_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    er_rata = rospy.Rate(20)
    rospy.sleep(0.5)

    for er_i in range(er_req.repetitions):
        rospy.loginfo("Echipa Robotelu executa cercul {}/{}".format(er_i + 1, er_req.repetitions))
        er_executa_cerc(er_pub, er_rata, er_req.side)

    rospy.loginfo("Echipa Robotelu a finalizat cercul/cercurile cu succes!")
    return CircleMoveResponse(True)


if __name__ == "__main__":
    rospy.init_node('er_circle_move_server_node')
    rospy.Subscriber('/odom', Odometry, er_callback_odom)
    rospy.Service('/er_make_circle', CircleMove, er_handle_circle_move)
    rospy.loginfo("Echipa Robotelu - A activat serverul! RObotul asteapta comenzi")
    rospy.spin()
