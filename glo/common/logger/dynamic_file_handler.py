import logging
import time


class DynamicFileHandler(logging.FileHandler):
    def __init__(self, directory, mode, delay=0):
        path = "./logs/{0}/{1}__log_file.log".format(directory, time.strftime("%Y_%m_%d__%H_%M_%S"))
        super(DynamicFileHandler, self).__init__(path, mode, delay=delay)
