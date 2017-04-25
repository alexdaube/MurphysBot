import logging
import sys

from common.logger.colored_formatter import ColoredFormatter
from common.logger.dynamic_file_handler import DynamicFileHandler
from common.logger.http_handler import HttpHandler
from common.logger.qt_handler import QtHandler

FILE_FORMAT = '[%(asctime)s] - %(name)-s : %(levelname)-s - %(message)-s - {%(pathname)s:%(lineno)d}'
FILE_DMT_FORMAT = '%Y-%m-%d %H:%M:%S'
FILE_MODE = 'a+'
FILE_LEVEL = logging.DEBUG
CONSOLE_FORMAT = '%(name)-12s: %(levelname)-8s -- %(message)s'
CONSOLE_LEVEL = logging.DEBUG
HTTP_FORMAT = '%(name)-4s: -- %(message)s'
HTTP_LEVEL = logging.DEBUG
QT_FORMAT = '%(name)-4s: %(levelname)-s -- %(message)s'
QT_LEVEL = logging.DEBUG
ROOT_LOGGER_LEVEL = logging.NOTSET
REQUESTS_LOGGER_LEVEL = logging.WARNING
URLLIB3_LOGGER_LEVEL = logging.WARNING
WERKZEUG_LOGGER_LEVEL = logging.WARNING
PYQT4_UIC_UIPARSER_LEVEL = logging.WARNING
PYQT4_UIC_PROPERTIES_LEVEL = logging.WARNING


def configure_root_logger(directory):
    root_logger = logging.getLogger("")
    root_logger.setLevel(ROOT_LOGGER_LEVEL)
    root_logger.propagate = 0

    file_handler = DynamicFileHandler(directory, FILE_MODE)
    file_handler.setLevel(FILE_LEVEL)
    file_formatter = logging.Formatter(FILE_FORMAT, FILE_DMT_FORMAT)
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(CONSOLE_LEVEL)
    console_handler.stream = sys.stdout
    console_formatter = ColoredFormatter(CONSOLE_FORMAT)
    console_handler.setFormatter(console_formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    logging.getLogger("requests").setLevel(REQUESTS_LOGGER_LEVEL)
    logging.getLogger("urllib3").setLevel(URLLIB3_LOGGER_LEVEL)
    logging.getLogger("werkzeug").setLevel(WERKZEUG_LOGGER_LEVEL)


def configure_http_logger(logger_name, client):
    http_logger = logging.getLogger(logger_name)
    http_handler = HttpHandler(client)
    http_handler.setLevel(HTTP_LEVEL)
    http_formatter = logging.Formatter(HTTP_FORMAT)
    http_handler.setFormatter(http_formatter)
    http_logger.addHandler(http_handler)


def configure_qt_logger(queue):
    root_logger = logging.getLogger("")
    qt_handler = QtHandler(queue)
    qt_handler.setLevel(QT_LEVEL)
    qt_formatter = logging.Formatter(QT_FORMAT)
    qt_handler.setFormatter(qt_formatter)
    root_logger.addHandler(qt_handler)


def set_qt_loggers_level():
    logging.getLogger("PyQt4.uic.uiparser").setLevel(PYQT4_UIC_UIPARSER_LEVEL)
    logging.getLogger("PyQt4.uic.properties").setLevel(PYQT4_UIC_PROPERTIES_LEVEL)