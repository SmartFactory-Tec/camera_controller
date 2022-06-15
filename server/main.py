import cv2
from Camera import Camera
from CameraController import CameraController
from PersonDetector import PersonDetector
from dotenv import dotenv_values
from flask import Flask

app = Flask(__name__)

def calculate_target_position(boxes, weights):
    if len(boxes) == 0 or len(weights) == 0:
        raise ValueError("Arguments must be non zero-length lists!")
    if len(boxes) != len(weights):
        raise ValueError("Arguments' lengths should be the same!")

    target_x = 0
    target_y = 0
    weight_total = 0
    for box, weight in zip(boxes, weights):
        x, y, w, h = box

        weight_total += weight * weight

        target_x += (x + w / 2) * weight * weight
        target_y += (y + h / 2) * weight * weight

    target_x /= weight_total
    target_y /= weight_total

    return int(target_x), int(target_y)


def draw_detection_boxes(frame, boxes, weights):
    for idx, weight in enumerate(weights):
        x, y, w, h = boxes[idx]
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)

        if weight < 0.13:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        elif weight < 0.3:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (190, 30, 0), 2)
        if weight < 0.7:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 122, 255), 2)
        else:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


def main():
    config = dotenv_values(".env")

    cams = [
        Camera(config["CAM1"], int(config["CAM1_PORT"]), config["CAM1_USER"], config["CAM1_PASS"]),
        Camera(config["CAM2"], int(config["CAM2_PORT"]), config["CAM2_USER"], config["CAM2_PASS"]),
        Camera(config["CAM3"], int(config["CAM3_PORT"]), config["CAM3_USER"], config["CAM3_PASS"]),
        Camera(config["CAM5"], int(config["CAM5_PORT"]), config["CAM5_USER"], config["CAM5_PASS"]),
    ]

    detectors = [
        PersonDetector(),
        PersonDetector(),
        PersonDetector(),
        PersonDetector(),
    ]

    pid_x = (0.4, 0.001, 0.01)
    pid_y = (0.2, 0, 0)

    controllers = [
        CameraController(cams[0], pid_x, pid_y),
        CameraController(cams[1], pid_x, pid_y),
        CameraController(cams[2], pid_x, pid_y),
        CameraController(cams[3], pid_x, pid_y),
    ]

    while True:
        for idx, (cam, detector, controller) in enumerate(zip(cams, detectors, controllers)):
            frame = cam.read_frame()
            frame = cv2.resize(frame, dsize=(int(frame.shape[1] * .4), int(frame.shape[0] * .4)),
                               interpolation=cv2.INTER_AREA)

            if frame is None:
                continue

            boxes, weights = detector.get_detections(frame)

            draw_detection_boxes(frame, boxes, weights)

            x_error = 0
            y_error = 0
            if len(weights) != 0:
                focus_x, focus_y = calculate_target_position(boxes, weights)

                cv2.rectangle(frame, (focus_x - 5, focus_y - 5), (focus_x + 5, focus_y + 5), (255, 0, 0), 2)
                x_error = 2 * (focus_x - (frame.shape[1] / 2)) / frame.shape[1]
                y_error = 2 * ((frame.shape[0] / 2) - focus_y) / frame.shape[0]

            controller.set_error(x_error, y_error)
            cv2.imshow("cam{}".format(idx), frame)

        k = cv2.waitKey(1)

        if k == 27:
            break
    for cam, detector, controller in zip(cams, detectors, controllers):
        controller.stop()
        cam.stop_movement()
        cam.stop()
        detector.stop()


if __name__ == "__main__":
    main()
