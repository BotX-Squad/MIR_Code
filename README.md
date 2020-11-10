# MIR_Code
This repository contains code for the MiR 200 robot with a range of different uses. The main objectives is to some develop some HRI capabilities for the platform.
Some of the desired capabilities are listed below: 
- Wi-Fi heatmap generation and evaluation.
- GUI for logging positions in the AAU smart lab for later use in discrete event simulations.
- Simple positional controllers and tele-operation using joystick.
- Object detection and depth sensing using Intel Realsense Camera.
- Leg detection from ROS.
- Goal publishing to the REST API interface of the MiR robot. 
- Application interface for working with cloud computing and natural language processing using AAU developed Max(botX) and CLAAUDIA.

To export the ROS master:
```
export ROS_MASTER_URI=http://192.168.12.20:11311
export ROS_IP=192.168.12.246 # find with ifconfig
```
