import mir
import time
import rospy
from std_msgs.msg import Int32, String


def init_mission(cls_mir):

    mission_id = cls_mir.create_mission('Orientation_test')
    cls_mir.post_position('test_pos')
    result, position_id = cls_mir.create_action(mission_id, 'test_pos', action_type='move')

    return mission_id, position_id


def ori_mission(cls_mir, angle):

    # Find the ids for the mission and used position
    mission_id = cls_mir.get_mission_guid('Orientation_test')
    position_id = cls_mir.get_position_guid('test_pos')

    # Get the current position (postion_id could also be used)
    current_pos = cls_mir.get_current_position()

    # Modify the function position with the new incoming angle
    response = cls_mir.set_position(position_id, current_pos[0], current_pos[1], angle)
    return mission_id

def get_dist(angle):
    position = cls_mir.get_current_position()
    current_angle = position[2]
    phi = abs(angle - current_angle) % 360
    dist = 360 - phi if phi > 180 else phi
    return dist

if __name__=='__main__':
    angle = 0
    cls_mir = mir.MiR()
    cls_mir.put_state_to_execute()
    rospy.init_node('stupid_node')
    pub = rospy.Publisher('/mir_status', String, queue_size=1)
    #mission_id, position_id = init_mission(cls_mir)

    while not rospy.is_shutdown():
        angle_data = rospy.wait_for_message('/mir_direction', Int32)
        angle = angle_data.data
        print('This is the angle: ', angle)
        mission_id = ori_mission(cls_mir, int(angle))
        current_angle = cls_mir.get_current_position()[2]
        phi = abs(angle - current_angle) % 360
        dist = 360 - phi if phi > 180 else phi
        response = cls_mir.post_to_mission_queue(mission_id)
        pub.publish('moving')
        while get_dist(angle) > 2:
            pass

        print('goal reached')
        pub.publish('done')
