#!/usr/bin/python2
# -*- coding: utf-8 -*-
import sys
import datetime
from PyQt4 import QtGui, QtCore

from detectionModelDrawer import DetectionModelQPainterDrawer
from imageCaptor import CVImageCaptor
from formSelectorQDialog import FormSelectorQDialog
from form import Point
import detectionModel


class ImageGeneratorMainWindow(QtGui.QMainWindow):
    image_captor = None
    detection_model_factory = None
    image_area = None
    image_pixmap = None
    image_label = None
    model = None
    model_drawer = None
    form_drawer = None
    current_adding_form = None

    def __init__(self, image_captor, detection_model_factory):
        super(ImageGeneratorMainWindow, self).__init__()
        self.detection_model_factory = detection_model_factory
        self.image_area = QtGui.QScrollArea()
        self.image_captor = image_captor
        self.init_ui()
        self.model_drawer = DetectionModelQPainterDrawer()

    def init_ui(self):
        self.setWindowTitle('Test image generator')
        self.resize(500, 350)
        self.init_menu()
        self.init_layout()
        self.show()

    def init_menu(self):
        exit_action = QtGui.QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit')
        exit_action.triggered.connect(self.close)
        menu = self.menuBar()
        file_menu = menu.addMenu('&File')
        file_menu.addAction(exit_action)

    def init_layout(self):
        main_layout = QtGui.QGridLayout()
        action_menu_layout = QtGui.QVBoxLayout()
        cwidget = QtGui.QWidget()
        cwidget.setLayout(main_layout)
        self.setCentralWidget(cwidget)
        action_menu_widget = QtGui.QWidget()
        action_menu_widget.setLayout(action_menu_layout)
        main_layout.addWidget(action_menu_widget, 1, 0)

        camera_selector = QtGui.QComboBox()
        for value in xrange(self.image_captor.get_camera_count()):
            camera_selector.addItem("Camera " + str(value))
        self.connect(camera_selector, QtCore.SIGNAL("currentIndexChanged(const int&)"), self.connect_camera_selection)
        action_menu_layout.addWidget(camera_selector)

        capture_image_button = QtGui.QPushButton("Capture", self)
        capture_image_button.clicked.connect(self.connect_capture_image)
        action_menu_layout.addWidget(capture_image_button)

        add_form_button = QtGui.QPushButton("Add form", self)
        add_form_button.clicked.connect(self.connect_add_form)
        action_menu_layout.addWidget(add_form_button)

        save_button = QtGui.QPushButton("Save Model and image", self)
        save_button.clicked.connect(self.connect_save_form_and_model)
        action_menu_layout.addWidget(save_button)

        self.image_area.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.image_area, 1, 1)

    def redraw_model(self):
        image_pixmap_display = self.image_pixmap.copy()
        image_pixmap_display
        painter = QtGui.QPainter(image_pixmap_display)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(0))
        painter.setPen(pen)
        self.model_drawer.draw_detection_model(painter, self.model)
        self.form_drawer.draw_form(painter)
        self.image_label.setPixmap(image_pixmap_display)
        del painter
        self.image_label.update()

    def connect_capture_image(self):
        cv_rgb_image = self.image_captor.capture_image()
        qt_image = QtGui.QImage(cv_rgb_image.data, cv_rgb_image.shape[1], cv_rgb_image.shape[0],
                                QtGui.QImage.Format_RGB888)
        self.image_pixmap = QtGui.QPixmap.fromImage(qt_image)
        image_pixmap_display = QtGui.QPixmap.fromImage(qt_image)
        self.image_label = QtGui.QLabel()
        self.image_label.setPixmap(image_pixmap_display)
        self.image_label.mousePressEvent = self.connect_image_click
        self.image_area.setWidget(self.image_label)
        self.model = detectionModel.DetectionModel()

    def connect_camera_selection(self, camera_port):
        self.image_captor.set_camera_port(camera_port)

    def connect_image_click(self, event):
        point = Point()
        point.x = event.pos().x()
        point.y = event.pos().y()
        if self.current_adding_form is not None:
            if self.current_adding_form.add_descriptor_point(point):
                self.model.add_form(self.current_adding_form)
                self.current_adding_form = None
        self.redraw_model()
        print ("mouse click on X:" + str(point.x) + " Y:" + str(point.y))

    def connect_add_form(self):
        value, form, self.form_drawer = FormSelectorQDialog.get_form_result()
        if value:
            self.current_adding_form = form

    def connect_save_form_and_model(self):
        now = datetime.datetime.now()
        filename = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "-" + str(now.hour) + str(
                now.minute) + str(now.second) + str(now.microsecond)
        myfile = QtCore.QFile(filename + ".png")
        self.image_pixmap.save(myfile, "PNG")
        model_exporter = self.detection_model_factory.create_detection_model_exporter()
        model_exporter.export_model_to_file(self.model, filename)


def main():
    app = QtGui.QApplication(sys.argv)
    image_captor = CVImageCaptor()
    detection_model_factory = detectionModel.DetectionModelFactory(detectionModel.EXPORTER_TYPE.JSON)
    w = ImageGeneratorMainWindow(image_captor, detection_model_factory)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
