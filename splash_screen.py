from PyQt5 import QtCore, QtGui, QtWidgets
import sys, res_splash


class Ui_SplashScreen(object):
    def setupUi(self, SplashScreen):
        SplashScreen.setObjectName("SplashScreen")
        SplashScreen.resize(680, 400)
        self.centralwidget = QtWidgets.QWidget(SplashScreen)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dropShadowFrame = QtWidgets.QFrame(self.centralwidget)
        self.dropShadowFrame.setStyleSheet("QFrame{\n"
"    \n"
"    \n"
"    image: url(:/title/splash-title.png);\n"
"    color: rgba(243, 4, 151, 100);\n"
"    border-radius: 20px;\n"
"}")
        self.dropShadowFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dropShadowFrame.setObjectName("dropShadowFrame")
        self.fish = QtWidgets.QGraphicsView(self.dropShadowFrame)
        self.fish.setGeometry(QtCore.QRect(300, 190, 51, 41))
        self.fish.setAcceptDrops(False)
        self.fish.setStyleSheet("border-image: url(:/fish/splash-fish.png);")
        self.fish.setInteractive(False)
        self.fish.setObjectName("fish")
        self.progressBar = QtWidgets.QProgressBar(self.dropShadowFrame)
        self.progressBar.setGeometry(QtCore.QRect(50, 250, 561, 23))
        self.progressBar.setStyleSheet("QProgressBar {\n"
"    \n"
"    background-color: rgb(94, 37, 204);\n"
"    color: rgb(255, 255, 255);\n"
"    border-style: none;\n"
"    border-radius: 20px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    border-radius: 10px;\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.67, x2:1, y2:0, stop:0 rgba(247, 99, 12, 255), stop:1 rgba(243, 4, 151, 100));\n"
"}\n"
"")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(self.dropShadowFrame)
        self.label.setGeometry(QtCore.QRect(0, 300, 661, 20))
        font = QtGui.QFont()
        font.setFamily("Lucida Sans Typewriter")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 69, 224)")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.dropShadowFrame)
        SplashScreen.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SplashScreen)
        self.statusbar.setObjectName("statusbar")
        SplashScreen.setStatusBar(self.statusbar)

        self.retranslateUi(SplashScreen)
        QtCore.QMetaObject.connectSlotsByName(SplashScreen)

    def retranslateUi(self, SplashScreen):
        _translate = QtCore.QCoreApplication.translate
        SplashScreen.setWindowTitle(_translate("SplashScreen", "MainWindow"))
        self.label.setText(_translate("SplashScreen", "loading..."))
