#!/usr/bin/python2
# -*- coding: utf-8 -*-

COLORS = ["Jaune", "Bleu", "Rouge", "Vert"]
FORMS = ["Triangle", "Carre", "Pentagone", "Cercle"]


class Point:
    x = None
    y = None

    def __init__(self):
        pass

    def to_dict(self):
        dictionary = dict()
        dictionary["x"] = self.x
        dictionary["y"] = self.y
        return dictionary


class Form(object):
    descriptor_points = None
    form_type = None
    form_color = None
    form_descriptor_point_amount = None

    def __init__(self, form_type, form_descriptor_point_amount, form_color):
        self.descriptor_points = list()
        self.form_color = form_color
        self.form_type = form_type
        self.form_descriptor_point_amount = form_descriptor_point_amount

    def get_type(self):
        return self.form_type

    def add_descriptor_point(self, descriptor_point):
        if len(self.descriptor_points) >= self.form_descriptor_point_amount:
            raise RuntimeError(
                    str(self.form_type) + " only have " + str(self.form_descriptor_point_amount) + " descriptor point")
        else:
            self.descriptor_points.append(descriptor_point)
            if self.form_descriptor_point_amount == len(self.descriptor_points):
                return True
            return False

    def to_dict(self):
        dictionary = dict()
        dictionary["form_type"] = self.form_type
        dictionary["form_color"] = self.form_color
        dictionary["form_descriptor_point_amount"] = self.form_descriptor_point_amount
        descriptor_points_dict = list()
        for point in self.descriptor_points:
            descriptor_points_dict.append(point.to_dict())
        dictionary["descriptor_points"] = descriptor_points_dict
        return dictionary


class Triangle(Form):
    def __init__(self, form_color):
        super(Triangle, self).__init__("Triangle", 3, form_color)


class Square(Form):
    def __init__(self, form_color):
        super(Square, self).__init__("Carre", 4, form_color)


class Pentagon(Form):
    def __init__(self, form_color):
        super(Pentagon, self).__init__("Pentagone", 5, form_color)


class Circle(Form):
    def __init__(self, form_color):
        super(Circle, self).__init__("Cercle", 2, form_color)


class FormFactory:
    def __init__(self):
        pass

    def create_form(self, form, color):
        if form is "Triangle":
            return Triangle(color)
        elif form is "Carre":
            return Square(color)
        elif form is "Pentagone":
            return Pentagon(color)
        elif form is "Cercle":
            return Circle(color)
        else:
            return None
