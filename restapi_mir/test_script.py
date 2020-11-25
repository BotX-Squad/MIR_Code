import mir
import time
import sys

cls_mir = mir.MiR()

def remap(angle):
    if angle < -180:
        angle = angle + 360
    elif angle > 180:
        angle = angle - 360
    return angle

for x in range(-360, 360):
    angle = remap(x)
    print('This is x: {0} and this is angle: {1}'.format(x, angle))







'''
try:

    if sys.argv[1] == 'init':
        print('Running the initialization...')
    elif sys.argv[1] == 'run':
        print('Running the main function...')
    elif sys.argv[1] == 'delete':
        print('Deleting mission...')
        #mission_id = cls_mir.get_mission_guid('Orientation_test')
        response = cls_mir.delete_mission('Orientation_test')
        print(response)
except:
    print('Please input either "init" or "run"')
'''
