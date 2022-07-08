from threading import Event, Thread, Lock
from time import time_ns
from camera_server.api import Camera


class CameraController:
    def __init__(self, camera, x_pid, y_pid, x_deadzone = 0.2, y_deadzone = 0.2):
        self.__x_error = 0
        self.__y_error = 0

        self.__camera = camera

        self.__x_pid = x_pid
        self.__y_pid = y_pid
        self.__x_deadzone = x_deadzone
        self.__y_deadzone = y_deadzone

        self.__thread = Thread(target=self.__update)
        self.__thread.daemon = True
        self.__thread.start()

    def set_error(self, x_error, y_error):
        self.__x_error = x_error
        self.__y_error = y_error

    def __update(self):
        x_int = 0
        x_prev = 0
        y_int = 0
        y_prev = 0
        prev_x_exec = time_ns()
        prev_y_exec = time_ns()
        while True:
            x_timestep = time_ns() - prev_x_exec

            if x_timestep == 0: continue

            x_int += self.__x_error * x_timestep / 1_000_000_000
            x_delta = (self.__x_error - x_prev) * 1_000_000_000 / x_timestep


            x_correction = self.__x_error * self.__x_pid[0] \
                                + x_int * self.__x_pid[1] \
                                + x_delta * self.__x_pid[2]



            x_prev = self.__x_error
            y_prev = self.__y_error

            prev_x_exec = time_ns()
            if abs(x_correction) > self.__x_deadzone:
                self.__camera.set_speed(x_correction, 0)
                prev_y_exec = time_ns()
                continue

            # Start counting time for y only when X has minimal error
            y_timestep = time_ns() - prev_y_exec

            if y_timestep == 0: continue

            y_int += self.__y_error * y_timestep / 1_000_000_000
            y_delta = (self.__y_error - y_prev) * 1_000_000_000 / y_timestep

            y_correction = self.__y_error * self.__y_pid[0] \
                           + y_int * self.__y_pid[1] \
                           + y_delta * self.__y_pid[2]

            prev_y_exec = time_ns()

            if abs(y_correction) > self.__y_deadzone:
                self.__camera.set_speed(0, y_correction)
            else:
                self.__camera.stop_movement()
