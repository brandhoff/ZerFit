# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow_lowres.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1158, 736)
        MainWindow.setStyleSheet("background-color: #FFF")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1131, 681))
        self.tabWidget.setObjectName("tabWidget")
        self.tabMain = QtWidgets.QWidget()
        self.tabMain.setObjectName("tabMain")
        self.plotSensor = MplWidget(self.tabMain)
        self.plotSensor.setGeometry(QtCore.QRect(20, 20, 500, 500))
        self.plotSensor.setObjectName("plotSensor")
        self.btnTakeImage = QtWidgets.QPushButton(self.tabMain)
        self.btnTakeImage.setGeometry(QtCore.QRect(20, 550, 171, 61))
        self.btnTakeImage.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"cursor: pointer;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnTakeImage.setObjectName("btnTakeImage")
        self.plotSensor_2 = MplWidget(self.tabMain)
        self.plotSensor_2.setGeometry(QtCore.QRect(590, 20, 500, 500))
        self.plotSensor_2.setObjectName("plotSensor_2")
        self.btnShow = QtWidgets.QPushButton(self.tabMain)
        self.btnShow.setGeometry(QtCore.QRect(590, 550, 171, 61))
        self.btnShow.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"cursor: pointer;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnShow.setObjectName("btnShow")
        self.btnSavePDF = QtWidgets.QPushButton(self.tabMain)
        self.btnSavePDF.setGeometry(QtCore.QRect(770, 550, 171, 61))
        self.btnSavePDF.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"cursor: pointer;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnSavePDF.setObjectName("btnSavePDF")
        self.btnSave_2 = QtWidgets.QPushButton(self.tabMain)
        self.btnSave_2.setGeometry(QtCore.QRect(950, 550, 171, 61))
        self.btnSave_2.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"cursor: pointer;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnSave_2.setObjectName("btnSave_2")
        self.spinBox = QtWidgets.QSpinBox(self.tabMain)
        self.spinBox.setGeometry(QtCore.QRect(590, 620, 71, 24))
        self.spinBox.setMinimum(1)
        self.spinBox.setObjectName("spinBox")
        self.label_2 = QtWidgets.QLabel(self.tabMain)
        self.label_2.setGeometry(QtCore.QRect(660, 620, 61, 21))
        self.label_2.setObjectName("label_2")
        self.horizontalSlider = QtWidgets.QSlider(self.tabMain)
        self.horizontalSlider.setGeometry(QtCore.QRect(590, 520, 251, 22))
        self.horizontalSlider.setMaximum(1000)
        self.horizontalSlider.setProperty("value", 200)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.btnCreateGrid = QtWidgets.QPushButton(self.tabMain)
        self.btnCreateGrid.setGeometry(QtCore.QRect(210, 550, 171, 61))
        self.btnCreateGrid.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"cursor: pointer;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnCreateGrid.setObjectName("btnCreateGrid")
        self.tabWidget.addTab(self.tabMain, "")
        self.tabCalibration = QtWidgets.QWidget()
        self.tabCalibration.setObjectName("tabCalibration")
        self.plotSensor_3 = MplWidget(self.tabCalibration)
        self.plotSensor_3.setGeometry(QtCore.QRect(20, 10, 1000, 1000))
        self.plotSensor_3.setObjectName("plotSensor_3")
        self.btnImgCali = QtWidgets.QPushButton(self.tabCalibration)
        self.btnImgCali.setGeometry(QtCore.QRect(1030, 70, 221, 71))
        self.btnImgCali.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"cursor: pointer;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnImgCali.setObjectName("btnImgCali")
        self.checkBox = QtWidgets.QCheckBox(self.tabCalibration)
        self.checkBox.setGeometry(QtCore.QRect(1040, 30, 201, 23))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.spinNumFoci = QtWidgets.QSpinBox(self.tabCalibration)
        self.spinNumFoci.setGeometry(QtCore.QRect(1270, 30, 111, 31))
        self.spinNumFoci.setObjectName("spinNumFoci")
        self.label = QtWidgets.QLabel(self.tabCalibration)
        self.label.setGeometry(QtCore.QRect(1400, 30, 151, 31))
        self.label.setObjectName("label")
        self.btnFindSpotsCali = QtWidgets.QPushButton(self.tabCalibration)
        self.btnFindSpotsCali.setGeometry(QtCore.QRect(1030, 160, 221, 71))
        self.btnFindSpotsCali.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"cursor: pointer;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnFindSpotsCali.setObjectName("btnFindSpotsCali")
        self.btnBuildGrid = QtWidgets.QPushButton(self.tabCalibration)
        self.btnBuildGrid.setGeometry(QtCore.QRect(1030, 250, 221, 71))
        self.btnBuildGrid.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"cursor: pointer;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnBuildGrid.setObjectName("btnBuildGrid")
        self.tabWidget.addTab(self.tabCalibration, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1158, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnTakeImage.setText(_translate("MainWindow", "Take Image"))
        self.btnShow.setText(_translate("MainWindow", "Reconstruct Wavefront"))
        self.btnSavePDF.setText(_translate("MainWindow", "Save PDF"))
        self.btnSave_2.setText(_translate("MainWindow", "Save TXT"))
        self.label_2.setText(_translate("MainWindow", "Order"))
        self.btnCreateGrid.setText(_translate("MainWindow", "Create Grid"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMain), _translate("MainWindow", "Main"))
        self.btnImgCali.setText(_translate("MainWindow", "Take Image"))
        self.checkBox.setText(_translate("MainWindow", "Use analytic Calibration"))
        self.label.setText(_translate("MainWindow", "Number of Foci"))
        self.btnFindSpotsCali.setText(_translate("MainWindow", "Find Spots"))
        self.btnBuildGrid.setText(_translate("MainWindow", "Build Grid"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCalibration), _translate("MainWindow", "Analyse"))

from mplwidget import MplWidget
