import time
import os
import toml
from CameraSystem import CameraSystem
from PersonDetector import PersonDetector


def main():


    detector = PersonDetector()

    cam = CameraSystem ((0.60,0.01,0.1), (0.60,0.01,0.1), detector, True, address=os.environ["CAMERA_ADDRESS"], port=int(os.environ["CAMERA_PORT"]), user=os.environ["CAMERA_USER"], password=os.environ["CAMERA_PASSWORD"])
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()