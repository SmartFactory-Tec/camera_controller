import cv2
import signal
import atexit
from flask import Blueprint, g, Response, jsonify
from camera_server.api.Camera import Camera
from camera_server.api.CameraSystem import CameraSystem
from camera_server.api.PersonDetector import PersonDetector

bp = Blueprint('camera', __name__, url_prefix='/api')

cameras = {}


def generate_responses(frame_function):
    while True:
        _, encoded_frame = cv2.imencode('.JPEG', frame_function())
        content = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + encoded_frame.tobytes() + b'\r\n\r\n'
        yield (content)


@bp.record
def initialize_cameras(setup_state):
    config = setup_state.app.config

    default = config["cameras"]["default"]

    detector = PersonDetector()

    for slug, cam in config["cameras"].items():
        if slug == 'default': continue
        name = cam["name"]
        controllable = cam["controllable"] if "controllable" in cam else default["controllable"]
        pid_x = cam["pid_x"] if "pid_x" in cam else default["pid_x"]
        pid_y = cam["pid_y"] if "pid_y" in cam else default["pid_y"]
        enable_detection = cam["enable_detection"] if "enable_detection" in cam else default["enable_detection"]

        pid_x = (float(pid_x["p"]), float(pid_x["i"]), float(pid_x["d"]))
        pid_y = (float(pid_y["p"]), float(pid_y["i"]), float(pid_y["d"]))



        if 'id' in cam:
            camera_id = cam['id']
            cameras[slug] = {
                'name': name,
                'detection_enabled': enable_detection,
                'pid_x': pid_x,
                'pid_y': pid_y,
                'controllable': controllable,
                'system': CameraSystem(pid_x=pid_x, pid_y=pid_y, id=camera_id,
                                       controllable=controllable, detector=detector),
            }
        else:
            user = cam["user"]
            password = cam["password"]
            address = cam["address"]
            port = cam["port"]
            cameras[slug] = {
                'name': name,
                'detection_enabled': enable_detection,
                'pid_x': pid_x,
                'pid_y': pid_y,
                'controllable': controllable,
                'system': CameraSystem(user=user, password=password, address=address, port=port,
                                       pid_x=pid_x, pid_y=pid_y, controllable=controllable,
                                       detector=detector),
            }

@bp.route('/cameras')
def camera_listing():
    camera_listing = []
    for slug, cam in cameras.items():
        camera_listing.append({
            'name': cam['name'],
            'slug': slug,
        })
    return jsonify(camera_listing)

@bp.route('/camera/<camera_id>')
def camera_info(camera_id):
    try:
        camera = cameras[camera_id]
        camera_info = {
            'slug': camera_id,
            'name': camera['name'],
            'detection_enabled': camera['detection_enabled'],
        }
        return jsonify(camera_info)
    except KeyError:
        return Response("Camera not found", status=404)


@bp.route('/camera/<camera_id>/video_feed')
def video_feed(camera_id):
    try:
        camera = cameras[camera_id]

        latest_frame = camera['system'].get_latest_frame()

        if latest_frame is None:
            return Response(status=503)

        return Response(generate_responses(cameras[camera_id]['system'].get_latest_frame),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    except KeyError:
        return Response("Camera not found", status=404)


@bp.route('/camera/<camera_id>/detections/video_feed')
def detections_video_feed(camera_id):
    try:
        camera = cameras[camera_id]

        latest_detections = camera['system'].get_latest_detections_frame()

        if latest_detections is None:
            return Response(status=503)

        return Response(generate_responses(cameras[camera_id]['system'].get_latest_detections_frame),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    except KeyError:
        return Response("Camera not found", status=404)
    except RuntimeError:
        return Response("Detector for this camera disabled", status=404)
