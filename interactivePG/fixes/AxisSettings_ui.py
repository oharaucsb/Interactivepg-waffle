# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\dvalovcin\Documents\GitHub\Interactivepg-waffle\interactivePG\fixes\AxisSettings.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AxisSettingsDialog(object):
    def setupUi(self, AxisSettingsDialog):
        AxisSettingsDialog.setObjectName("AxisSettingsDialog")
        AxisSettingsDialog.resize(309, 180)
        self.verticalLayout = QtWidgets.QVBoxLayout(AxisSettingsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cbVisible = QtWidgets.QCheckBox(AxisSettingsDialog)
        self.cbVisible.setObjectName("cbVisible")
        self.horizontalLayout.addWidget(self.cbVisible)
        self.label_6 = QtWidgets.QLabel(AxisSettingsDialog)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.tTitle = QtWidgets.QLineEdit(AxisSettingsDialog)
        self.tTitle.setObjectName("tTitle")
        self.horizontalLayout.addWidget(self.tTitle)
        self.label_9 = QtWidgets.QLabel(AxisSettingsDialog)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout.addWidget(self.label_9)
        self.sbSize = SpinBox(AxisSettingsDialog)
        self.sbSize.setObjectName("sbSize")
        self.horizontalLayout.addWidget(self.sbSize)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(AxisSettingsDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.tFrom = QFNumberEdit(AxisSettingsDialog)
        self.tFrom.setObjectName("tFrom")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tFrom)
        self.label_2 = QtWidgets.QLabel(AxisSettingsDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.tTo = QFNumberEdit(AxisSettingsDialog)
        self.tTo.setObjectName("tTo")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.tTo)
        self.label_3 = QtWidgets.QLabel(AxisSettingsDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.cbMode = QtWidgets.QComboBox(AxisSettingsDialog)
        self.cbMode.setObjectName("cbMode")
        self.cbMode.addItem("")
        self.cbMode.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cbMode)
        self.horizontalLayout_2.addLayout(self.formLayout)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_7 = QtWidgets.QLabel(AxisSettingsDialog)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.label_8 = QtWidgets.QLabel(AxisSettingsDialog)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.tMajSpacing = QFNumberEdit(AxisSettingsDialog)
        self.tMajSpacing.setObjectName("tMajSpacing")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tMajSpacing)
        self.tMinSpacing = QFNumberEdit(AxisSettingsDialog)
        self.tMinSpacing.setObjectName("tMinSpacing")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.tMinSpacing)
        self.label_4 = QtWidgets.QLabel(AxisSettingsDialog)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.bColor = ColorButton(AxisSettingsDialog)
        self.bColor.setText("")
        self.bColor.setObjectName("bColor")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.bColor)
        self.label_5 = QtWidgets.QLabel(AxisSettingsDialog)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.tWidth = QFNumberEdit(AxisSettingsDialog)
        self.tWidth.setObjectName("tWidth")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.tWidth)
        self.horizontalLayout_2.addLayout(self.formLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(AxisSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AxisSettingsDialog)
        self.buttonBox.accepted.connect(AxisSettingsDialog.accept)
        self.buttonBox.rejected.connect(AxisSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AxisSettingsDialog)

    def retranslateUi(self, AxisSettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        AxisSettingsDialog.setWindowTitle(_translate("AxisSettingsDialog", "Axis Settings"))
        self.cbVisible.setText(_translate("AxisSettingsDialog", "Visible"))
        self.label_6.setText(_translate("AxisSettingsDialog", "Title"))
        self.label_9.setText(_translate("AxisSettingsDialog", "Size:"))
        self.label.setText(_translate("AxisSettingsDialog", "From"))
        self.label_2.setText(_translate("AxisSettingsDialog", "To"))
        self.label_3.setText(_translate("AxisSettingsDialog", "Type"))
        self.cbMode.setItemText(0, _translate("AxisSettingsDialog", "Linear"))
        self.cbMode.setItemText(1, _translate("AxisSettingsDialog", "Log10"))
        self.label_7.setText(_translate("AxisSettingsDialog", "Major Spacing"))
        self.label_8.setText(_translate("AxisSettingsDialog", "Minor Spacing"))
        self.label_4.setText(_translate("AxisSettingsDialog", "Color"))
        self.label_5.setText(_translate("AxisSettingsDialog", "Width"))

from ..widgets.numberEdits import QFNumberEdit
from pyqtgraph import ColorButton, SpinBox
