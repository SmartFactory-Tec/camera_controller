from onvif import ONVIFCamera
from os.path import abspath
from threading import Thread, Lock, Event, Condition
import cv2
import re


class Camera:
    def __init__(self, address=None, port=None, user=None,
                 password=None, id=None):
        if id is not None:
            self.__stream = cv2.VideoCapture(id)
            self.__onvif_camera = None
        else:
            self.__onvif_camera = ONVIFCamera(address, port, user, password)

            self.__media = self.__onvif_camera.create_media_service()
            self.__ptz = self.__onvif_camera.create_ptz_service()
            self.__media_profile = self.__media.GetProfiles()[0]

            request = self.__ptz.create_type('GetConfigurations')

            token = self.__ptz.GetConfigurations(request)[0].token

            request = self.__ptz.create_type('GetConfigurationOptions')

            request.ConfigurationToken = token

            print(self.__ptz.GetStatus({"ProfileToken": self.__media_profile.token}))

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

        self.__frame_lock = Lock()
        self.__frame_requested_event = Event()
        self.__frame_available_condition = Condition()

        self.__thread = Thread(target=self.__update)
        self.__thread.daemon = True
        self.__thread.start()

    def __update(self):
        while True:
            self.__stream.grab()
            if self.__frame_requested_event.is_set():
                ret, frame = self.__stream.retrieve()
                if ret:
                    with self.__frame_available_condition:
                        self.__frame_c = frame
                        self.__frame_requested_event.clear()
                        self.__frame_available_condition.notify_all()

    def get_latest_frame(self):
        self.__frame_requested_event.set()
        with self.__frame_available_condition:
            self.__frame_available_condition.wait()
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
        # self.__ptz.RelativeMove(request)

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
