import rospy
import numpy as np
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32, Int32
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import TwistStamped
import math

yaw_current = 0.0
roll_voice = pitch_voice = yaw_voice = 0.0
const_vel = 0.2
kp=0.1

def remap(angle):
    if angle < 0:
        remap_angle = abs(angle+180) + 180
    else:
        remap_angle = angle
    return remap_angle #remap_angle


def get_rotation(msg):
    global yaw_current
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll_temp, pitch_temp, yaw_temp) = euler_from_quaternion (orientation_list)
    yaw_current = remap(math.degrees(yaw_temp))
    print('Current angle in degrees: ', yaw_current)


def get_direction(msg1):
    global yaw_voice
    yaw_voice = remap(msg1.data)+yaw_current


# Start up program
rospy.init_node('Voice_ctrl')
sub = rospy.Subscriber('/robot_pose', Pose, get_rotation)
sub1 = rospy.Subscriber('/mir_direction', Int32, get_direction)
pub = rospy.Publisher('cmd_vel', TwistStamped, queue_size = 1)
r = rospy.Rate(10)
command = TwistStamped()

while not rospy.is_shutdown():

    yaw_voice_rad = math.radians(yaw_voice) # yaw_voice * math.pi/180
    yaw_current_rad = math.radians(yaw_current) # yaw_current * math.pi/180

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
    if dist > 5: # can be made with degrees
        command.twist.angular.z = sign*const_vel
        pub.publish(command)
        print('Sending ctrl commands now!')


    r.sleep()
