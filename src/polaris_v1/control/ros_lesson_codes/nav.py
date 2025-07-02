#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Düğüm Yardımıyla Hedefe Gitme
"""

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def istemci():
    rospy.init_node("hedefe_git")
    istemci = actionlib.SimpleActionClient("move_base",MoveBaseAction)
    istemci.wait_for_server()
    hedef = MoveBaseGoal()
    hedef.target_pose.header.frame_id = "map"
    hedef.target_pose.pose.position.x = 1.0
    hedef.target_pose.pose.position.y = 0.0
    hedef.target_pose.pose.orientation.w = 1.0
    istemci.send_goal(hedef)
    istemci.wait_for_result()
    print(istemci.get_result())
    rospy.loginfo("Hedefe varildi !")

istemci()
