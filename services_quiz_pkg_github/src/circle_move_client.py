#!/usr/bin/env python

import sys
import rospy
from services_quiz_pkg.srv import CircleMove


def er_apeleaza_serviciu_cerc(er_raza, er_repetitii):
    rospy.loginfo("Echipa Robotelu cauta serviciul pentru cerc")
    rospy.wait_for_service('/er_make_circle')
    rospy.loginfo("Echipa Robotelu a gasit serviciul!")

    try:
        er_make_circle = rospy.ServiceProxy('/er_make_circle', CircleMove)
        rospy.loginfo("Echipa Robotelu trimite comanda: raza={}, repetitii={}".format(er_raza, er_repetitii))

        er_raspuns = er_make_circle(er_raza, er_repetitii)

        rospy.loginfo("Echipa Robotelu - Comanda executata: {}".format(er_raspuns.success))
    except rospy.ServiceException as er_eroare:
        rospy.logerr("Echipa Robotelu - Apelul serviciului a esuat: {}".format(er_eroare))


if __name__ == "__main__":
    rospy.init_node('er_circle_move_client_node')

    er_raza_val = 1.0
    er_rep_val = 1

    er_argv = rospy.myargv(argv=sys.argv)
    if len(er_argv) == 3:
        er_raza_val = float(er_argv[1])
        er_rep_val = int(er_argv[2])

    er_apeleaza_serviciu_cerc(er_raza_val, er_rep_val)
