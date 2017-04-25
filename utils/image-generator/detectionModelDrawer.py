#!/usr/bin/python2
# -*- coding: utf-8 -*-
from formDrawer import FormDrawerFactory


class DetectionModelQPainterDrawer(object):
    form_drawer_factory = FormDrawerFactory()

    def draw_detection_model(self, painter, detection_model):
        forms = detection_model.get_forms()
        for form in forms:
            form_drawer = self.form_drawer_factory.create_form_drawer(form)
            form_drawer.draw_form(painter)
