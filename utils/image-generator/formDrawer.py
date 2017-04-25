#!/usr/bin/python2
# -*- coding: utf-8 -*-
import math
from PyQt4 import QtCore

from form import Point


class PointDrawer(object):
    def draw_point(self, point, painter):
        qpoint = QtCore.QPoint(point.x, point.y)
        painter.drawEllipse(qpoint, 5, 5);


class FormDrawerFactory(object):
    point_drawer = PointDrawer()

    def create_form_drawer(self, form):
        form_type = form.form_type
        if form_type is "Triangle":
            return PolygonDrawer(form, self.point_drawer)
        elif form_type is "Carre":
            return PolygonDrawer(form, self.point_drawer)
        elif form_type is "Pentagone":
            return PolygonDrawer(form, self.point_drawer)
        elif form_type is "Cercle":
            return CircleDrawer(form, self.point_drawer)
        else:
            return None


class PolygonDrawer(object):
    polygon = None
    point_drawer = None

    def __init__(self, polygon, point_drawer):
        self.polygon = polygon
        self.point_drawer = point_drawer

    def draw_form(self, painter):
        first_point = None
        previous_point = None
        for point in self.polygon.descriptor_points:
            if first_point is None:
                first_point = point
            if previous_point is not None:
                self.draw_line(previous_point, point, painter)
            self.point_drawer.draw_point(point, painter)
            previous_point = point
        if len(self.polygon.descriptor_points) is self.polygon.form_descriptor_point_amount:
            self.draw_line(first_point, previous_point, painter)

    def draw_line(self, point1, point2, painter):
        painter.drawLine(point1.x, point1.y, point2.x, point2.y)


class CircleDrawer(object):
    def __init__(self, polygon, point_drawer):
        self.polygon = polygon
        self.point_drawer = point_drawer

    def draw_form(self, painter):
        first_point = None
        previous_point = None
        for point in self.polygon.descriptor_points:
            if first_point is None:
                first_point = point
            self.point_drawer.draw_point(point, painter)
            previous_point = point
        if len(self.polygon.descriptor_points) is self.polygon.form_descriptor_point_amount:
            center_point = Point()
            dx = previous_point.x - first_point.x
            center_point.x = first_point.x + dx / 2
            dy = previous_point.y - first_point.y
            center_point.y = first_point.y + dy / 2
            qpoint = QtCore.QPoint(center_point.x, center_point.y)
            r = math.sqrt(math.pow((dx / 2), 2) + math.pow((dy / 2), 2))
            painter.drawEllipse(qpoint, r, r)
