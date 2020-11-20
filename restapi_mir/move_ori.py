import mir
import time



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


if __name__=='__main__':

    cls_mir = mir.MiR()
    cls_mir.put_state_to_execute()
    #mission_id, position_id = init_mission(cls_mir)
    while True:
        angle = input('Type the wanted angle: ')

        mission_id = ori_mission(cls_mir, int(angle))
        response = cls_mir.post_to_mission_queue(mission_id)
