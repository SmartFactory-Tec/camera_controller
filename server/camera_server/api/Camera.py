from onvif import ONVIFCamera
from os.path import abspath
from threading import Thread, Lock, Event
import cv2
import re


class Camera:
    def __init__(self, address: str | None = None, port: int | None = None, user: str | None = None,
                 password: str | None = None, id: int | None = None):
        if id is not None:
            self.__stream = cv2.VideoCapture()
            self.__onvif_camera = None
        else:
            self.__onvif_camera = ONVIFCamera(address, port, user, password)

            self.__media = self.__onvif_camera.create_media_service()
            self.__ptz = self.__onvif_camera.create_ptz_service()
            self.__media_profile = self.__media.GetProfiles()[0]

            uri_request = self.__media.create_type('GetStreamUri')
            uri_request.StreamSetup = {
                'Stream': 'RTP-Multicast',
                'Transport': {
                    'Protocol': 'TCP'
                }
            }
            uri_request.ProfileToken = self.__media_profile.token

            stream_uri = self.__media.GetStreamUri(uri_request).Uri

            uri_front = re.search(r'://(.*)', stream_uri).groups()[0]

            # Add the user and password for the stream
            self.__stream_uri = 'rtsp://' + user + ':' + password + '@' + uri_front

            self.__stream = cv2.VideoCapture(self.__stream_uri)

        self.__is_ready_flag = Event()
        self.__frame_lock = Lock()

        self.__thread = Thread(target=self.__update)
        self.__thread.daemon = True
        self.__thread.start()

    def __update(self):
        while True:
            ret, frame = self.__stream.read()
            if ret:
                with self.__frame_lock:
                    self.__frame_c = frame
                    self.__is_ready_flag.set()

    def is_ready(self):
        return self.__is_ready_flag.is_set()

    def get_latest_frame(self):
        self.__is_ready_flag.wait()
        with self.__frame_lock:
            return self.__frame_c

    def move(self, pan_offset: float, tilt_offset: float):
        request = self.__ptz.create_type('RelativeMove')
        request.ProfileToken = self.__media_profile.token
        request.Translation = {
            'PanTilt': {
                'x': pan_offset,
                'y': tilt_offset,
            },

        }
        request.Speed = {
            'PanTilt': {
                'x': 0.5,
                'y': 0.5,
            }
        }
        self.__ptz.RelativeMove(request)

    def set_speed(self, pan: float, tilt: float):
        request = self.__ptz.create_type('ContinuousMove')
        request.ProfileToken = self.__media_profile.token
        pan = pan if pan < 1 else 1
        pan = pan if pan > -1 else -1
        tilt = tilt if tilt < 1 else 1
        tilt = tilt if tilt > -1 else -1
        request.Velocity = {
            'PanTilt': {
                'x': pan,
                'y': tilt,
                'space': 'http://www.onvif.org/ver10/tptz/PanTiltSpaces/PositionGenericSpace',
            },
        }
        self.__ptz.ContinuousMove(request)

    def stop_movement(self):
        request = self.__ptz.create_type('Stop')
        request.ProfileToken = self.__media_profile.token
        self.__ptz.Stop(request)
