#!/usr/bin/python2
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4 import QtCore

import form
from formDrawer import FormDrawerFactory


class FormSelectorQDialog(QtGui.QDialog):
    color_selector = None
    form_selector = None

    def __init__(self, parent=None):
        super(FormSelectorQDialog, self).__init__(parent)
        layout = QtGui.QVBoxLayout(self)

        self.form_selector = QtGui.QComboBox()
        for value in form.FORMS:
            self.form_selector.addItem(value)
        layout.addWidget(self.form_selector)

        self.color_selector = QtGui.QComboBox()
        for value in form.COLORS:
            self.color_selector.addItem(value)
        layout.addWidget(self.color_selector)
        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
                                         QtCore.Qt.Horizontal, self)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

    def get_color(self):
        return form.COLORS[self.color_selector.currentIndex()]

    def get_form(self):
        return form.FORMS[self.form_selector.currentIndex()]

    @staticmethod
    def get_form_result(parent=None):
        dialog = FormSelectorQDialog(parent)
        result = dialog.exec_()
        form_factory = form.FormFactory()
        my_form = form_factory.create_form(dialog.get_form(), dialog.get_color())
        form_drawer_factory = FormDrawerFactory()
        form_drawer = form_drawer_factory.create_form_drawer(my_form)
        return result == QtGui.QDialog.Accepted, my_form, form_drawer
