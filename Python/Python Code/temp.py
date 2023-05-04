#! /usr/bin/env python

import numpy as np
import time
import matplotlib.pyplot as plt
import pybullet_data as pd
import rospy
import math
import sys
from std_msgs.msg import Float64
from std_srvs.srv import Empty
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from open_manipulator_msgs.srv import SetJointPosition, SetJointPositionRequest
from sensor_msgs.msg import JointState



def fk_move(a):
    rospy.init_node('service_set_joint_position_client')
    rospy.wait_for_service('/goal_joint_space_path')
    goal_joint_space_path_service_client = rospy.ServiceProxy('/goal_joint_space_path', SetJointPosition)
    goal_joint_space_path_request_object = SetJointPositionRequest()
    goal_joint_space_path_request_object.planning_group = 'arm'
    goal_joint_space_path_request_object.joint_position.joint_name = ['joint1', 'joint2', 'joint3', 'joint4']
    goal_joint_space_path_request_object.joint_position.position = a
    goal_joint_space_path_request_object.joint_position.max_accelerations_scaling_factor = 1.0
    goal_joint_space_path_request_object.joint_position.max_velocity_scaling_factor = 1.0
    goal_joint_space_path_request_object.path_time = 4.0
    rospy.loginfo("Doing Service Call")
    result = goal_joint_space_path_service_client(goal_joint_space_path_request_object)
    print (result)
    rospy.sleep(4.0)
def grip_move(x):
    if (x== 'open'):
        x = [0.01]
    else:
        x = [-0.01]  
    rospy.init_node('service_set_joint_position_client')
    rospy.wait_for_service('/goal_tool_control')
    goal_joint_space_path_service_client = rospy.ServiceProxy('/goal_tool_control', SetJointPosition)
    goal_joint_space_path_request_object = SetJointPositionRequest()
    goal_joint_space_path_request_object.planning_group = 'gripper'
    goal_joint_space_path_request_object.joint_position.joint_name = ['gripper']
    goal_joint_space_path_request_object.joint_position.position = x
    goal_joint_space_path_request_object.joint_position.max_accelerations_scaling_factor = 1.0
    goal_joint_space_path_request_object.joint_position.max_velocity_scaling_factor = 1.0
    goal_joint_space_path_request_object.path_time = 2.0
    rospy.loginfo("Gripper...")
    result = goal_joint_space_path_service_client(goal_joint_space_path_request_object)
    print (result)
    rospy.sleep(5.0)

home = [3.14,0,0,0]
inter = [3.14 ]
fk_move(inter)

