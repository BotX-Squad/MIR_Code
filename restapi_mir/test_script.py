import mir
import time

cls_mir = mir.MiR()


while True:

    current_angle = cls_mir.get_current_position()

    print('Result: ', current_angle, 'Time: ', time.time())
