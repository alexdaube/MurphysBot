import time
from threading import Thread

import cv2


class Camera:
    FPS = 30
    WAIT_TIME = 1000

    def __init__(self, camera_number):
        self.camera_number = camera_number
        self.video_capture = cv2.VideoCapture(camera_number)
        self.video_capture.set(cv2.CAP_PROP_FPS, self.FPS)
        self.video_capture.set(cv2.CAP_PROP_BRIGHTNESS, 0.60)
        self.current_frame = self.video_capture.read()[1]
        self.high_res_pics = []
        self._running = False
        self.last_time = 0
        self._is_high_res = False
        self._thread = Thread(target=self._update_frame, args=())
        self._thread.start()

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    def _update_frame(self):
        self._running = True
        self.last_time = self._now()
        while self._running:
            if self._elapsed_time() > self.WAIT_TIME / self.FPS:
                self.video_capture.grab()
                self.last_time = self._now()

    def _elapsed_time(self):
        now = self._now()
        return int(round(now - self.last_time))

    @staticmethod
    def _now():
        return int(round(time.time() * 1000))

    def get_current_frame(self):
        self._wait_next_frame()
        return self.video_capture.retrieve()[1]

    def _wait_next_frame(self):
        diff = self._elapsed_time()
        sleep_time = (self.WAIT_TIME / self.FPS) - diff
        if 0 < sleep_time:
            time.sleep(sleep_time / self.WAIT_TIME)
