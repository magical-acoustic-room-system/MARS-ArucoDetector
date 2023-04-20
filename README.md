# Aruco
This is a project to detect the Aruco marker with two Realsense D455i cameras for [magical-acoustic-room-system](https://github.com/magical-acoustic-room-system).

## How to use
### Set up the python environment.

Even though it is not required, it is highly recommended to set up a virtual enrivonment for this project if you just want to try it out.

```
python -m venv myenv
source myenv/bin/activate
```

It is entirely fine if you skip above steps, if you want constantly work with this project.

Intall the required packages for this project.

```
pip install -r requirements.txt
```

### Connect Realsense D455i cameras to your computer.

Please installl [Intel RealSense SDK 2.0](https://www.intelrealsense.com/sdk-2/) for better visual display.

### Run the code

Run the code in the terminal. There are two diffenrent mode of detecting, one camera or two cameras. Choose the one you want.

```bash
python ArucoDetector_OneCamera.py
python ArucoDetector_TwoCamera.py
```
There will be printout message in the terminal, which indicates and distance of Aruco Marker to each camera.

Press the Esc key to exit when it is done.

### Note

1. Version of cv2.aruco

   Make sure the version of **cv2.aruco** match. There is a vital change of **cv2.aruco**. If you are using the mismatch version of **cv2.aruco**. It most likely can't detect the Aruco Marker successfully. There is also a change of api between the previous and newest version, which will cause compile failed.

2. Mutiple Cameras(more than two)

   It is totally doable if you want to add more than two cameras. Please check `.src/ArucoDetector_TwoCamera`, I mentioned about the **SERIAL_NUMBER**, reading my comments could be a good start to adding more cameras. Just make sure connecting the cameras correctly to pipelines correctly according the **SERIAL_NUMBER**.

3. Potential error due to not using official cables

   There is a major issue with cables of intel Realsense Camera! Please use the official cables(it is a USB-B to type-C cable) if possible.

   1. If you don't have USB-B ports and only have type-C ports on your device, do not try to use a type-C to type-C cable to connect the camera. Use a USB-B to type-C cable and a USB-B to type-C converter instead. I know it is confusing. But the protocol of intel Realsense Camera is weird.
   2. If you are using a unofficial USB-B to type-C cable, there is potential error when connecting camera. Your device may fail to accept the data stream. I have avoided the data stream issue by **SERIAL_NUMBER**. But there may have more potential issues I haven't met yet.

4. Mutiple Aruco Marker detect

   According to the requirements of the project, I just implemented detecting one Aruco Marker. However, detecting multiple marker is pratical and easy from my code. Please check the api of **cv2.aruco.detectMarkers**, the output actually should be an array of all markers detected, just slight changes to my code could display all markers.