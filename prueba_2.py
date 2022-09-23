import time

from CameraSystem import CameraSystem
from PersonDetector import PersonDetector

def main():
    detector = PersonDetector()


    cam = CameraSystem ((0.60,0.01,0.1), (0.60,0.01,0.1), detector, True, address='10.22.240.53', port=80, user='admin', password='L2793C70')
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()



