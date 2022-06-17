from copy import deepcopy

import torch
from threading import Thread, Lock, Event, local

class PersonDetector:

    def __init__(self):
        self.__initial_frame = False
        self.__latest_frame = None
        self.__boxes_c = []
        self.__weights_c = []

        self.__lock = Lock()
        self.__stop_flag = Event()

        self.__model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

        self.__thread = Thread(target=self.__update)
        self.__thread.start()

    def stop(self):
        self.__stop_flag.set()
        self.__thread.join()

    def get_detections(self, frame):
        with self.__lock:
            self.__latest_frame = frame
            return ([deepcopy(box) for box in self.__boxes_c], [deepcopy(weight) for weight in self.__weights_c])

    def __update(self):
        data = local()
        while True:
            if self.__stop_flag.is_set():
                break
            with self.__lock:
                if self.__latest_frame is None: continue
                data.frame = self.__latest_frame

            detections = self.__model(data.frame).pandas().xyxy[0]
            people_detected = detections[detections['class'] == 0]
            x = people_detected['xmin'].tolist()
            y = people_detected['ymin'].tolist()
            w = (people_detected['xmax'] - people_detected['xmin']).tolist()
            h = (people_detected['ymax'] - people_detected['ymin']).tolist()
            with self.__lock:
                self.__boxes_c = list(zip(x, y, w, h))
                self.__weights_c = people_detected['confidence'].tolist()
