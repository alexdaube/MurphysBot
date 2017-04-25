import logging


class HttpHandler(logging.Handler):
    def __init__(self, client):
        logging.Handler.__init__(self)
        self.client = client

    def emit(self, record):
        try:
            lvl = record.levelno
            msg = self.format(record)
            self.client.send_log({'log': (lvl, msg)})
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
