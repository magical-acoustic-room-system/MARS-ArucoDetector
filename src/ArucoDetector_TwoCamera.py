import pyrealsense2 as rs
import numpy as np
import cv2
from cv2 import aruco
from Pisition_Calculator import position


class ArucoDetector_TwoCamera:

    def __init__(self):
        realsense_ctx = rs.context()
        connected_devices = []

        for i in range(len(realsense_ctx.devices)):
            detected_camera = realsense_ctx.devices[i].get_info(rs.camera_info.serial_number)
            connected_devices.append(detected_camera)

        # Configure depth and color streams...
        # ...from Camera 1
        self.pipeline_1 = rs.pipeline()
        config_1 = rs.config()
        config_1.enable_device(connected_devices[0])
        config_1.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config_1.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        print("Device 1 constucted, SERIAL_NUMBER is", connected_devices[0])
        # ...from Camera 2
        self.pipeline_2 = rs.pipeline()
        config_2 = rs.config()
        config_2.enable_device(connected_devices[1])
        config_2.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config_2.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        print("Device 2 constucted, SERIAL_NUMBER is", connected_devices[1])

        # Start streaming from both cameras
        self.pipeline_1.start(config_1)
        self.pipeline_2.start(config_2)
        print("Start streaming")

        # Initialize for the Aruco parameters
        self.dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
        self.marker_siza = 0.05
        self.parameters =  aruco.DetectorParameters()

    def get_frames(self, pipeline):
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        if not depth_frame or not color_frame:
            return False, None, None
        return True, depth_image, color_image
    
    def detect_aruco(self, color_frame, depth_frame, device_id):
        corners, ids, rejectedImgPoints = aruco.detectMarkers(color_frame, self.dictionary)
        dis = []

        if ids is not None:
            distance = []
            for marker in corners[0]:
                for corner in marker:
                    point = (int(corner[0]), int(corner[1]))
                    cv2.circle(color_frame, point, 4, (0, 0, 255))
                    distance.append(depth_frame[int(corner[1]), int(corner[0])])
            aveDis = sum(distance)/4
            dis.append(aveDis)

            # the result of the distance is in cm, and it is the average distance of four cornors
            print("Distance of the marker from Device", device_id, "is:", aveDis/10.0, "cm")
            
        self.position = position(dis[0], dis[1])
        return        
    
    def display(self):
        while True:
            ret1, depth_frame1, color_frame1 = self.get_frames(self.pipeline_1)
            ret2, depth_frame2, color_frame2 = self.get_frames(self.pipeline_2)

            self.detect_aruco(color_frame1, depth_frame1, 1)
            self.detect_aruco(color_frame2, depth_frame2, 2)

            # cv2.imshow("depth frame", depth_frame)
            images = np.hstack((color_frame1,color_frame2))
            cv2.imshow("Color frame", images)
            key = cv2.waitKey(1)
            if key == 27:
                break

    def stop(self):
        # Stop streaming
        self.pipeline_1.stop()
        self.pipeline_2.stop()
        cv2.destroyAllWindows()

def main():
    Detector = ArucoDetector_TwoCamera()
    Detector.display()
    Detector.stop()

if __name__ == "__main__":
    main()
