import cv2
from threading import Thread
from Camera import Camera
from CameraController import CameraController
from PersonDetector import PersonDetector
from dotenv import dotenv_values
from PIL import Image
from flask import Flask, Response
from io import BytesIO


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


def process_frame(frame, controller, detector):
    scale = 0.4
    resized_frame = cv2.resize(frame, dsize=(int(frame.shape[1] * scale), int(frame.shape[0] * scale)),
                               interpolation=cv2.INTER_AREA)

    boxes, weights = detector.get_detections(resized_frame)

    for idx, box in enumerate(boxes):
        x, y, w, h = box
        x = int(x / scale)
        y = int(y / scale)
        w = int(w / scale)
        h = int(h / scale)
        boxes[idx] = (x, y, w, h)

    draw_detection_boxes(frame, boxes, weights)

    x_error = 0
    y_error = 0
    if len(weights) != 0:
        focus_x, focus_y = calculate_target_position(boxes, weights)

        cv2.rectangle(frame, (focus_x - 5, focus_y - 5), (focus_x + 5, focus_y + 5), (255, 0, 0), 2)
        x_error = 2 * (focus_x - (frame.shape[1] / 2)) / frame.shape[1]
        y_error = 2 * ((frame.shape[0] / 2) - focus_y) / frame.shape[0]

    controller.set_error(x_error, y_error)


def gen(latest_frames, id):
    while True:
        # get camera frame
        _, encoded_frame = cv2.imencode('.JPEG', latest_frames[id])
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + encoded_frame.tobytes() + b'\r\n\r\n')


def main():
    config = dotenv_values(".env")

    cams = [
        Camera(config["CAM1"], int(config["CAM1_PORT"]), config["CAM1_USER"], config["CAM1_PASS"]),
        Camera(config["CAM2"], int(config["CAM2_PORT"]), config["CAM2_USER"], config["CAM2_PASS"]),
        Camera(config["CAM3"], int(config["CAM3_PORT"]), config["CAM3_USER"], config["CAM3_PASS"]),
        Camera(config["CAM5"], int(config["CAM5_PORT"]), config["CAM5_USER"], config["CAM5_PASS"]),
    ]

    latest_frame = [
        None,
        None,
        None,
        None
    ]

    app = Flask("server")

    @app.route('/video_feed/<id>')
    def video_feed(id):
        if not id.isdigit() or int(id) >= len(cams) or int(id) < 0 == None:
            return Response(status=404)
        if latest_frame[int(id)] is None:
            return Response(status=503)

        return Response(gen(latest_frame, int(id)),
                        mimetype='multipart/x-mixed-replace;boundary=frame')

    flask_thread = Thread(target=lambda: app.run("0.0.0.0", 8080, debug=False))
    flask_thread.daemon = True
    flask_thread.start()

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

    print("Ready")

    while True:
        for idx, (cam, detector, controller) in enumerate(zip(cams, detectors, controllers)):
            frame = cam.read_frame()

            if frame is None: continue

            process_frame(frame, controller, detector)

            latest_frame[idx] = frame

    for cam, detector, controller in zip(cams, detectors, controllers):
        controller.stop()
        cam.stop_movement()
        cam.stop()
        detector.stop()


if __name__ == "__main__":
    main()
