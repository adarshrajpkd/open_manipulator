#! /usr/bin/env python

import pybullet as p
import numpy as np
import time
import pybullet_data as pd
import rospy
import sys
from std_msgs.msg import Float64
from std_srvs.srv import Empty
from open_manipulator_msgs.srv import SetJointPosition, SetJointPositionRequest

p.connect(p.GUI)
p.setGravity(0, 0, -9.81)
p.setTimeStep(1./240.)
p.setAdditionalSearchPath(pd.getDataPath())
robot = p.loadURDF("/home/adarsh/catkin_ws/src/open_manipulator/open_manipulator_description/urdf/output.urdf", [0, 0, 0])
num_joints = p.getNumJoints(robot)
joint_indices = list(range(num_joints))
joint_damping = [0.1] * num_joints

def ik_move(a):
    x = a[0]
    y = a[1]
    z = a[2]
    end_effector_pos = np.array([x, y, z])
    end_effector_orient = np.array([[0, 0, 0], [0, -0, 0], [0, 0, -1]]) # This rotates the end-effector by 180 degrees around the y-axis
    end_effector_pose = np.eye(4)
    end_effector_pose[:3, :3] = end_effector_orient
    end_effector_pose[:3, 3] = end_effector_pos
    joint_angles = p.calculateInverseKinematics(robot, num_joints - 1, end_effector_pos, end_effector_orient.flatten(), jointDamping=joint_damping)
    fk_move([joint_angles[0],joint_angles[1],joint_angles[2],joint_angles[3]])

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
    goal_joint_space_path_request_object.path_time = 5.0
    rospy.loginfo("Doing Service Call")
    result = goal_joint_space_path_service_client(goal_joint_space_path_request_object)
    print (result)
    rospy.sleep(5)

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
    goal_joint_space_path_request_object.path_time = 5.0
    rospy.loginfo("Gripper...")
    result = goal_joint_space_path_service_client(goal_joint_space_path_request_object)
    print (result)
    rospy.sleep(2)

home = [0,0,0,0]
inter = [0,-1.05,0.35,0.7]

def ansi_color(n,s):
	code={"bold":1,"faint":2,"italic":3,"underline":4,"blink_slow":5,"blink_fast":6,"negative":7,"conceal":8,"strike_th":9,
	"black":30,"red":31,"green":32,"yellow":33,"blue":34,"magenda":35,"cyan":36,"white":37,
	"b_black":40,"b_red":41,"b_green":42,"b_yellow":43,"b_blue":44,"b_magenda":45,"b_cyan":46,"b_white":47,}
	try:
		num=str(code[n])
		value="\033["+num+"m"+s+"\033[0m"
		return value
	except:
		pass
		
#grip_move('open')
#fk_move(home)
#fk_move(source)
#grip_move('close')
#fk_move(inter)
#fk_move(destination)
#grip_move('open')
#fk_move(home)
#grip_move('close')

#ik_move([0.286,0,0.205])
#ik_move([0.128,0,0.105])
#ik_move([0.134,0,0.241])
#ik_move([0.213,-0.062,0.118])

print("\n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n ")
time.sleep(4)
print("Pick and Place - Kinematics \n ")
time.sleep(2)
print ("Enter your selection : \n")
time.sleep(2)
print("1. Forward Kinematics \n2. Inverse Kinematics")
temp = int(input("Enter your selection : "))
if (temp == 1):
    print("You have selected Forward Kinematics...")
    time.sleep(1.5)
    print (ansi_color('blink_fast',"Loading ..."))
    time.sleep(5)
    print("\n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n ")
    source = list(map(float,
                 input("Enter the joint angles for source : ").strip().split()))[:4]

    destination = list(map(float,
                 input("Enter the joint angles for destination : ").strip().split()))[:4]

    print (ansi_color('blink_fast',"Planning"))
    time.sleep(5)
    print("\n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n ")

    grip_move('open')
    fk_move(home)
    fk_move(source)
    grip_move('close')
    fk_move(inter)
    fk_move(destination)
    grip_move('open')
    fk_move(home)
    grip_move('close')
elif (temp == 2):
    print("You have selected Inverse Kinematics...")
    time.sleep(1.5)
    print (ansi_color('blink_fast',"Loading ..."))
    time.sleep(5)
    print("\n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n ")
    source = list(map(float,
                 input("Enter the position values of source : ").strip().split()))[:3]

    destination = list(map(float,
                 input("Enter the position values of destination : ").strip().split()))[:3]

    print (ansi_color('blink_fast',"Planning"))
    time.sleep(5)
    print("\n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n ")
    grip_move('open')
    fk_move(home)
    ik_move(source)
    grip_move('close')
    fk_move(inter)
    ik_move(destination)
    grip_move('open')
    fk_move(home)
    grip_move('close')

else:
    print("Wrong Input")
