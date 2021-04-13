# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup

cityList = []
cityDict = {}

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1042, 783)
        MainWindow.setMinimumSize(QtCore.QSize(1042, 783))
        MainWindow.setMaximumSize(QtCore.QSize(1042, 783))
        MainWindow.setSizeIncrement(QtCore.QSize(200, 200))
        MainWindow.setIconSize(QtCore.QSize(24, 24))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(738, 0))
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(540, 80, 121, 41))
        self.pushButton.setObjectName("pushButton")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 90, 141, 31))
        self.label.setObjectName("label")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(230, 80, 301, 41))
        self.textEdit.setObjectName("textEdit")

        self.Back_ground = QtWidgets.QLabel(self.centralwidget)
        self.Back_ground.setGeometry(QtCore.QRect(0, -10, 1081, 811))
        self.Back_ground.setText("")
        self.Back_ground.setPixmap(QtGui.QPixmap("233.png"))
        self.Back_ground.setObjectName("Back_ground")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(230, 180, 431, 241))
        self.textBrowser.setObjectName("textBrowser")
        self.Message = QtWidgets.QLabel(self.centralwidget)
        self.Message.setGeometry(QtCore.QRect(100, 510, 111, 41))
        self.Message.setObjectName("Message")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(230, 500, 441, 51))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.Title = QtWidgets.QLabel(self.centralwidget)
        self.Title.setGeometry(QtCore.QRect(270, 20, 351, 41))
        self.Title.setObjectName("Title")
        self.Back_ground.raise_()
        self.pushButton.raise_()
        self.label.raise_()
        self.textEdit.raise_()
        self.textBrowser.raise_()
        self.Message.raise_()
        self.textBrowser_2.raise_()
        self.Title.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionada = QtWidgets.QAction(MainWindow)
        self.actionada.setObjectName("actionada")

        font = QtGui.QFont()
        font.setFamily('黑体')
        font.setBold(True)
        font.setPointSize(15)
        font.setWeight(80)
        self.textEdit.setFont(font)
        self.textBrowser.setFont(font)
        self.textBrowser_2.setFont(font)

        #self.textEdit.inputMethodEvent()
        self.pushButton.clicked.connect(self.Show_print)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "查询"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">"
                                                    "输入查询城市：</span></p></body></html>"))
        self.Message.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;"
                                                      " color:#000000;\">生活小贴士：</span></p></body></html>"))
        self.Title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;"
                                                    " font-weight:600; color:#000001;\">Python 天气</span></p></body></html>"))
        self.actionada.setText(_translate("MainWindow", "ada"))

    def Show_print(self):
        str1, str2 = self.main()
        #self.textBrowser.setText(self.main())
        self.textBrowser.setText(str1)
        self.textBrowser_2.setText(str2)

    def Input_city(self):
        city_name = self.textEdit.toPlainText()
        for key in cityDict.keys():
            if city_name == key:
                return cityDict[key]
            else:
                if cityDict[key] == '101340406':
                    #self.textBrowser.setText("查询城市不在记录中，请重新输入城市名称！")
                    return "0"

    #将txt内容转换为字典
    def Get_city(self):
        with open("./CITY.txt", 'r', encoding='UTF-8') as file:
            loadList = json.load(file)  # 省份
            #print(type(loadList))
            for i in range(0, 4):
                cityList.append(loadList[i]['cityList'])
            for i in range(4, 34):
                for j in loadList[i]['cityList']:
                    cityList.append(j['districtList'])
            for i in cityList:
                for j in i:
                    if 'cityName' in j.keys():
                        cityDict.setdefault(j['cityName'], j['cityId'])  # 直辖市
                    else:
                        cityDict.setdefault(j['districtName'], j['districtId'])  # 省

    #获取天气的html
    def Get_weather(self,net):
        url = urlopen(net)
        soup = BeautifulSoup(url, 'html.parser')
        #tag = soup.find('li', class_="skyid")
        return soup

    def main(self):
        self.Get_city()
        City_num = self.Input_city()
        if City_num!="0":
            net = "http://www.weather.com.cn/weather/" + City_num + ".shtml"
            soup = self.Get_weather(net)
            tag = soup.find('li', class_="skyid")
            #tag = self.Get_weather(net)
            str0 = "天气状况：" + tag.find('p', class_="wea").string + '\n'
            # str1 = "气温："+tag.find('p', class_="tem").find('span').string + "/" + tag.find('p', class_="tem").find('i').string+'\n'
            str1 = "气温：" + tag.find('p', class_="tem").find('i').string + '\n'
            str2 = "风向：" + tag.find('p', class_="win").find('span')['title'] + '\n'
            str3 = "风力：" + tag.find('p', class_="win").find('i').string + '\n'
            str4 = soup.find('li', class_ = 'li3 hot').p.string
            return str0 + str1 + str2 + str3, str4
        else:
            return "查询城市不在记录中，请重新输入城市名称~~~", "小贴士正在赶来的路上。。。。。"

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())