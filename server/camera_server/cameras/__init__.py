import cv2
import signal
import atexit
from flask import Blueprint, g, Response, jsonify
from camera_server.cameras.Camera import Camera
from camera_server.cameras.CameraSystem import CameraSystem

bp = Blueprint('camera', __name__)

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

    for slug, cam in config["cameras"].items():
        if slug == 'default': continue
        name = cam["name"]
        controllable = cam["controllable"] if "controllable" in cam else default["controllable"]
        pid_x = cam["pid_x"] if "pid_x" in cam else default["pid_x"]
        pid_y = cam["pid_y"] if "pid_y" in cam else default["pid_y"]
        scale = cam["scale"] if "scale" in cam else default["scale"]

        pid_x = (float(pid_x["p"]), float(pid_x["i"]), float(pid_x["d"]))
        pid_y = (float(pid_y["p"]), float(pid_y["i"]), float(pid_y["d"]))

        if 'id' in cam:
            camera_id = cam['id']
            cameras[slug] = {
                'name': name,
                'system': CameraSystem(pid_x=pid_x, pid_y=pid_y, image_scale=scale, id=camera_id,
                                       controllable=controllable),
            }
        else:
            user = cam["user"]
            password = cam["password"]
            address = cam["address"]
            port = cam["port"]
            cameras[slug] = {
                'name': name,
                'system': CameraSystem(user=user, password=password, address=address, port=port, image_scale=scale,
                                       pid_x=pid_x,
                                       pid_y=pid_y, controllable=controllable),
            }


@bp.route('/cameras')
def home():
    camera_listing = []
    for slug, cam in cameras.items():
        camera_listing.append({
            'name': cam['name'],
            'slug': slug,
        })
    return jsonify(camera_listing)


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
def people_video_feed(camera_id):
    try:
        camera = cameras[camera_id]

        latest_detections = camera['system'].get_latest_detections_frame()

        if latest_detections is None:
            return Response(status=503)

        return Response(generate_responses(cameras[camera_id]['system'].get_latest_detections_frame),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    except KeyError:
        return Response("Camera not found", status=404)
