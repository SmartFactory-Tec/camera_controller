import time
import os
import toml
from CameraSystem import CameraSystem
from PersonDetector import PersonDetector


def main():


    detector = PersonDetector()
    # camera_settings = toml.load("CameraSettings.toml")

    # for camera_name, camera in camera_settings.items():
    #     pid_x = camera["pid_x"]
    #     cam = CameraSystem(pid_x, camera["pid_y"], detector, camera["controllable"], address= camera["address"],port= camera["port"], user=camera["user"], password= camera["password"])
    cam = CameraSystem ((0.45,0.01,0.05), (0.3,0.01,0), detector, True, address=os.environ["CAMERA_ADDRESS"], port=int(os.environ["CAMERA_PORT"]), user=os.environ["CAMERA_USER"], password=os.environ["CAMERA_PASSWORD"])
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()