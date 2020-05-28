from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import timedelta
import keyboard
import sys
import time
import configparser

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        label_dims = (int(config['Default']['box_width']),int(config['Default']['box_height']))
        self.startText = ""
        self.buildData = self.getBuildData(config['Default']['build_order_path'])
        self.buildProg = 0
        self.buildMax = len(self.buildData)
        if self.buildMax > 1 and (self.buildData[0][1] == '0:00' or self.buildData[0][1] == '00:00'):
            self.buildProg = 1
        buildString = self.getBuildString(config['Default']['build_order_path'])
        self.label = QLabel(text=self.buildData[self.buildProg][0])
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: rgba" + config['Default']['app_color'] + "; color : white; font-size: 14px;") 
        self.label.setFixedWidth(label_dims[0])
        self.label.setMinimumSize(label_dims[0], label_dims[1])
        ag = QDesktopWidget().availableGeometry()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")
        self.setCentralWidget(self.label)
        x = ag.width() - self.label.width() - ag.width()//100
        y = ag.height() // 10
        self.move(x,y)

    def getBuildString(self,fileName):
        f = open(fileName,"r")
        buildString = f.read()
        return buildString

    def getBuildData(self,fileName):
        f = open(fileName,"r")
        buildString = f.read()
        actionsList = buildString.split("\n")
        actionsList = actionsList[1:]
        if actionsList[-1] == "":
            actionsList = actionsList[:-1]
        actionsList = list(map(lambda x: x.split(","), actionsList))
        actionsList=  [[str(x[0]),str(x[1])] for x in actionsList]
        return actionsList
    
    def updateTime(self):
        if len(self.buildData) < 1:
            return
        if self.buildProg >= self.buildMax:
            return
        elapsedTime = (time.time() - startTime)
        hours, rem = divmod(elapsedTime, 3600)
        minutes, seconds = divmod(rem, 60)
        seconds = int(seconds)
        startTextRaw = "{:d}:{:02d}".format(int(minutes),seconds)
        startText = "<html>Time: " + startTextRaw + " / " + self.buildData[self.buildProg][1] + "<br/><br/></html>" 
        if startTextRaw == self.buildData[self.buildProg][1] or "0"+ startTextRaw == self.buildData[self.buildProg][1]:
            self.buildProg += 1
        else:
            if self.buildProg + 1 < self.buildMax and self.buildProg > 0:
                self.label.setText(startText + "<html>"+self.buildData[self.buildProg - 1][0] + "<br/></html>" + '<html><b><p style="font-size:16px">'+self.buildData[self.buildProg][0] + \
                "</p><br/></b></html>" + "<html>"+self.buildData[self.buildProg + 1][0] + "</html>")
            elif self.buildProg + 1 < self.buildMax:
                self.label.setText(startText + '<html><b><p style="font-size:16px">' +self.buildData[self.buildProg][0] + \
                "</p><br/></b></html>" + "<html>"+self.buildData[self.buildProg + 1][0] + "</html>")
            elif self.buildProg > 0:
                self.label.setText(startText + "<html>"+self.buildData[self.buildProg - 1][0] + '<br/></html><p style="font-size:16px">' + "<html><b>"+self.buildData[self.buildProg][0] + \
                "</p></b></html>")
            else:
                self.label.setText(startText + "<html><b>"+self.buildData[self.buildProg][0] + \
                "</b></html>")

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.close()

config = configparser.ConfigParser()
config.read('config.ini')
keyboard.wait(config['Default']['init_command'])
startTime = time.time() - 0.5
app = QApplication(sys.argv)
app.setWindowIcon(QIcon('icon_rts.ico'))
window = MainWindow()
window.setWindowIcon(QIcon('icon_rts.ico'))
timer = QTimer()
timer.timeout.connect(window.updateTime)
timer.start(int(config['Default']['timer_interval']))
flags = Qt.WindowFlags()
window.setWindowFlags(flags | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
window.show()
app.exec_()