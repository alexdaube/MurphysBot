import logging
import re


class QtHandler(logging.Handler):
    def __init__(self, queue):
        logging.Handler.__init__(self)
        self.queue = queue

    def emit(self, record):
        level = re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', '%s' % record.levelname)
        record = self.format(record)
        if record:
            message = re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', '%s\n' % record)
            self.queue.put((level, message))
