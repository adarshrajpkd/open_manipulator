#!/bin/bash
gnome-terminal --geometry=80x20+0+0 -- bash -c "roslaunch open_manipulator_controller open_manipulator_controller.launch use_platform:=false"
sleep 10
gnome-terminal --geometry=80x20+0+0 -- bash -c "roslaunch open_manipulator_gazebo open_manipulator_gazebo.launch"
sleep 10
gnome-terminal --geometry=80x20+0+0 -- bash -c "python3 /home/adarsh/Desktop/movement.py"
