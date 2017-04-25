from threading import Thread

import cv2


class CameraRetrieve:
    FPS = 30

    def __init__(self, camera_number):
        self.camera_number = camera_number
        self.video_capture = cv2.VideoCapture(camera_number)
        self.video_capture.set(cv2.CAP_PROP_FPS, self.FPS)
        self.current_frame = self.video_capture.read()[1]
        self._running = False
        self.last_time = 0
        self._thread = Thread(target=self._update_frame, args=())
        self._thread.start()

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    def _update_frame(self):
        self._running = True
        while self._running:
            self.current_frame = self.video_capture.read()[1]

    def get_current_frame(self):
        return self.current_frame
