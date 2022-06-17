import signal
import cv2
from dotenv import dotenv_values
from flask import Flask, Response
from os.path import abspath
from CameraSystem import CameraSystem


def handle_kb_interrupt(sig, frame):
    for cam in cams:
        cam.stop()


def generate_responses(frame_function):
    while True:
        _, encoded_frame = cv2.imencode('.JPEG', frame_function())
        content = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + encoded_frame.tobytes() + b'\r\n\r\n'
        yield (content)

app = Flask("server")

config = dotenv_values(".env")
pid_x = (0.45, 0.01, 0.01)
pid_y = (0.3, 0.01, 0)
cams = [
    CameraSystem({'image_scale': float(config["IMAGE_SCALE"]), 'address': config["CAM1"], 'port': config["CAM1_PORT"], 'user': config["CAM1_USER"],
                  'password': config["CAM1_PASS"], 'pid_x': pid_x, 'pid_y': pid_y}),
    CameraSystem({'image_scale': float(config["IMAGE_SCALE"]), 'address': config["CAM2"], 'port': config["CAM2_PORT"], 'user': config["CAM2_USER"],
                  'password': config["CAM2_PASS"], 'pid_x': pid_x, 'pid_y': pid_y}),
    CameraSystem({'image_scale': float(config["IMAGE_SCALE"]), 'address': config["CAM3"], 'port': config["CAM3_PORT"], 'user': config["CAM3_USER"],
                  'password': config["CAM3_PASS"], 'pid_x': pid_x, 'pid_y': pid_y}),
    CameraSystem({'image_scale': float(config["IMAGE_SCALE"]), 'address': config["CAM5"], 'port': config["CAM5_PORT"], 'user': config["CAM5_USER"],
                  'password': config["CAM5_PASS"], 'pid_x': pid_x, 'pid_y': pid_y}),
]

signal.signal(signal.SIGINT, handle_kb_interrupt)
signal.signal(signal.SIGHUP, handle_kb_interrupt)

@app.route('/')
def home():
    return Response("Hello world!")

@app.route('/camera/<int:camera_id>')
def camera_info(camera_id):
    if camera_id >= len(cams) or camera_id < 0 == None:
        return Response(status=404)
    return Response()


@app.route('/camera/<int:camera_id>/video_feed')
def video_feed(camera_id):
    if camera_id >= len(cams) or camera_id < 0 == None:
        return Response(status=404)
    return Response(generate_responses(cams[camera_id].get_latest_frame),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/camera/<int:camera_id>/detections/video_feed')
def people_video_feed(camera_id):
    # If the id doesn't match an index in the camera array, return a not found code.
    if camera_id >= len(cams) or camera_id < 0 == None:
        return Response(status=404)
    latest_detections = cams[camera_id].get_latest_detections_frame()
    # If frame is None, then the camera system isn't ready to stream.
    if latest_detections is None:
        return Response(status=503)
    # Encode the frame
    return Response(generate_responses(cams[camera_id].get_latest_detections_frame),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
