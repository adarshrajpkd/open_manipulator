#! /usr/bin/env python

#import
import pybullet as p
import numpy as np
import time
import matplotlib.pyplot as plt
import pybullet_data as pd
import rospy
import sys
from std_msgs.msg import Float64
from std_srvs.srv import Empty
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from open_manipulator_msgs.srv import SetJointPosition, SetJointPositionRequest
from sensor_msgs.msg import JointState

#initialise
p.connect(p.GUI)
p.setGravity(0, 0, -9.81)
p.setTimeStep(1./240.)
p.setAdditionalSearchPath(pd.getDataPath())
robot = p.loadURDF("/home/adarsh/catkin_ws/src/open_manipulator/open_manipulator_description/urdf/output.urdf", [0, 0, 0])
num_joints = p.getNumJoints(robot)
joint_indices = list(range(num_joints))
joint_damping = [0.1] * num_joints
joint_angles = {joint_name: [] for joint_name in ['joint1', 'joint2', 'joint3', 'joint4', 'gripper']}


#functions
def callback(data):
    # Store the joint angles for each joint
    for i in range(len(data.name)):
        joint_name = data.name[i]
        joint_angle = data.position[i]
        joint_angles[joint_name].append(joint_angle)
def plot_fk():
     rospy.Subscriber('/open_manipulator_x/joint_states', JointState, callback)
     while not rospy.is_shutdown():
          plt.clf()
          for joint_name in joint_angles.keys():
               plt.plot(joint_angles[joint_name])
          plt.xlabel('Time (s)')
          plt.ylabel('Joint Angle (rad)')
          plt.title('Joint Angles of Open Manipulator X')
          plt.legend(joint_angles.keys())
          plt.pause(0.1)         
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
    goal_joint_space_path_request_object.path_time = 4
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
def rect(a):
     a1 = [0.286,0,0.205]
     a2 = [0.286,a[0]/2,0.205]
     a3 = [0.286+a[1],a[0]/2,0.205]
     a4 = [0.286+a[1],-a[0]/2,0.205]
     a5 = [0.286,-a[0]/2,0.205]
     ik_move(a1)
     ik_move(a2)
     ik_move(a3)
     ik_move(a4)
     ik_move(a5)
     ik_move(a1)
def circle(r):
    radius = r
    center = [0.286, 0.0, 0.204]
    num_points = 20
    speed = 1
    for i in range(num_points):
        theta = 2 * math.pi * i / num_points
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        z = center[2]
        ik_move([x,y,z])
        rospy.sleep(1 / speed)

home = [0,0,0,0]
inter = [0,-1.05,0.35,0.7]


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
print("Open Manipulator Kinematics \n ")
time.sleep(2)
print ("Enter your selection : \n")
time.sleep(2)
print("1. Forward Kinematics \n2. Inverse Kinematics \n3. Trajectory \n")
temp = int(input("Your Input : "))

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
elif (temp ==3):
     print("You have selected Trajectory Planning...")
     time.sleep(3)
     print("Choose an option.   \n1.Rectangle \n2.Circle")
     y = int(input("Enter your input : "))
     if y == 1:
          l = list(map(float,
                 input("Enter the length and breadth : ").strip().split()))[:2]
          time.sleep(1)
          print (ansi_color('blink_fast',"Planning"))
          time.sleep(3)
          rect(l)
     elif y == 2:
          r = float(input("Enter the radius : "))
          time.sleep(1.5)
          print (ansi_color('blink_fast',"Planning"))
          time.sleep(2)
          circle(r)
else:
    print("Wrong Input")
