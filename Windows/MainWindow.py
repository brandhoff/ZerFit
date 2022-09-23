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
        MainWindow.resize(1137, 756)
        MainWindow.setStyleSheet("background-color: #FFF")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1131, 711))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.plotSensor_3 = MplWidget(self.tab)
        self.plotSensor_3.setGeometry(QtCore.QRect(20, 20, 500, 500))
        self.plotSensor_3.setObjectName("plotSensor_3")
        self.btnCaliConnect = QtWidgets.QPushButton(self.tab)
        self.btnCaliConnect.setGeometry(QtCore.QRect(770, 0, 171, 61))
        self.btnCaliConnect.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnCaliConnect.setObjectName("btnCaliConnect")
        self.btnCaliDisconnect = QtWidgets.QPushButton(self.tab)
        self.btnCaliDisconnect.setGeometry(QtCore.QRect(950, 0, 171, 61))
        self.btnCaliDisconnect.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnCaliDisconnect.setObjectName("btnCaliDisconnect")
        self.btnCaliConnect_2 = QtWidgets.QPushButton(self.tab)
        self.btnCaliConnect_2.setGeometry(QtCore.QRect(20, 520, 171, 61))
        self.btnCaliConnect_2.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnCaliConnect_2.setObjectName("btnCaliConnect_2")
        self.sliderCaliRadius = QtWidgets.QSlider(self.tab)
        self.sliderCaliRadius.setGeometry(QtCore.QRect(530, 520, 271, 22))
        self.sliderCaliRadius.setProperty("value", 50)
        self.sliderCaliRadius.setOrientation(QtCore.Qt.Horizontal)
        self.sliderCaliRadius.setObjectName("sliderCaliRadius")
        self.btnCaliRadius = QtWidgets.QPushButton(self.tab)
        self.btnCaliRadius.setGeometry(QtCore.QRect(530, 590, 171, 61))
        self.btnCaliRadius.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnCaliRadius.setObjectName("btnCaliRadius")
        self.btnCaliUp = QtWidgets.QPushButton(self.tab)
        self.btnCaliUp.setGeometry(QtCore.QRect(640, 360, 51, 51))
        self.btnCaliUp.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnCaliUp.setObjectName("btnCaliUp")
        self.btnCaliRight = QtWidgets.QPushButton(self.tab)
        self.btnCaliRight.setGeometry(QtCore.QRect(690, 410, 51, 51))
        self.btnCaliRight.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnCaliRight.setObjectName("btnCaliRight")
        self.btnCaliLeft = QtWidgets.QPushButton(self.tab)
        self.btnCaliLeft.setGeometry(QtCore.QRect(590, 410, 51, 51))
        self.btnCaliLeft.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnCaliLeft.setObjectName("btnCaliLeft")
        self.btnCaliDown = QtWidgets.QPushButton(self.tab)
        self.btnCaliDown.setGeometry(QtCore.QRect(640, 460, 51, 51))
        self.btnCaliDown.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnCaliDown.setObjectName("btnCaliDown")
        self.btnCaliGridFix = QtWidgets.QPushButton(self.tab)
        self.btnCaliGridFix.setGeometry(QtCore.QRect(720, 590, 171, 61))
        self.btnCaliGridFix.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnCaliGridFix.setObjectName("btnCaliGridFix")
        self.btnCaliLoadGrid = QtWidgets.QPushButton(self.tab)
        self.btnCaliLoadGrid.setGeometry(QtCore.QRect(20, 590, 171, 61))
        self.btnCaliLoadGrid.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnCaliLoadGrid.setObjectName("btnCaliLoadGrid")
        self.btnCaliSaveGrid = QtWidgets.QPushButton(self.tab)
        self.btnCaliSaveGrid.setGeometry(QtCore.QRect(200, 590, 171, 61))
        self.btnCaliSaveGrid.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnCaliSaveGrid.setObjectName("btnCaliSaveGrid")
        self.textCaliCamera = QtWidgets.QTextEdit(self.tab)
        self.textCaliCamera.setEnabled(True)
        self.textCaliCamera.setGeometry(QtCore.QRect(770, 70, 351, 211))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.textCaliCamera.setFont(font)
        self.textCaliCamera.setReadOnly(True)
        self.textCaliCamera.setPlaceholderText("")
        self.textCaliCamera.setObjectName("textCaliCamera")
        self.tabWidget.addTab(self.tab, "")
        self.tabMain = QtWidgets.QWidget()
        self.tabMain.setObjectName("tabMain")
        self.plotSensor = MplWidget(self.tabMain)
        self.plotSensor.setGeometry(QtCore.QRect(20, 20, 500, 500))
        self.plotSensor.setObjectName("plotSensor")
        self.btnTakeImage = QtWidgets.QPushButton(self.tabMain)
        self.btnTakeImage.setGeometry(QtCore.QRect(10, 550, 171, 61))
        self.btnTakeImage.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
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
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnShow.setObjectName("btnShow")
        self.btnSavePDF = QtWidgets.QPushButton(self.tabMain)
        self.btnSavePDF.setGeometry(QtCore.QRect(770, 550, 171, 61))
        self.btnSavePDF.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnSavePDF.setObjectName("btnSavePDF")
        self.btnSave_2 = QtWidgets.QPushButton(self.tabMain)
        self.btnSave_2.setGeometry(QtCore.QRect(950, 550, 171, 61))
        self.btnSave_2.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnSave_2.setObjectName("btnSave_2")
        self.spinBox = QtWidgets.QSpinBox(self.tabMain)
        self.spinBox.setGeometry(QtCore.QRect(590, 620, 71, 24))
        self.spinBox.setMinimum(1)
        self.spinBox.setProperty("value", 6)
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
        self.btnCreateGrid.setGeometry(QtCore.QRect(190, 550, 171, 61))
        self.btnCreateGrid.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnCreateGrid.setObjectName("btnCreateGrid")
        self.btnFindSpots = QtWidgets.QPushButton(self.tabMain)
        self.btnFindSpots.setGeometry(QtCore.QRect(370, 550, 171, 61))
        self.btnFindSpots.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnFindSpots.setObjectName("btnFindSpots")
        self.checkBoxAutomatic = QtWidgets.QCheckBox(self.tabMain)
        self.checkBoxAutomatic.setGeometry(QtCore.QRect(380, 610, 141, 21))
        self.checkBoxAutomatic.setObjectName("checkBoxAutomatic")
        self.checkBoxCorrectTipTilt = QtWidgets.QCheckBox(self.tabMain)
        self.checkBoxCorrectTipTilt.setGeometry(QtCore.QRect(380, 630, 141, 21))
        self.checkBoxCorrectTipTilt.setObjectName("checkBoxCorrectTipTilt")
        self.btnSave_3 = QtWidgets.QPushButton(self.tabMain)
        self.btnSave_3.setGeometry(QtCore.QRect(950, 620, 171, 61))
        self.btnSave_3.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnSave_3.setObjectName("btnSave_3")
        self.tabWidget.addTab(self.tabMain, "")
        self.tabCalibration = QtWidgets.QWidget()
        self.tabCalibration.setObjectName("tabCalibration")
        self.plotAnalyse = MplWidget(self.tabCalibration)
        self.plotAnalyse.setGeometry(QtCore.QRect(20, 10, 500, 500))
        self.plotAnalyse.setObjectName("plotAnalyse")
        self.btnPlotZernike = QtWidgets.QPushButton(self.tabCalibration)
        self.btnPlotZernike.setGeometry(QtCore.QRect(530, 100, 221, 71))
        self.btnPlotZernike.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"cursor: pointer;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnPlotZernike.setObjectName("btnPlotZernike")
        self.spinNumFoci = QtWidgets.QSpinBox(self.tabCalibration)
        self.spinNumFoci.setGeometry(QtCore.QRect(1270, 30, 111, 31))
        self.spinNumFoci.setObjectName("spinNumFoci")
        self.label = QtWidgets.QLabel(self.tabCalibration)
        self.label.setGeometry(QtCore.QRect(1400, 30, 151, 31))
        self.label.setObjectName("label")
        self.btnFindSpotsCali = QtWidgets.QPushButton(self.tabCalibration)
        self.btnFindSpotsCali.setGeometry(QtCore.QRect(530, 180, 221, 71))
        self.btnFindSpotsCali.setStyleSheet("color: #fff;\n"
"background-color: #337ab7;\n"
"border-color: #2e6da4;\n"
"cursor: pointer;\n"
"background-image: none;\n"
"border: 1px solid transparent;\n"
"border-radius: 4px;")
        self.btnFindSpotsCali.setObjectName("btnFindSpotsCali")
        self.spinBoxSingleZernike = QtWidgets.QSpinBox(self.tabCalibration)
        self.spinBoxSingleZernike.setGeometry(QtCore.QRect(760, 110, 71, 24))
        self.spinBoxSingleZernike.setMinimum(1)
        self.spinBoxSingleZernike.setProperty("value", 6)
        self.spinBoxSingleZernike.setObjectName("spinBoxSingleZernike")
        self.label_3 = QtWidgets.QLabel(self.tabCalibration)
        self.label_3.setGeometry(QtCore.QRect(830, 110, 61, 21))
        self.label_3.setObjectName("label_3")
        self.sliderAnalyse = QtWidgets.QSlider(self.tabCalibration)
        self.sliderAnalyse.setGeometry(QtCore.QRect(30, 520, 251, 22))
        self.sliderAnalyse.setMaximum(1000)
        self.sliderAnalyse.setProperty("value", 200)
        self.sliderAnalyse.setOrientation(QtCore.Qt.Horizontal)
        self.sliderAnalyse.setObjectName("sliderAnalyse")
        self.tabWidget.addTab(self.tabCalibration, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1137, 21))
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
        MainWindow.setWindowTitle(_translate("MainWindow", "ZerFit"))
        self.btnCaliConnect.setText(_translate("MainWindow", "Connect"))
        self.btnCaliDisconnect.setText(_translate("MainWindow", "Disconnect"))
        self.btnCaliConnect_2.setText(_translate("MainWindow", "Take Image"))
        self.btnCaliRadius.setText(_translate("MainWindow", "Set ROI"))
        self.btnCaliUp.setText(_translate("MainWindow", "^"))
        self.btnCaliRight.setText(_translate("MainWindow", ">"))
        self.btnCaliLeft.setText(_translate("MainWindow", "<"))
        self.btnCaliDown.setText(_translate("MainWindow", "v"))
        self.btnCaliGridFix.setText(_translate("MainWindow", "Fix my Grid"))
        self.btnCaliLoadGrid.setText(_translate("MainWindow", "Load Grid"))
        self.btnCaliSaveGrid.setText(_translate("MainWindow", "Save Grid"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Camera"))
        self.btnTakeImage.setText(_translate("MainWindow", "Insert Taken Image"))
        self.btnShow.setText(_translate("MainWindow", "Reconstruct Wavefront"))
        self.btnSavePDF.setText(_translate("MainWindow", "Save PDF"))
        self.btnSave_2.setText(_translate("MainWindow", "Save TXT"))
        self.label_2.setText(_translate("MainWindow", "Order"))
        self.btnCreateGrid.setText(_translate("MainWindow", "Create Grid"))
        self.btnFindSpots.setText(_translate("MainWindow", "Find Spots"))
        self.checkBoxAutomatic.setText(_translate("MainWindow", "Fit 2D Gaussian (slow!)"))
        self.checkBoxCorrectTipTilt.setText(_translate("MainWindow", "Auto-Correct Tip Tilt"))
        self.btnSave_3.setText(_translate("MainWindow", "Wavefront Info"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMain), _translate("MainWindow", "Fit Zernike"))
        self.btnPlotZernike.setText(_translate("MainWindow", "Plot Zernike"))
        self.label.setText(_translate("MainWindow", "Number of Foci"))
        self.btnFindSpotsCali.setText(_translate("MainWindow", "Open Exported TXT"))
        self.label_3.setText(_translate("MainWindow", "Degree"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCalibration), _translate("MainWindow", "Analyse"))

from mplwidget import MplWidget
