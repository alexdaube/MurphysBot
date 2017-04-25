import logging


class ColoredFormatter(logging.Formatter):
    RED = '\033[0;31m%s\033[0m'
    GREEN = '\033[0;32m%s\033[0m'
    YELLOW = '\033[1;33m%s\033[0m'
    LIGHT_BLUE = '\033[1;34m%s\033[0m'
    RESET = '\033[0m%s\033[0m'
    GREY = '\033[0;37m%s\033[0m'

    def format(self, record):
        if record.levelno == logging.WARNING:
            record.name = self.GREY % record.name
            record.levelname = self.YELLOW % record.levelname
            record.msg = self.YELLOW % record.msg
        elif record.levelno == logging.ERROR:
            record.name = self.GREY % record.name
            record.levelname = self.RED % record.levelname
            record.msg = self.RED % record.msg
        elif record.levelno == logging.CRITICAL:
            record.name = self.GREY % record.name
            record.levelname = self.RED % record.levelname
            record.msg = self.RED % record.msg
        elif record.levelno == logging.INFO:
            record.name = self.GREY % record.name
            record.levelname = self.LIGHT_BLUE % record.levelname
            record.msg = self.LIGHT_BLUE % record.msg
        elif record.levelno == logging.DEBUG:
            record.name = self.GREY % record.name
            record.levelname = self.GREEN % record.levelname
            record.msg = self.GREEN % record.msg
        else:
            record.name = self.RESET % record.name
            record.levelname = self.RESET % record.levelname
            record.msg = self.RESET % record.msg
        return logging.Formatter.format(self, record)
