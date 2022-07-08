import cv2
from threading import Thread, Lock, Event
from typing import TypedDict
from copy import deepcopy
from camera_server.api import Camera
from camera_server.api.CameraController import CameraController
from camera_server.api.PersonDetector import PersonDetector
from camera_server.api.utility import draw_detection_boxes, calculate_target_position


class CameraSystem():
    def __init__(self, pid_x: tuple[float, float, float],
                 pid_y: tuple[float, float, float], detector, controllable, id = None,
                 address = None, port = None, user = None,
                 password = None):

        self.__id = id

        self.__address = address
        self.__port = port
        self.__user = user
        self.__password = password
        self.__pid_x = pid_x
        self.__pid_y = pid_y
        self.__controllable = controllable
        self.__detector = detector

        self.__latest_frame = None
        self.__latest_detections = []

        self.__frame_lock = Lock()
        self.__detections_lock = Lock()

        self.__is_ready_flag = Event()

        self.__thread = Thread(target=self.__update)
        self.__thread.daemon = True
        self.__thread.start()

    def __async_init(self):
        if self.__id is not None:
            self.__camera = Camera(id=self.__id)
        else:
            self.__camera = Camera(address=self.__address, port=self.__port, user=self.__user, password=self.__password)

        if self.__controllable:
            self.__controller = CameraController(self.__camera, self.__pid_x, self.__pid_y)

        self.__batch_id = self.__detector.register_frame_source(lambda : self.__camera.get_latest_frame())

        self.__is_ready_flag.set()

    def __update(self):
        self.__async_init()

        while True:
            frame = self.__camera.get_latest_frame()

            if frame is None: continue

            frame = frame.copy()

            boxes, weights = self.__detector.get_detections(self.__batch_id)

            draw_detection_boxes(frame, boxes, weights)

            x_error = 0
            y_error = 0
            if len(weights) != 0:
                focus_x, focus_y = calculate_target_position(boxes, weights)

                cv2.rectangle(frame, (focus_x - 5, focus_y - 5), (focus_x + 5, focus_y + 5), (255, 0, 0), 2)
                x_error = 2 * (focus_x - (frame.shape[1] / 2)) / frame.shape[1]
                y_error = 2 * ((frame.shape[0] / 2) - focus_y) / frame.shape[0]

            if self.__controllable:
                self.__controller.set_error(x_error, y_error)

            with self.__detections_lock:
                self.__latest_detections = zip(boxes, weights)

            with self.__frame_lock:
                self.__latest_frame = frame

    def get_latest_frame(self):
        if not self.__is_ready_flag.is_set(): return None
        return self.__camera.get_latest_frame()

    def get_latest_detections(self):
        if not self.__is_ready_flag.is_set(): return None
        with self.__detections_lock:
            return self.__latest_detections

    def get_latest_detections_frame(self):
        if not self.__is_ready_flag.is_set(): return None
        with self.__frame_lock:
            return self.__latest_frame
