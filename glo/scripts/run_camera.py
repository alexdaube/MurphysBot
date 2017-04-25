import cv2

from common.vision.camera import Camera

if __name__ == '__main__':
    camera = Camera(-1)
    camera.start()

    while True:
        frame = camera.get_current_frame()
        cv2.imshow('video', frame)
        cv2.waitKey(1)

    cv2.destroyAllWindows()
