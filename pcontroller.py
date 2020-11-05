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
    global roll_current, pitch_current, yaw_current
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll_current, pitch_current, yaw_current) = euler_from_quaternion (orientation_list)
    #print yaw_current


def get_direction(msg1):
    global yaw_voice
    yaw_voice = msg1.data
    #print(yaw_voice.float32)
    #print yaw_voice

rospy.init_node('rotate_robot')

sub = rospy.Subscriber('/odom', Odometry, get_rotation)
sub1 = rospy.Subscriber('/voice_direction', Float32, get_direction)
pub = rospy.Publisher('cmd_vel', TwistStamped, queue_size=1)
r = rospy.Rate(10)
command =TwistStamped()

while not rospy.is_shutdown():
    #quat = quaternion_from_euler (roll, pitch,yaw)
    #print quat
    yaw_voice_rad = yaw_voice*math.pi/180
    print('This is the voice_deg: ', yaw_voice)
    print('This is the voice_rad: ', yaw_voice_rad)
    if (yaw_voice_rad-yaw_current) > 0.02 :
        command.twist.angular.z = kp * (yaw_voice_rad-yaw_current)
        pub.publish(command)
        print("Goal_pose:{0} Current_pose:{1}".format(yaw_voice_rad, yaw_current))


    r.sleep()
