# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\dvalovcin\Documents\GitHub\Interactivepg-waffle\interactivePG\fixes\AxisSettings.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_AxisSettingsDialog(object):
    def setupUi(self, AxisSettingsDialog):
        AxisSettingsDialog.setObjectName(_fromUtf8("AxisSettingsDialog"))
        AxisSettingsDialog.resize(309, 180)
        self.verticalLayout = QtGui.QVBoxLayout(AxisSettingsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cbVisible = QtGui.QCheckBox(AxisSettingsDialog)
        self.cbVisible.setObjectName(_fromUtf8("cbVisible"))
        self.horizontalLayout.addWidget(self.cbVisible)
        self.label_6 = QtGui.QLabel(AxisSettingsDialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout.addWidget(self.label_6)
        self.tTitle = QtGui.QLineEdit(AxisSettingsDialog)
        self.tTitle.setObjectName(_fromUtf8("tTitle"))
        self.horizontalLayout.addWidget(self.tTitle)
        self.label_9 = QtGui.QLabel(AxisSettingsDialog)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout.addWidget(self.label_9)
        self.sbSize = SpinBox(AxisSettingsDialog)
        self.sbSize.setObjectName(_fromUtf8("sbSize"))
        self.horizontalLayout.addWidget(self.sbSize)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(AxisSettingsDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.tFrom = QFNumberEdit(AxisSettingsDialog)
        self.tFrom.setObjectName(_fromUtf8("tFrom"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.tFrom)
        self.label_2 = QtGui.QLabel(AxisSettingsDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.tTo = QFNumberEdit(AxisSettingsDialog)
        self.tTo.setObjectName(_fromUtf8("tTo"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.tTo)
        self.label_3 = QtGui.QLabel(AxisSettingsDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.cbMode = QtGui.QComboBox(AxisSettingsDialog)
        self.cbMode.setObjectName(_fromUtf8("cbMode"))
        self.cbMode.addItem(_fromUtf8(""))
        self.cbMode.addItem(_fromUtf8(""))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.cbMode)
        self.horizontalLayout_2.addLayout(self.formLayout)
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_7 = QtGui.QLabel(AxisSettingsDialog)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_7)
        self.label_8 = QtGui.QLabel(AxisSettingsDialog)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_8)
        self.tMajSpacing = QFNumberEdit(AxisSettingsDialog)
        self.tMajSpacing.setObjectName(_fromUtf8("tMajSpacing"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.tMajSpacing)
        self.tMinSpacing = QFNumberEdit(AxisSettingsDialog)
        self.tMinSpacing.setObjectName(_fromUtf8("tMinSpacing"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.tMinSpacing)
        self.label_4 = QtGui.QLabel(AxisSettingsDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.bColor = ColorButton(AxisSettingsDialog)
        self.bColor.setText(_fromUtf8(""))
        self.bColor.setObjectName(_fromUtf8("bColor"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.bColor)
        self.label_5 = QtGui.QLabel(AxisSettingsDialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)
        self.tWidth = QFNumberEdit(AxisSettingsDialog)
        self.tWidth.setObjectName(_fromUtf8("tWidth"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.tWidth)
        self.horizontalLayout_2.addLayout(self.formLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(AxisSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AxisSettingsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AxisSettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AxisSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AxisSettingsDialog)

    def retranslateUi(self, AxisSettingsDialog):
        AxisSettingsDialog.setWindowTitle(_translate("AxisSettingsDialog", "Axis Settings", None))
        self.cbVisible.setText(_translate("AxisSettingsDialog", "Visible", None))
        self.label_6.setText(_translate("AxisSettingsDialog", "Title", None))
        self.label_9.setText(_translate("AxisSettingsDialog", "Size:", None))
        self.label.setText(_translate("AxisSettingsDialog", "From", None))
        self.label_2.setText(_translate("AxisSettingsDialog", "To", None))
        self.label_3.setText(_translate("AxisSettingsDialog", "Type", None))
        self.cbMode.setItemText(0, _translate("AxisSettingsDialog", "Linear", None))
        self.cbMode.setItemText(1, _translate("AxisSettingsDialog", "Log10", None))
        self.label_7.setText(_translate("AxisSettingsDialog", "Major Spacing", None))
        self.label_8.setText(_translate("AxisSettingsDialog", "Minor Spacing", None))
        self.label_4.setText(_translate("AxisSettingsDialog", "Color", None))
        self.label_5.setText(_translate("AxisSettingsDialog", "Width", None))

from InstsAndQt.customQt import QFNumberEdit
from pyqtgraph import ColorButton, SpinBox
