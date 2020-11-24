import rospy
from std_msgs.msg import Int32
import random

if __name__=='__main__':

    rospy.init_node('Angle_publisher')
    pub = rospy.Publisher('/mir_direction', Int32, queue_size=1)
    r = rospy.Rate(0.2)

    while not rospy.is_shutdown():
        try:
            rand_angle = random.randint(-180, 180)
            pub.publish(rand_angle)
            r.sleep()

        except KeyboardInterrupt:
            stored_exception=sys.exc_info()
            break
