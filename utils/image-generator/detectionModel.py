#!/usr/bin/python2
# -*- coding: utf-8 -*-
import json


def enum(**enums):
    return type('Enum', (), enums)


EXPORTER_TYPE = enum(JSON="json", CONSOLE="console")


class DetectionModel:
    form_list = None
    robot_position = None
    robot_orientation = None

    def __init__(self):
        self.form_list = list()

    def add_form(self, form):
        self.form_list.append(form)

    def set_robot_position(self, position):
        self.robot_position = position

    def set_robot_orientation(self, orientation):
        self.robot_orientation = orientation

    def get_forms(self):
        return self.form_list

    def to_dict(self):
        dictionary = dict()
        if self.robot_position is None:
            dictionary["robot_position"] = None
            dictionary["robot_orientation"] = None
        else:
            dictionary["robot_position"] = self.robot_position.to_dict()
            dictionary["robot_orientation"] = self.robot_orientation
        form_list_dict = list()
        for form in self.form_list:
            form_list_dict.append(form.to_dict())
        dictionary["from_list"] = form_list_dict
        return dictionary

    def get_robot_position(self):
        return self.robot_position;

    def get_robot_orientation(self):
        return self.robot_orientation;

    def get_form_list(self):
        return self.form_list;


class DetectionModelConsoleExporter:
    def export_model_to_file(self, detection_model, filename):
        print detection_model.to_dict()


class DetectionModelJSONExporter:
    def __init__(self):
        pass

    def export_model_to_file(self, detection_model, filename):
        localfilename = filename + ".json"
        with open(localfilename, 'w') as myfile:
            myfile.write(json.dumps(detection_model.to_dict(), indent=2, sort_keys=True).encode('utf8'))
            myfile.close()


class DetectionModelFactory:
    exporter_type = None

    def __init__(self, exporter_type=EXPORTER_TYPE.JSON):
        self.exporter_type = exporter_type

    def create_detection_model(self):
        return DetectionModel()

    def create_detection_model_exporter(self):
        if self.exporter_type is EXPORTER_TYPE.JSON:
            return DetectionModelJSONExporter()
        elif self.exporter_type is EXPORTER_TYPE.CONSOLE:
            return DetectionModelConsoleExporter()
        else:
            return None
