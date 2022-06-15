from threading import Event, Thread
from time import time_ns
from Camera import Camera


class CameraController:
    def __init__(self, camera: Camera, x_pid: tuple[float, float, float], y_pid: tuple[float, float, float], x_deadzone = 0.2, y_deadzone = 0.2):
        self.__x_error = 0
        self.__y_error = 0
        self.__stop_flag = Event()
        self.__camera = camera
        self.__x_pid = x_pid
        self.__y_pid = y_pid
        self.__x_deadzone = x_deadzone
        self.__y_deadzone = y_deadzone
        self.__thread = Thread(target=self.__update)
        self.__thread.start()

    def stop(self):
        self.__stop_flag.set()
        self.__thread.join()

    def set_error(self, x_error, y_error):
        self.__x_error = x_error
        self.__y_error = y_error

    def __update(self):
        x_int = 0
        x_prev = 0
        y_int = 0
        y_prev = 0
        prev_exec = time_ns()
        while not self.__stop_flag.is_set():
            timestep = time_ns() - prev_exec

            x_int += self.__x_error * timestep / 1_000_000_000
            x_delta = (self.__x_error - x_prev) * 1_000_000_000 / timestep

            y_int += self.__y_error * timestep / 1_000_000_000
            y_delta = (self.__y_error - y_prev) * 1_000_000_000 / timestep

            x_correction = self.__x_error * self.__x_pid[0] \
                                + x_int * self.__x_pid[1] \
                                + x_delta * self.__x_pid[2]

            y_correction = self.__y_error * self.__y_pid[0] \
                           + y_int * self.__y_pid[1] \
                           + y_delta * self.__y_pid[2]

            x_prev = self.__x_error
            y_prev = self.__y_error
            prev_exec = time_ns()
            if abs(x_correction) > self.__x_deadzone:
                self.__camera.set_speed(x_correction, 0)
            elif abs(y_correction) > self.__y_deadzone:
                self.__camera.set_speed(0, y_correction)
            else:
                self.__camera.stop_movement()