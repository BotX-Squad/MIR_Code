import rospy
import numpy as np
import message_filters
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32, Int32
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import TwistStamped
import math

yaw_current = -180.0
roll_voice = pitch_voice = yaw_voice = 0.0
const_vel = 0.3
const_vel_slow = 0.2
const_vel_slowest = 0.1
kp=0.1

def remap(angle):
    print('This is the angle: ', angle)
    if angle < -180:
        angle = angle + 360
    return angle


def get_rotation(msg):
    global yaw_current
    orientation_q = msg.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll_temp, pitch_temp, yaw_temp) = euler_from_quaternion (orientation_list)
    yaw_current = math.degrees(yaw_temp)
    #print('Current angle in degrees: ', yaw_current)


def get_direction(msg1):
    global yaw_voice
    yaw_voice = remap(-1*msg1.data + yaw_current)


# Start up program
rospy.init_node('Voice_ctrl')
sub = rospy.Subscriber('/robot_pose', Pose, get_rotation)
sub1 = rospy.Subscriber('/mir_direction', Int32, get_direction)
pub = rospy.Publisher('cmd_vel', TwistStamped, queue_size = 1)
r = rospy.Rate(10)
command = TwistStamped()

while not rospy.is_shutdown():

    # find the shortest turning direction
    if yaw_current < yaw_voice:
        if abs(yaw_current - yaw_voice) < 180:
            sign = 1
        else:
            sign = -1
    else:
        if abs(yaw_current - yaw_voice) < 180:
            sign = -1
        else:
            sign = 1
    # calculate the true error between [0, 180] for the angle to overcome wrap around
    phi = abs(yaw_voice - yaw_current) % 360
    dist = 360 - phi if phi > 180 else phi
    print('This is the difference: ', dist)
    print('Goal_pose:{0} Current_pose:{1}'.format(yaw_voice, yaw_current))
    # add dead zone, to avoid oscillations
    if dist < 20:
        if dist < 10: # can be made with degrees
            command.twist.angular.z = sign*const_vel_slowest
            pub.publish(command)
            print('Sending very slow ctrl commands now!')
        else:
            command.twist.angular.z = sign*const_vel_slow
            pub.publish(command)
            print('Sending slow ctrl commands now!')
    else:
            command.twist.angular.z = sign*const_vel
            pub.publish(command)
            print('Sending normal ctrl commands now!')


    r.sleep()
