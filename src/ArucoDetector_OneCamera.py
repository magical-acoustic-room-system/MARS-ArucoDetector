import cv2
from cv2 import aruco
import pyrealsense2 as rs
import numpy as np

class ArucoDetector_OneCamera:

    def __init__(self):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        self.pipeline.start(config)

        self.dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
        self.marker_siza = 0.05
        self.parameters =  aruco.DetectorParameters()

    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        if not depth_frame or not color_frame:
            return False, None, None
        return True, depth_image, color_image

    def release(self):
        self.pipeline.stop()
        self.pipeline.release()
        cv2.destroyAllWindows()

    def display(self):
        while True:
            ret, depth_frame, color_frame = self.get_frame()

            corners, ids, rejectedImgPoints = aruco.detectMarkers(color_frame, self.dictionary)

            if ids is not None:
                distance = []
                for marker in corners[0]:
                    for corner in marker:
                        point = (int(corner[0]), int(corner[1]))
                        cv2.circle(color_frame, point, 4, (0, 0, 255))
                        distance.append(depth_frame[int(corner[1]), int(corner[0])])
                aveDis = sum(distance)/4
                print("Distance of the marker is:", aveDis/10.0, "cm")

            # cv2.imshow("depth frame", depth_frame)
            cv2.imshow("Color frame", color_frame)
            key = cv2.waitKey(1)
            if key == 27:
                break        

def main():
    Detector = ArucoDetector_OneCamera()
    Detector.display()
    Detector.release()

if __name__ == "__main__":
    main()