import rospy
import numpy as np
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import TwistStamped
import math

roll_current = pitch_current = yaw_current = 0.0
roll_voice = pitch_voice = yaw_voice = 0.0

kp=0.1

def get_rotation(msg):
    global yaw_current
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll_temp, pitch_temp, yaw_temp) = euler_from_quaternion(orientation_list)
    yaw_current degrees(yaw_temp)



def get_direction(msg1):
    global yaw_voice
    yaw_voice = msg1.data


rospy.init_node('rotate_robot')

sub = rospy.Subscriber('/odom', Odometry, get_rotation)
sub1 = rospy.Subscriber('/voice_direction', Float32, get_direction)
pub = rospy.Publisher('cmd_vel', TwistStamped, queue_size=1)
r = rospy.Rate(10)
command =TwistStamped()

while not rospy.is_shutdown():
    print('This is the current orientation: ', yaw_current)
    print('This is the voice_deg: ', yaw_voice)
    phi = math.abs(yaw_voice - yaw_current) % 360
    dist = 360 - phi if phi > 180 else dist = phi
    print('This is the minimum error to the desired pose: ', dist)
    if dist > 2: # current deadzone is 2 degrees.
        command.twist.angular.z = kp * dist
        pub.publish(command)
        print("Goal_pose:{0} Current_pose:{1}".format(yaw_voice_rad, yaw_current))


    r.sleep()
