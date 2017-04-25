#!/usr/bin/python2
# -*- coding: utf-8 -*-
import cv2


class CVImageCaptor:
    def __init__(self):
        self.camera_port = 1
        self.correction_frames_count = 30

    def set_correction_frames_amount(self, amount):
        self.correction_frames_count = amount

    def set_camera_port(self, camera):
        self.camera_port = camera

    @staticmethod
    def get_camera_count():
        count = 0
        pcount = -1
        while count != pcount:
            pcount = count
            try:
                cv2.VideoCapture(count)
                count += 1
                break
            except:
                pass
        return count

    def capture_image(self):
        camera = cv2.VideoCapture(self.camera_port)
        for i in xrange(self.correction_frames_count):
            camera.read()
        print("Taking image...")
        value, image_capture = camera.read()
        cv_rgb_image = cv2.cvtColor(image_capture, cv2.cv.CV_BGR2RGB)
        camera.release()
        return cv_rgb_image
