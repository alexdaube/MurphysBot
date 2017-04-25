import cv2


class DummyCamera:
    def __init__(self, image):
        self.image = image

    def start(self):
        pass

    def stop(self):
        pass

    def get_current_frame(self):
        return cv2.imread(self.image)

    def get_high_res_caps(self, num):
        return [self.get_current_frame() for i in range(0, num)]
