import pyrealsense2 as rs
import numpy as np
import cv2
import imagezmq
from time import time
import socket
# Create a pipeline
pipeline = rs.pipeline()

# Create a config and configure the pipeline to stream
#  different resolutions of color and depth streams
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)

# Start streaming
profile = pipeline.start(config)

sender = imagezmq.ImageSender(connect_to='tcp://172.27.15.18:5555')

rgb_cam = 'RGB Camera'
depth_cam = 'Depth Camera'
try:
    while True:
        # Get frameset of color and depth
        start = time()
        frames = pipeline.wait_for_frames()
        end = time()
        #print('fps counter: ', 1/(end-start))

        # Get aligned frames
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        image_depth = np.asanyarray(depth_frame.get_data())
        image_color = np.asanyarray(color_frame.get_data())
        image_combined = np.dstack((image_color, image_depth))
        #print('image_color_size: {} image_depth_size {}'.format(np.shape(image_combined), np.shape(image_depth)))
        print(image_depth)
        # create color mask for depth image
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(image_depth, alpha=0.03), cv2.COLORMAP_JET)
        # images = np.hstack((bg_removed, depth_colormap))
        cv2.namedWindow('Depth', cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow('Color', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Depth', image_depth)
        cv2.imshow('Color', image_color)
        #sender.send_image(rgb_cam, image_color)
        sender.send_image(depth_cam, image_combined)
        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    pipeline.stop()
