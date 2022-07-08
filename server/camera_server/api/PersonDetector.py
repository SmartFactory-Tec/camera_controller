from copy import deepcopy
from typing import Callable

import cv2
import torch
from threading import Thread, Lock, Event, local
import numpy as np

class PersonDetector:

    def __init__(self):
        self.__initial_frames = False
        self.__boxes_c = []
        self.__weights_c = []

        self.__detections_lock = Lock()

        self.__model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

        self.__frame_sources: [Callable[[], np.ndarray | None]] = []

        self.__thread = Thread(target=self.__update)
        self.__thread.daemon = True
        self.__thread.start()

    def register_frame_source(self, frame_source):
        self.__frame_sources.append(frame_source)
        self.__boxes_c.append([])
        self.__weights_c.append([])
        return len(self.__frame_sources) - 1

    def get_detections(self, id):
        with self.__detections_lock:
            boxes = self.__boxes_c[id]
            weights = self.__weights_c[id]
            return ([deepcopy(box) for box in boxes], [deepcopy(weight) for weight in weights])

    def __update(self):
        data = local()
        while True:
            # Don't do anything until there are frame sources
            if len(self.__frame_sources) == 0:
                continue
            frames = []

            for source in self.__frame_sources:
                frame = source()

                if frame is not None:
                    resized_frame = cv2.resize(frame, dsize=(int(frame.shape[1] * 0.4), int(frame.shape[0] * 0.4)),
                                               interpolation=cv2.INTER_AREA)
                    frames.append(resized_frame)

            detections = self.__model(frames).pandas().xyxy

            for idx, detection in enumerate(detections):
                people_detected = detection[detection['class'] == 0]
                x = people_detected['xmin'].tolist()
                y = people_detected['ymin'].tolist()
                w = (people_detected['xmax'] - people_detected['xmin']).tolist()
                h = (people_detected['ymax'] - people_detected['ymin']).tolist()

                for box_idx  in range(len(x)):
                    x[box_idx] = int(x[box_idx] / 0.4)
                    y[box_idx] = int(y[box_idx] / 0.4)
                    w[box_idx] = int(w[box_idx] / 0.4)
                    h[box_idx] = int(h[box_idx] / 0.4)

                with self.__detections_lock:
                    self.__boxes_c[idx] = list(zip(x, y, w, h))
                    self.__weights_c[idx] = people_detected['confidence'].tolist()
