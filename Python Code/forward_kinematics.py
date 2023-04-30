#! /usr/bin/env python
# Forward Kinematics - Pick and place

import rospy
import sys
import numpy as np
from std_msgs.msg import Float64
from std_srvs.srv import Empty
from open_manipulator_msgs.srv import SetJointPosition, SetJointPositionRequest

def inverse(a): 
    d1, a2, a3, d4 = 0.126, 0.225, 0.150, 0.055
    x = a[0]
    y = a[1]
    z = a[2]
    roll = 0
    pitch = 0
    yaw = 0
    # Calculate the rotation matrix from the given Euler angles
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(roll), -np.sin(roll)],
                    [0, np.sin(roll), np.cos(roll)]])
    R_y = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                    [0, 1, 0],
                    [-np.sin(pitch), 0, np.cos(pitch)]])
    R_z = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                    [np.sin(yaw), np.cos(yaw), 0],
                    [0, 0, 1]])
    R = R_z.dot(R_y).dot(R_x)
    # Calculate the position of the end effector
    p = np.array([x, y, z])
    # Calculate the position of the wrist center
    p_wc = p - d4 * R[:, 2]

    # Calculate the joint angles
    theta1 = np.arctan2(p_wc[1], p_wc[0])
    d = np.sqrt(p_wc[0]**2 + p_wc[1]**2)
    s = p_wc[2] - d1
    theta2_1 = np.arctan2(s, d - a2)
    theta2_2 = np.arctan2(s, d + a2)
    alpha = np.arccos((a2**2 + (d-s)**2 - a3**2) / (2*a2*np.sqrt((d-s)**2 + a2**2)))
    theta3_1 = np.pi/2 - alpha - np.arctan2(d-s, a2)
    theta3_2 = np.pi/2 + alpha - np.arctan2(d-s, a2)
    theta4_1 = np.arctan2(R[1, 0], R[0, 0])
    theta4_2 = np.arctan2(-R[1, 0], -R[0, 0])
    # Choose the solution with the smallest joint angle changes
    joint_angles1 = [theta1, theta2_1, theta3_1, theta4_1]
    joint_angles2 = [theta1, theta2_2, theta3_2, theta4_2]
    diff1 = np.sum(np.abs(np.subtract(joint_angles1, np.zeros(4))))
    diff2 = np.sum(np.abs(np.subtract(joint_angles2, np.zeros(4))))
    i_array = [0,0,0,0]
    if diff1 < diff2:
        i_array = joint_angles1
    else:
        i_array = joint_angles2

    forward(i_array)

def forward(b):
    rospy.init_node('service_set_joint_position_client')
    rospy.wait_for_service('/goal_joint_space_path')
    goal_joint_space_path_service_client = rospy.ServiceProxy('/goal_joint_space_path', SetJointPosition)
    goal_joint_space_path_request_object = SetJointPositionRequest()
    goal_joint_space_path_request_object.planning_group = 'arm'
    goal_joint_space_path_request_object.joint_position.joint_name = ['joint1', 'joint2', 'joint3', 'joint4']
    goal_joint_space_path_request_object.joint_position.position = b
    goal_joint_space_path_request_object.joint_position.max_accelerations_scaling_factor = 1.0
    goal_joint_space_path_request_object.joint_position.max_velocity_scaling_factor = 1.0
    goal_joint_space_path_request_object.path_time = 4.5
    rospy.loginfo("Arm Movement...")
    result = goal_joint_space_path_service_client(goal_joint_space_path_request_object)
    print (result)
    rospy.sleep(5)

def grip_move(c):
    if (c== 'open'):
        c = [-0.01]
    else:
        c = [0.01]  
    rospy.init_node('service_set_joint_position_client')
    rospy.wait_for_service('/goal_tool_control')
    goal_joint_space_path_service_client = rospy.ServiceProxy('/goal_tool_control', SetJointPosition)
    goal_joint_space_path_request_object = SetJointPositionRequest()
    goal_joint_space_path_request_object.planning_group = 'gripper'
    goal_joint_space_path_request_object.joint_position.joint_name = ['gripper']
    goal_joint_space_path_request_object.joint_position.position = c
    goal_joint_space_path_request_object.joint_position.max_accelerations_scaling_factor = 1.0
    goal_joint_space_path_request_object.joint_position.max_velocity_scaling_factor = 1.0
    goal_joint_space_path_request_object.path_time = 4.0
    rospy.loginfo("Gripper Movement...")
    result = goal_joint_space_path_service_client(goal_joint_space_path_request_object)
    print (result)
    rospy.sleep(4.5)

def home():
    forward([0,0,0,0])

def intermediate():
    forward([0,-1.05,0.350,0.70])

def gripper_open():
    grip_move('open')

def gripper_close():
    grip_move('close')

def move_robot():
    home()
    gripper_open()
    forward(source)
    gripper_close()
    intermediate()
    forward(dest)
    gripper_open()
    intermediate()
    home()

#source
source = [0,-0.249,0.05,1.75]

#destination
dest = [-0.4,-0.2,1,-0.8]

move_robot()