from PyQt4 import QtGui, uic
from PyQt4.QtGui import QDialog


class StateSelectorQDialog(QDialog):
    def __init__(self, parent=None):
        super(StateSelectorQDialog, self).__init__(parent)
        uic.loadUi("basestation/ui/ui_state_selector.ui", self)

    @staticmethod
    def get_states_to_execute(parent=None):
        dialog = StateSelectorQDialog(parent)
        result = dialog.exec_()
        state_list = list()
        if dialog.checkBox_findTreasures.isChecked():
            state_list.append("FindTreasuresState")
        if dialog.checkBox_moveToRechargeStation.isChecked():
            state_list.append("MoveToChargeStationState")
        if dialog.checkBox_recharge.isChecked():
            state_list.append("ChargeState")
        if dialog.checkBox_readCode.isChecked():
            state_list.append("ReadCodeState")
        if dialog.checkBox_moveToTreasure.isChecked():
            state_list.append("MoveToTreasureState")
        if dialog.checkBox_pickupTreasure.isChecked():
            state_list.append("PickupTreasureState")
        if dialog.checkBox_moveToIsland.isChecked():
            state_list.append("MoveToIslandState")
        if dialog.checkBox_dropTreasure.isChecked():
            state_list.append("DropTreasureState")
        return result == QtGui.QDialog.Accepted, state_list
