import mir
import time
import rospy
from std_msgs.msg import Int32, String
import numpy as np

def init_mission(cls_mir):

    mission_id = cls_mir.create_mission('Orientation_test')
    cls_mir.post_position('martin_test')
    result, position_id = cls_mir.create_action(mission_id, 'martin_test', action_type='move')

    return mission_id, position_id


def ori_mission(cls_mir, angle):

    # Find the ids for the mission and used position
    mission_id = cls_mir.get_mission_guid('Orientation_test')
    position_id = cls_mir.get_position_guid('martin_test')

    # Get the current position (postion_id could also be used)
    current_pos = cls_mir.get_current_position()
    x = cls_mir.get_specific_position(position_id)['pos_x']
    y = cls_mir.get_specific_position(position_id)['pos_y']
    # Modify the function position with the new incoming angle
    response = cls_mir.set_position(position_id, x, y, angle)
    return mission_id

def get_dist(angle):
    got_position = False
    while not got_position:
        try:
            position = cls_mir.get_current_position()
            current_angle = position[2]
            got_position = True
        except KeyError:
            pass

    phi = abs(angle - current_angle) % 360
    dist = 360 - phi if phi > 180 else phi
    return dist

def remap(angle):
    print('This is the angle: ', angle)
    if angle < -180:
        angle = angle + 360
    elif angle > 180:
        angle = angle - 180

    return angle

if __name__=='__main__':
    angle = 0
    cls_mir = mir.MiR()
    cls_mir.put_state_to_execute()
    rospy.init_node('rest_api_node')
    pub = rospy.Publisher('/mir_status', String, queue_size=1)
    #mission_id, position_id = init_mission(cls_mir)

    pub.publish('done')

    while not rospy.is_shutdown():
        pub.publish('done')
        angle_data = rospy.wait_for_message('/mir_direction', Int32)
        current_angle = cls_mir.get_current_position()[2]
        angle = remap(-1*angle_data.data + current_angle)
        print('This is the angle: ', angle)
        mission_id = ori_mission(cls_mir, np.around(angle))
        response = cls_mir.post_to_mission_queue(mission_id)
        pub.publish('moving')
        while get_dist(angle) > 1:
            pass

        print('goal reached')
        pub.publish('done')
