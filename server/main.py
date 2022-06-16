import cv2
from threading import Thread
from Camera import Camera
from CameraController import CameraController
from PersonDetector import PersonDetector
from dotenv import dotenv_values
from PIL import Image
from flask import Flask, Response
from io import BytesIO
from os.path import abspath
from CameraSystem import SystemConfig, CameraSystem


def main():
    config = dotenv_values(".env")

    pid_x = (0.5, 0.01, 0.02)
    pid_y = (0.3, 0.01, 0)

    cams = [
        CameraSystem({ 'address': config["CAM1"], 'port': config["CAM1_PORT"], 'user': config["CAM1_USER"], 'password': config["CAM1_PASS"], 'pid_x': pid_x, 'pid_y': pid_y}),
        CameraSystem({ 'address': config["CAM2"], 'port': config["CAM2_PORT"], 'user': config["CAM2_USER"], 'password': config["CAM2_PASS"], 'pid_x': pid_x, 'pid_y': pid_y}),
        CameraSystem({ 'address': config["CAM3"], 'port': config["CAM3_PORT"], 'user': config["CAM3_USER"], 'password': config["CAM3_PASS"], 'pid_x': pid_x, 'pid_y': pid_y}),
        CameraSystem({ 'address': config["CAM5"], 'port': config["CAM5_PORT"], 'user': config["CAM5_USER"], 'password': config["CAM5_PASS"], 'pid_x': pid_x, 'pid_y': pid_y}),
    ]
    app = Flask("server", root_path=abspath("./"))

    def generate_responses(frame_function):
        while True:
            _, encoded_frame = cv2.imencode('.JPEG', frame_function())
            content = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + encoded_frame.tobytes() + b'\r\n\r\n'
            yield (content)

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

    app.run("0.0.0.0", 8080, debug=False)

if __name__ == "__main__":
    main()
