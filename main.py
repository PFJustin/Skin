#add profile?? menu bar
#public UI 
#save routine info into config
#https://github.com/Jorgen-VikingGod/Qt-Frameless-Window-DarkStyle
#https://github.com/antonypro/QGoodWindow
#https://github.com/ThePBone/FlatTabWidget

import sys
import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox,QDialog, QApplication, QStackedWidget, QWidget, QTabWidget, QTableView, QMainWindow, QLabel, QHBoxLayout, QTableWidgetItem, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QFontMetrics, QMovie, QMoveEvent, QCursor, QTextCursor
from PyQt5.QtCore import Qt, QTimer, QSize, QDateTime, pyqtSignal
import requests
import json
import jsbeautifier
import re
import QNotifications #pip install python-qnotifications
import pickle
#import syntax
#from qt_material import apply_stylesheet

_token = ""
cmsdata = []
usermail = ""
survey_count = 0
option_count = 1
_products = []
tbcount = 0
condiname = []
option = []
option_ans = []
extra_valueLst = []
condi = {}
rtn = []

#class MainUi(QDialog):
class MainUi(QMainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        loadUi(r"login.ui",self)
        self.pwd_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_btn.clicked.connect(self.login_post)
        self.login_btn.setShortcut("Return")
        self._exitbtn.clicked.connect(self._exit)
        self._hidebtn.clicked.connect(self._min)
       
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor)) #更改鼠标图标
      
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag: 
            self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
            QMouseEvent.accept()
        
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))
    

    def _exit(self):
        self.close()
    def _min(self):
        self.showMinimized()
        



        #self.line = QLineEdit(self)

    def login_post(self):
        #print("login_post btn Clicked")
        self.accinfo = {}
        global usermail
        usermail = self.account_field.text()
        password = self.pwd_field.text()
        
          
        if len(usermail) == 0 or len(password) == 0:
            self.error_display.setText("Can't be empty")
            #loading_mask.hide()
        else:
            #self._loading()
            #self.load_ani = threading.Thread(target=self.show_animation)
            #self.load_ani.start()

            self.accinfo["email"] = usermail
            self.accinfo["password"] = password
            #print(self.accinfo)
            #login post
            #s = requests.Session()
            try:
                self.url = 'https://console-api.perfectcorp.com/backend/admin/customer/sign-in.action'
                self.HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
                x = requests.post(self.url, headers=self.HEADERS, data = self.accinfo)
                x = x.json() #convert respond dict into json
                with open('cmsdata.json', 'w') as outfile:
                    json.dump(x, outfile)
                
                if len(x["token"]) != 0:
                    #print(x["token"])
                    self.error_display.setText("")
                    #self.gotologin()
                    welcome.hide()
                    self.login = LoginScreen()
                    self.login.setWindowTitle("Skincare Logic Tool")
                    self.login.show()
            except KeyError:
                if x["status"] == "fail":
                    print(x["status"]),print(x["errorCode"]),print(x["errorType"]),print(x["errorMessage"])
                    self.error_msg = "Status: " + str(x["status"]) + " " + "Error Code: " + str(x["errorCode"]) + " " + "Type: " + str(x["errorType"]) + " " + "Message: " + str(x["errorMessage"])
                    self.error_display.setText(self.error_msg)
    '''
    def gotologin(self):
        login = LoginScreen()
        #widget.addWidget(login)
        #widget.setCurrentIndex(widget.currentIndex()+1)
    '''  


class LoginScreen(QMainWindow):
    
    print("token: " + _token)
    Signal = pyqtSignal
    notify = Signal(
		['QString', 'QString', int, bool],
		['QString', 'QString', int, bool, 'QString']
	)
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("condi.ui",self)
        self.gotoCalculator()
        
        '''
        highlight = syntax.PythonHighlighter(self.code.document())
        infile = open('syntax_pars.py', 'r')
        self.code.setPlainText(infile.read())
        '''
        

        #self.back_to_main_btn.clicked.connect(self.back_to_main) #回去后無法關閉這個window
        
        #model = QStandardItemModel(0, 3)
        #model.setHorizontalHeaderLabels(["SKU ID" , "SKU NAME",'SKU IMAGE','ENABLE'])

        #self.au.clicked.connect(au)

    def __setup_notification_area(self, targetWidget):
        notification_area = QNotifications.QNotificationArea(targetWidget)
        self.notify['QString', 'QString', int, bool].connect(
            notification_area.display
        )
        self.notify['QString', 'QString', int, bool, 'QString'].connect(
            notification_area.display
        )
        return notification_area


    def back_to_main(self):
        self.login = LoginScreen()
        self.login.hide() ##這個没写好
        welcome.show()
        
        #welcome.setCurrentIndex(widget.currentIndex()-1)
        #self.error_display.setText("")
        #self.account_field.setText("")
        #self.pwd_field.setText("")
    
        
    def gotoCalculator(self):
        self.timer=QTimer()
        self.timer.start(1000)
        time=QDateTime.currentDateTime()
        timedisplay=time.toString("yyyy-MM-dd hh:mm:ss dddd")#格式化一下時間
        self.notification_area = self.__setup_notification_area(self.centralwidget)
        #self.notify['QString', 'QString', int, bool, 'QString'].emit("test", "info", 5000, True, "button") #可接受5個參數
        self.notification_area.setEntryEffect("fadeIn", 1000) #fadeIn or None, ms
        self.notification_area.setExitEffect("fadeOut", 1000) #fadeOut or None, ms
        self.notify['QString', 'QString', int, bool].emit("Welcome", "primary", 10000, True) #"primary", "success", "info", "warning", "danger"


        self.label.setToolTip('Set up survey IDs if you will be using survey')
        self.dc_qIdField.setToolTip('Find survey optionID from Perfect console')
        self.dc_qAns.setToolTip('This field can be empty, can be used in advanced mode')
        self.declear_option_btn.setToolTip('Insert the survey will be use in the logic')
        self.declear_OptionAns_btn.setToolTip('Insert the survey answers that will be use in the logic')
        self.extra_nameField.setToolTip('If you will be using extra.info, declare here before insert into the logic')
        self.dc_specialVar.setToolTip('If you need special variables, declare here before insert into the logic')
        self.label_7.setToolTip('Click on the concerns that will be use in the logic for calculation')
        self.customize_cam.setToolTip('Declare customized concern if there is a customization')
        self.declare_cusCam.setToolTip('Insert the customized concern into the logic for further calculation')
        self.routine_name.setToolTip('Give a product routine a name')
        self.routine_id.setToolTip('Input product IDs in the field, and group them as a routine')
        self.add_routibe_tblBtn.setToolTip('Add products into a routine, can be added when creating logic')
        
        
        
        
        #login.setWindowTitle("Console Skincare Logic - " + usermail + ' - 登录: '+ timedisplay)
        #pfsearch = pfconsole.PerfectConsoleSearch()
        #widget.addWidget(pfsearch)
        #widget.setCurrentIndex(widget.currentIndex()+1)
        
        self.insert_elseif.hide()
        self._left_bracket.hide()
        self._letbtn.hide()
        self._elsebtn.hide()
        self.switchBtn.hide()
        self.caseBtn.hide()
        self.BreakBtn.hide()
        self._right_bracket.hide()
        self._left_curlybracket.hide()
        self._right_curlybracket.hide()
        #self.next_surveyBtn_2.hide()
        #self._closeif_btn_2.hide()
        self._semicom.hide()
        #exinfoname
        self.label_4.hide()
        self.code_5.hide()
        self.extra_nameField.hide()
        self.dc_extraInfoBtn.hide()
        self.code_6.hide()
        self.extraInfo_dropdown.hide()
        self.decear_extrainfo_btn.hide()
        self.line_5.hide()
        #specname
        self.label_10.hide()
        self.code_12.hide()
        self.dc_specialVar.hide()
        self.dc_specialVarBtn.hide()
        self.code_10.hide()
        self.dc_specialVar_dropdown.hide()
        self.dc_specialVarDetailBtn.hide()
        
        self.cheat.clicked.connect(self.advanced)
        self.saveSettingBtn.clicked.connect(self.saveConfig)
        self.loadSettingBtn.clicked.connect(self.loadConfig)
        self.helpbtn.clicked.connect(self.help)
        self.clearbtn.clicked.connect(self.cleartmpCondi)
        ##Step 1
        self.dc_questionBtn.clicked.connect(self.addsurvey)
        self.declear_option_btn.clicked.connect(self.insertOptionVar)
        self.declear_OptionAns_btn.clicked.connect(self.insertOptionAnsVar)
        self.dc_extraInfoBtn.clicked.connect(self.addextrainfo)
        self.dc_specialVarBtn.clicked.connect(self.addspecialVar)
        self.dc_specialVarDetailBtn.clicked.connect(self.insertspecialVarDetail)
        self.insert_specialNameBtn.clicked.connect(self.insertSpecialName)
        self.next_surveyBtn.clicked.connect(self.nextSurvey)
        self.add_routibe_tblBtn.clicked.connect(self.add_routine_tbl)
        
        ##step 2
        self.enable_darkc.clicked.connect(self.decleardc)
        self.enable_wrink.clicked.connect(self.declearwrink)
        self.enable_spots.clicked.connect(self.declearspot)
        self.enable_texture.clicked.connect(self.decleartexture)
        self.enable_oilness.clicked.connect(self.declearoil)
        self.enable_redness.clicked.connect(self.declearredness)
        self.enable_moisture.clicked.connect(self.declearmoist)
        self.enable_eyebag.clicked.connect(self.decleareyebag)
        self.enable_radiance.clicked.connect(self.declearradiance)
        self.add_cusCam.clicked.connect(self.declearcustomizeCam)
        self.declare_cusCam.clicked.connect(self.declearcustomizeCamToCode)
        self.insert_cusCam.clicked.connect(self.addCustomizeCam)

        #step 3 operator
        self.insert_if.clicked.connect(self.addif)
        self.insert_elseif.clicked.connect(self.addelseif)
        self._letbtn.clicked.connect(self.addLet)
        self._elsebtn.clicked.connect(self.addelse)
        self.switchBtn.clicked.connect(self.addSwitch)
        self.caseBtn.clicked.connect(self.addCase)
        self.BreakBtn.clicked.connect(self.addBreak)
        self.insert_and.clicked.connect(self.addand)
        self.insert_or.clicked.connect(self.addor)
        self.insert_hasAns.clicked.connect(self.addHasAns)
        self.insert_surveyOption_btn.clicked.connect(self.insertSurveyOption)
        self.insert_routineBtn.clicked.connect(self.insertRtouine)
        
        #step 3 concern score
        self.darkcircle_score.clicked.connect(self.addDarkCircle)
        self.wrinkles_score.clicked.connect(self.addWrinkles)
        self.spot_score.clicked.connect(self.addSpot)
        self.texture_score.clicked.connect(self.addTexture)
        self.oilnes_score.clicked.connect(self.addOilness)
        self.redness_score.clicked.connect(self.Addredness)
        self.moisture_score.clicked.connect(self.addMoisture)
        self.eyebag_score.clicked.connect(self.addEyebag)
        self.radiance_score.clicked.connect(self.addRadiance)
        self.skinage_score.clicked.connect(self.addSkinage)


        #step 3 operator
        self._plus.clicked.connect(self.addplus)
        self._minus.clicked.connect(self.addminus)
        self._times.clicked.connect(self.addtimes)
        self._divide.clicked.connect(self.adddivide)
        self._equal.clicked.connect(self.addequal)
        self._equals.clicked.connect(self.addequals)
        self._greater.clicked.connect(self.addgrater)
        self._smaller.clicked.connect(self.addsmaller)
        self._greater_equal.clicked.connect(self.addgequal)
        self._smaller_equal.clicked.connect(self.addsequal)
        self._not_equal.clicked.connect(self.addnotequal)
        self._not.clicked.connect(self.addnot)
        self._semicom.clicked.connect(self.addsemicom)
        self._left_bracket.clicked.connect(self.addleftbracket)
        self._right_bracket.clicked.connect(self.addrightbrcket)
        self._left_curlybracket.clicked.connect(self.addleftCbracket)
        self._right_curlybracket.clicked.connect(self.addrightCbrcket)

        #step 3 numbers
        self._1.clicked.connect(self.add1)
        self._2.clicked.connect(self.add2)
        self._3.clicked.connect(self.add3)
        self._4.clicked.connect(self.add4)
        self._5.clicked.connect(self.add5)
        self._6.clicked.connect(self.add6)
        self._7.clicked.connect(self.add7)
        self._8.clicked.connect(self.add8)
        self._9.clicked.connect(self.add9)
        self._0.clicked.connect(self.add0)


        #step 3 add special info
        
        self.insert_questionAnswer_btn.clicked.connect(self.insertAnswer)
        self.insert_freeText_btn.clicked.connect(self.insertFreetext)
        self.decear_extrainfo_btn.clicked.connect(self.declearExtraInfo)
        self.insert_extrainfoName_btn.clicked.connect(self.insertExtraInfoName)

        #step 3 close if
        self._closeif_btn.clicked.connect(self.closeif)
        
        #step 4 add id to product pool
        self.add_productid_btn.clicked.connect(self.addtoProductpool)
        self.insert_productid_btn.clicked.connect(self.insertProduct)

        #Step 5 add into condi database
        self.addToCondiStoreBtn.clicked.connect(self.addToCondiDB)
        #self.condiDB_Dropdown.currentIndexChanged.connect(self.condiPreview) #改爲table

        #Step 6 Complete JS
        #self.insert_condiBtn.clicked.connect(self.InsertCondi) #整合入table
        #self.remove_condiBtn.clicked.connect(self.RemoveCondi) #整合如table
        self.endingBtn.clicked.connect(self.complete)
        self.nice.clicked.connect(self.nicee)
        self.checker.clicked.connect(self.validate)
    #step 1
    def nextSurvey(self):
        global survey_count, option_count
        survey_count = int(survey_count)
        survey_count = survey_count + 1
        option_count = 1
        self.count_survey.setText(str(survey_count))

    def addsurvey(self):
        global survey_count, option_count, option, option_ans
        
        survey_count = self.count_survey.text()
        _qId = self.dc_qIdField.text()
        _ans = self.dc_qAns.text()
        _qId = _qId.strip()
        #_ans = self._ans.strip() #Answer can be blank?
        #if _qId.isnumeric() == True and len(_ans) != 0:
        if _qId.isnumeric() == True:
            option_var_name = "var q" + str(survey_count) + "_" + "a" + str(option_count) + " = " + str(_qId) + ";"
            option_var_Ans = "var q" + str(survey_count) + "_" + "a" + str(option_count) + "_ans" + " = " + str(_ans) + ";"
            option_name = "q" + str(survey_count) + "_" + "a" + str(option_count)
            option_Ans = "q" + str(survey_count) + "_" + "a" + str(option_count) + "_ans"

            option.append(option_name)
            option_ans.append(option_Ans)
            
            self.dcOption_dropDown.addItem(option_var_name)
            self.dcOptionAns_dropDown.addItem(option_var_Ans)

            self.survey_option_dropdown.addItem(option_name)
            self.survey_ans_dropdown.addItem(option_Ans)

            option_count = option_count + 1
            self.dc_qIdField.clear()
            self.dc_qAns.clear()
        else:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet("QLabel{ color: black}")
            msgbox.setWindowTitle('Invalid ID')
            msgbox.setIcon(msgbox.Warning)
            msgbox.setText("Survey Option ID can not be empty if you want add survey\nSurvey Answers can be empty.")
            msgbox.exec()
    
    def insertOptionVar(self):
        self.selected = self.dcOption_dropDown.currentText()
        self.code.append(self.selected)

    def insertOptionAnsVar(self):
        self.selected = self.dcOptionAns_dropDown.currentText()
        self.code.append(self.selected)

    def addextrainfo(self):
        global extra_valueLst
        _extraValueName = self.extra_nameField.text()
        _extraValueName = _extraValueName.strip()
        if len(_extraValueName) != 0:
            extra_valueLst.append(_extraValueName)
            self.extraInfo_dropdown.addItem(_extraValueName)
            self.extraInfoName_dropdown.addItem(_extraValueName)
            self.extra_nameField.clear()
        else:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet("QLabel{ color: black}")
            msgbox.setWindowTitle('Invalid Name')
            msgbox.setIcon(msgbox.Warning)
            msgbox.setText("Name cannot be empty")
            msgbox.exec()

    def insertAnswer(self):
        self.selected = self.survey_ans_dropdown.currentText()
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText(self.selected + "== ")
    
    def declearExtraInfo(self):
        self.selected = self.extraInfo_dropdown.currentText()
        self.selected = self.selected.strip()
        if len(self.selected) != 0:
            self.tmp_condition.append("extra_info." + self.selected + " = ")
            self.notify['QString', 'QString', int, bool].emit("Don't forget to end with semicolon(;)", "info", 10000, True)
            self.pixmap = QPixmap('alert.png')
            self.icon = QIcon(self.pixmap)
            self._semicom.setIcon(self.icon)
        else:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet("QLabel{ color: black}")
            msgbox.setWindowTitle('Invalid Name')
            msgbox.setIcon(msgbox.Warning)
            msgbox.setText("No extra.info name to be declare")
            msgbox.exec()

    def insertExtraInfoName(self):
        self.selected = self.extraInfoName_dropdown.currentText()
        self.selected = self.selected.strip()
        if len(self.selected) != 0:
            self.tmp_condition.moveCursor(QTextCursor.End)
            self.tmp_condition.insertPlainText("extra_info." + self.selected + "")
        else:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet("QLabel{ color: black}")
            msgbox.setWindowTitle('Empty extra_info Name')
            msgbox.setIcon(msgbox.Warning)
            msgbox.setText("No extra.info name to be insert")
            msgbox.exec()

        

    def insertFreetext(self):
        self._text = self.freeTextBox.text()
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText('"' + str(self._text) + '"')
        self.freeTextBox.clear()

    def addspecialVar(self):
        self._spVar = self.dc_specialVar.text()
        self._spVar = self._spVar.strip()
        if len(self._spVar) != 0:
            self.specialVar_dropdown.addItem(self._spVar)
            self.dc_specialVar_dropdown.addItem(self._spVar)
            self.dc_specialVar.clear()
        else:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet("QLabel{ color: black}")
            msgbox.setWindowTitle('Empty Variable')
            msgbox.setIcon(msgbox.Warning)
            msgbox.setText("Variable cannot be empty")
            msgbox.exec()
    
    def insertspecialVarDetail(self):
        self.selected = self.dc_specialVar_dropdown.currentText()
        self.selected = self.selected.strip()
        if len(self.selected) != 0:
            self.tmp_condition.append("var " + self.selected + ' = ')
            self.notify['QString', 'QString', int, bool].emit("Don't forget to end with semicolon(;)", "info", 10000, True)
            self.pixmap = QPixmap('alert.png')
            self.icon = QIcon(self.pixmap)
            self._semicom.setIcon(self.icon)
        else:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet("QLabel{ color: black}")
            msgbox.setWindowTitle('Empty name')
            msgbox.setIcon(msgbox.Warning)
            msgbox.setText("There is no valid name to insert")
            msgbox.exec()

    def insertSpecialName(self):
        self.selected = self.specialVar_dropdown.currentText()
        self.selected = self.selected.strip()
        if len(self.selected) != 0:
            self.tmp_condition.insertPlainText(self.selected)
        else:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet("QLabel{ color: black}")
            msgbox.setWindowTitle('Empty Special name')
            msgbox.setIcon(msgbox.Warning)
            msgbox.setText("There is no valid special name to insert")
            msgbox.exec()
        
    def add_routine_tbl(self):
        global rtn
        self.routineName = self.routine_name.text()
        self.routine_ids = self.routine_id.text()
        if self.routineName in rtn or len(self.routine_ids) < 1:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet("QLabel{ color: black}")
            msgbox.setWindowTitle('Error')
            msgbox.setIcon(msgbox.Warning)
            msgbox.setText("Name is duplicated or productID is empty.")
            msgbox.exec()
        else:
            try:
                self.routineName = self.routine_name.text()
                self.routine_ids = self.routine_id.text()
                self.row_number = self.routine_table.rowCount()
                self.routine_table.insertRow(self.row_number) 
                self.routine_table.setItem(self.row_number, 0, QTableWidgetItem(self.routineName))
                self.routine_table.setItem(self.row_number, 1, QTableWidgetItem(self.routine_ids))
                self.routine_table.resizeColumnsToContents()
                self.routine_dropdown.addItem(self.routineName)
                rtn.append(self.routineName)
            except AttributeError as e:
                print(e)
    def tick(self,btn):
        pixmap = QPixmap('tick.png')
        icon = QIcon(pixmap)
        btn.setIcon(icon)
        
    #step 2
    def decleardc(self):
        self.code.append("scores.darkcircle = skin_score.darkcircle;")
        self.tick(self.enable_darkc)
        
    def declearwrink(self):
        self.code.append("scores.wrinkle = skin_score.wrinkle;")
        self.tick(self.enable_wrink)
        
    def declearspot(self):
        self.code.append("scores.spot = skin_score.spot;")
        self.tick(self.enable_spots)
        
    def decleartexture(self):
        self.code.append("scores.texture = skin_score.texture;")
        self.tick(self.enable_texture)
        
    def declearoil(self):
        self.code.append("scores.oilness = skin_score.oilness;")
        self.tick(self.enable_oilness)
        
    def declearredness(self):
        self.code.append("scores.redness = skin_score.redness;")
        self.tick(self.enable_redness)
        
    def declearmoist(self):
        self.code.append("scores.moisture = skin_score.moisture;")
        self.tick(self.enable_moisture)

    def decleareyebag(self):
        self.code.append("scores.eyebag = skin_score.eyebag;")
        self.tick(self.enable_eyebag)
        
    def declearradiance(self):
        self.code.append("scores.radiance = skin_score.radiance;")
        self.tick(self.enable_radiance)
        
    def declearcustomizeCam(self):
        self._consern = self.customize_cam.text()
        self._consern = self._consern.strip()
        if len(self._consern) != 0:
            self.custom_cam_dropdown.addItem(self._consern)
            self.dc_custom_cam_dropdown.addItem(self._consern)
            self.customize_cam.clear()
    def declearcustomizeCamToCode(self):
        self.selected = self.dc_custom_cam_dropdown.currentText()
        self.code.append("scores." + self.selected + " = skin_score." + self.selected + ";")

    def addCustomizeCam(self):
        self.selected = self.custom_cam_dropdown.currentText()
        self.tmp_condition.append("scores." + self.selected + " ")



    #step 3 operator
    def addif(self):
        self.tmp_condition.append("if (")
        self.notify['QString', 'QString', int, bool].emit("Don't forget to CloseIF when complete the logic", "info", 10000, True)

        self.pixmap = QPixmap('alert.png')
        self.icon = QIcon(self.pixmap)
        self._closeif_btn.setIcon(self.icon)

    def addelseif(self):
        self.tmp_condition.append("else if (")
        
        self.notify['QString', 'QString', int, bool].emit("Don't forget to CloseIF when complete the logic", "info", 10000, True)

        self.pixmap = QPixmap('alert.png')
        self.icon = QIcon(self.pixmap)
        self._closeif_btn.setIcon(self.icon)
    def addelse(self):
        self.tmp_condition.append("else (")
    def addLet(self):
        self.tmp_condition.append("let = ")
    def addSwitch(self):
        self.tmp_condition.append("switch (") #switch (asnwers) {}
    def addCase(self):
        self.tmp_condition.append("case: ")
    def addBreak(self):
        self.tmp_condition.append("break;")#case 'Male': {product_ids = [3];break;}
    def addand(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("&& ")
    def addor(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("|| ")
    def addHasAns(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("has_answer(")
        self.notify['QString', 'QString', int, bool].emit("Don't forget to insert survey option", "info", 10000, True)
        self.pixmap = QPixmap('alert.png')
        self.icon = QIcon(self.pixmap)
        self.insert_surveyOption_btn.setIcon(self.icon)

    def insertSurveyOption(self):
        self.selected = self.survey_option_dropdown.currentText() ##可以做个dic，dropbox就可以给给survey名字，然后显示survey名字
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText(self.selected + ") ")
        self.insert_surveyOption_btn.setIcon(QIcon())


    #step 3 concern score
    def addDarkCircle(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("skin_score.darkcircle ")
    def addWrinkles(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("skin_score.wrinkle ")
    def addSpot(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("skin_score.spot ")
    def addTexture(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("skin_score.texture ")
    def addOilness(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("skin_score.oilness ")
    def Addredness(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("skin_score.redness ")
    def addMoisture(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("skin_score.moisture ")
    def addEyebag(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("skin_score.eyebag ")
    def addRadiance(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("skin_score.radiance ")
    def addSkinage(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("skin_score.skinage ")


    #step 3 operator
    def addplus(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("+ ")
    def addminus(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("- ")
    def addtimes(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("* ")
    def adddivide(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("/ ")
    def addequal(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("= ")
    def addequals(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("== ")
    def addgrater(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("> ")
    def addsmaller(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("< ")
    def addgequal(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText(">= ")
    def addsequal(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("<= ")
    def addnotequal(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("!= ")
    def addnot(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("!")
    def addleftbracket(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("( ")
    def addrightbrcket(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText(") ")
    def addsemicom(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("; ")
        self._semicom.setIcon(QIcon())
    def addleftCbracket(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("{ ")
    def addrightCbrcket(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("} ")

    #step 3 numbers    
    def add1(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("1")
    def add2(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("2")
    def add3(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("3")
    def add4(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("4")
    def add5(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("5")
    def add6(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("6")
    def add7(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("7")
    def add8(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("8")
    def add9(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("9")
    def add0(self):
        self.tmp_condition.moveCursor(QTextCursor.End)
        self.tmp_condition.insertPlainText("0")

    #step 3 close if
    def closeif(self):
        self.tmp_condition.insertPlainText("){")
        self._closeif_btn.setIcon(QIcon())

    #step 4 add product ids
    def addtoProductpool(self):
        global _products, tbcount
        self._pid = self.productId_field.text()
        if self._pid.isnumeric() == True:
            _products.append(self._pid)
            self.productId_field.clear()
            self.row_number = self.idList.rowCount()
            self.idList.insertRow(self.row_number) #should clear row and set column name again, should not add empty number
            self.idList.setItem(tbcount,0,QTableWidgetItem(self._pid))
            tbcount = tbcount + 1
        else:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet("QLabel{ color: black}")
            msgbox.setWindowTitle('Invalid ID')
            msgbox.setIcon(msgbox.Warning)
            msgbox.setText("ProductID can only be numbers")
            msgbox.exec()

    def insertProduct(self):
        global _products, tbcount
        self.tmp_condition.append("product_ids = [")
        self.tmp_condition.moveCursor(QTextCursor.End)
        for i in _products:
            self.tmp_condition.insertPlainText(str(i)+ ',')
        cursor = self.tmp_condition.textCursor()
        cursor.deletePreviousChar()
        self.tmp_condition.insertPlainText("];")
        self.tmp_condition.append("}")
        _products.clear()
        self.idList.clear()
        tbcount = 0
        #self.idList.setRowCount(1)
        #self.idList.insertColumn(1)
        self.idList.setHorizontalHeaderLabels(['ID'])

    def insertRtouine(self):
        self.selected = self.routine_dropdown.currentText()
        match = self.routine_table.findItems(self.selected, Qt.MatchExactly)
        if match:
            for i in match:
                print(i.text())
            itemx = match[0].row() #row
            #itemy = match[0].column() #column #indexAt
            print(itemx)
            #print(itemy)
            ids = self.routine_table.item(itemx,1)
            print(ids.text())
            self.tmp_condition.append("product_ids = [" + ids.text() + "];")
            self.tmp_condition.moveCursor(QTextCursor.End)
            self.tmp_condition.append("}")
            
    #Step 5 add to condiDB
    def addToCondiDB(self):
        global condi, condiname
        self.currentcondi = self.tmp_condition.toPlainText()
        self.condiName = self.condi_name.text()
        self.condiName = self.condiName.strip()
        if self.condiName not in condiname and len(self.condiName) != 0:
            condiname.append(self.condiName)
            tmp_condi_dict = {self.condiName : self.currentcondi}
            condi.update(tmp_condi_dict)
            #print(condi)
            #self.condiname.append(self.condiName)
            #self.condiDB_Dropdown.addItem(self.condiName) #用table代替
            self.tmp_condition.clear()
            self.condi_name.clear()
            self.condiTableView()
        else:
            #print(self.condiName)
            #print(condiname)
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet("QLabel{ color: black}")
            msgbox.setWindowTitle('Empty or Duplicated')
            msgbox.setIcon(msgbox.Warning)
            msgbox.setText("Condition name cannot be empty or duplicate")
            msgbox.exec()
        

    def condiPreview(self): #用table代替
        self.pre_condiPreview.clear()
        self.selected = self.condiDB_Dropdown.currentText()
        self.condi_text = condi.get(str(self.selected)) #獲得condi dict中選擇的condition value
        self.pre_condiPreview.append(self.condi_text)
    
    def condiTableView(self):
        _row = 0
        self.condi_tableview.setColumnCount(4)
        self.condi_tableview.setRowCount(len(condiname))
        self.condi_tableview.setSortingEnabled(True)
        self.condi_tableview.setHorizontalHeaderLabels(['Name', 'Insert','Remove','Load']) #delete condi
        
        for i in condiname:
            item = QTableWidgetItem(str(i))
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.condi_tableview.setItem(_row, 0, QTableWidgetItem(item))

            self.insertBtn = QPushButton("Insert")
            self.condi_tableview.setCellWidget(_row, 1, self.insertBtn)
            self.insertBtn.clicked.connect(self.InsertCondi)

            self.deletBtn = QPushButton("Remove")
            self.condi_tableview.setCellWidget(_row, 2, self.deletBtn)
            self.deletBtn.clicked.connect(self.RemoveCondi)

            self.loadBtn = QPushButton("Load")
            self.condi_tableview.setCellWidget(_row, 3, self.loadBtn)
            self.loadBtn.clicked.connect(self.loadCondi)

            #self.delBtn = QPushButton("Delet")
            #self.condi_tableview.setCellWidget(_row, 4, self.delBtn)
            #self.delBtn.clicked.connect(self.delCondi)

            _row = _row + 1

        self.condi_tableview.resizeColumnsToContents()
        self.condi_tableview.resizeRowsToContents()
        

    #Step 6 Complete JS
    def InsertCondi(self):
        global condi
        #self.selected = self.condiDB_Dropdown.currentText() #以dropdown來查詢并選擇添加，後續改成讀取table
        buttonClicked = self.sender()  #添加信號
        index = self.condi_tableview.indexAt(buttonClicked.pos()) #獲得按鈕點擊index
        self._value_row = index.row() #index即row
        self._condiNameValue = self.condi_tableview.item(self._value_row, 0) #獲取table第0的name值
        #print(self._condiNameValue.text())
        self.selectedStart = "/*" + self._condiNameValue.text() + "*/"
        self.selectedEnd = "/*end" + self._condiNameValue.text() + "*/"
        self.condi_text = condi.get(str(self._condiNameValue.text())) #獲得condi dict中選擇的condition value

        self.code.append(str(self.selectedStart)) #添加開始標識符
        self.code.append(self.condi_text) #添加condition value
        self.code.append(str(self.selectedEnd)) #添加結尾標識符

    def RemoveCondi(self):
        #self.selected = self.condiDB_Dropdown.currentText()
        buttonClicked = self.sender()  #添加信號
        index = self.condi_tableview.indexAt(buttonClicked.pos()) #獲得按鈕點擊index
        self._value_row = index.row() #index即row
        self._condiNameValue = self.condi_tableview.item(self._value_row, 0) #獲取table第0的name值

        self.currentcondi = self.code.toPlainText() #get .code's all text
        #/\W1*\W/\W(.|\n)*?/\W*\Wend1*\W/   1,2,3的話好像都會誤刪
        #/..2../(.|\n)*?/..end2../
        self.rule = "/\W" + self._condiNameValue.text() + r"*\W/\W(.|\n)*?/\W*\Wend" + self._condiNameValue.text() + "*\W/"
        self.rule2 = "/." + self._condiNameValue.text() + r"./(.|\n)*?/.end" + self._condiNameValue.text() + "./"
        #print(self.rule)
        #print(self.currentcondi)
        self.removed_condi = re.sub(self.rule2, '', self.currentcondi)
        #print(self.removed_condi)
        self.code.clear()
        self.code.append(self.removed_condi)

    def loadCondi(self):
        buttonClicked = self.sender()  #添加信號
        index = self.condi_tableview.indexAt(buttonClicked.pos()) #獲得按鈕點擊index
        self._value_row = index.row() #index即row
        self._condiNameValue = self.condi_tableview.item(self._value_row, 0) #獲取table第0的name值
        self.condi_text = condi.get(str(self._condiNameValue.text())) #獲取字典内存儲的condition
        
        self.existing_text = self.tmp_condition.toPlainText() #get current text
        if len(self.existing_text) == 0: #check if anything in, pop up warning
            self.tmp_condition.append(self.condi_text)
        else:
            reply = QMessageBox.warning(self, 'Unfinished Condition', 'You have condition inside the editor, do you want to overwrite it',QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
            '''
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet("QLabel{ color: black}")
            msgbox.setWindowTitle('Unfinished Condition')
            msgbox.setIcon(msgbox.Warning)
            msgbox.setText("You have condition inside the editor, do you want to overwrite it?")
            msgbox.setStandardButtons(msgbox.Ok | msgbox.Close)
            '''
            if reply == QMessageBox.Ok:
                #print(self._condiNameValue.text())
                #print(self.condi_text)
                self.tmp_condition.clear()
                self.tmp_condition.append(self.condi_text)
            else:
                pass
            #msgbox.exec()

    def complete(self):
        self.code.append("return wrap_result(product_ids, oem_attrs, extra_info);\n}")
    def nicee(self):
        ugly = self.code.toPlainText()
        res = jsbeautifier.beautify(ugly)
        #res = jsbeautifier.beautify_file('some_file.js')
        self.code.setText(res)
    def help(self):
        self.popmainWindow = popdisplay()
        self.popmainWindow.show()
    def cleartmpCondi(self):
        reply = QMessageBox.critical(self, 'Clear', 'You have condition inside the editor, do you want to remove all? This action cannot be revert',QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
        if reply == QMessageBox.Ok:
            self.tmp_condition.clear()
        else:
            pass
    def saveConfig(self):
        global survey_count, option_count, option, option_ans, condiname, condi

        
        configName = self.settingNameField.text()

        #get existing values
        dcOptions = [self.dcOption_dropDown.itemText(i) for i in range(self.dcOption_dropDown.count())] #get list items
        dcOptionAns = [self.dcOptionAns_dropDown.itemText(i) for i in range(self.dcOptionAns_dropDown.count())]
        extraInfo = [self.extraInfo_dropdown.itemText(i) for i in range(self.extraInfo_dropdown.count())]
        dc_specialVar = [self.dc_specialVar_dropdown.itemText(i) for i in range(self.dc_specialVar_dropdown.count())]
        custom_cam = [self.custom_cam_dropdown.itemText(i) for i in range(self.custom_cam_dropdown.count())]
        survey_option = [self.survey_option_dropdown.itemText(i) for i in range(self.survey_option_dropdown.count())]
        survey_ans = [self.survey_ans_dropdown.itemText(i) for i in range(self.survey_ans_dropdown.count())]
        extraInfoName = [self.extraInfoName_dropdown.itemText(i) for i in range(self.extraInfoName_dropdown.count())]
        specialVar = [self.specialVar_dropdown.itemText(i) for i in range(self.specialVar_dropdown.count())]
        tmpCode = self.tmp_condition.toPlainText()
        finalCode = self.code.toPlainText()
        #print(dcOptions)
        survey_count2Int = int(survey_count)  #changed to str in above, change back to int


        file_exists = os.path.exists(configName + '.pickle')
        if file_exists:
            _warning = QMessageBox.question(self, 'Config Exist', 'Config name already exist.\nDo you want overwrite?',QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
            if _warning == QMessageBox.Ok:
                with open(configName + '.pickle', 'wb') as f:
                    pickle.dump(survey_count2Int, f, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(option_count, f, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(dcOptions, f, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(dcOptionAns, f, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(extraInfo, f, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(dc_specialVar, f, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(custom_cam, f, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(survey_option, f, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(survey_ans, f, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(extraInfoName, f, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(specialVar, f, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(condiname, f, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(condi, f, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(tmpCode, f, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(finalCode, f, pickle.HIGHEST_PROTOCOL)
                            
                    '''
                    f.write('survey_count = ' + repr(survey_count) + "\n" + \
                        'option_count = ' + repr(option_count) + "\n" + \
                        'option = ' + repr(option) + "\n" + \
                        'option_ans = ' + repr(option_ans) + "\n" + \
                        'condiname = ' + repr(condiname) + "\n" + \
                        'condi = ' + repr(condi) + "\n" \
                        
                        'dcOption_dropDown = ' + repr(dcOptions) + "\n" + \
                        'dcOptionAns_dropDown = ' + repr(dcOptionAns) + "\n" + \
                        'extraInfo_dropdown = ' + repr(extraInfo) + "\n" + \
                        'dc_specialVar_dropdown = ' + repr(dc_specialVar) + "\n" + \
                        'custom_cam_dropdown = ' + repr(custom_cam) + "\n" + \
                        'survey_option_dropdown = ' + repr(survey_option) + "\n" + \
                        'survey_ans_dropdown = ' + repr(survey_ans) + "\n" + \
                        'extraInfoName_dropdown = ' + repr(extraInfoName) + "\n" + \
                        'specialVar_dropdown = ' + repr(specialVar) + "\n" + \
                        'tmp_condition = ' + repr(tmpCode) + "\n" + \
                        'code = ' + repr(finalCode))\
                    '''
                    self.notify['QString', 'QString', int, bool].emit('Config saved as\n' + configName + '.pickle', 'success', 5000, True)
            else:
                self.notify['QString', 'QString', int, bool].emit('Config not saved', 'warning', 5000, True)
                pass
        else:
            with open(configName + '.pickle', 'wb') as f:
                pickle.dump(survey_count2Int, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(option_count, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(dcOptions, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(dcOptionAns, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(extraInfo, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(dc_specialVar, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(custom_cam, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(survey_option, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(survey_ans, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(extraInfoName, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(specialVar, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(condiname, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(condi, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(tmpCode, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(finalCode, f, pickle.HIGHEST_PROTOCOL)

                ''' #这个还要加global给下面load func用 有点麻烦
                https://blog.csdn.net/coffee_cream/article/details/51754484
                psci = pickle.dumps(survey_count2Int)
                poc = pickle.dumps(option_count)
                po = pickle.dumps(option)
                poa = pickle.dumps(option_ans)
                pcn = pickle.dumps(condiname)
                pc = pickle.dumps(condi)
                pdo = pickle.dumps(dcOptions)
                pdoa = pickle.dumps(dcOptionAns)
                pdsv = pickle.dumps(dc_specialVar)
                pei = pickle.dumps(extraInfo)
                pcc = pickle.dumps(custom_cam)
                pso = pickle.dumps(survey_option)
                psa = pickle.dumps(survey_ans)
                pein = pickle.dumps(extraInfoName)
                psv = pickle.dumps(specialVar)
                ptc = pickle.dumps(tmpCode)
                pfc = pickle.dumps(finalCode)
                '''
            
                
            
            '''
            with open(configName + ".txt", 'w') as f:
                f.write(repr(survey_count2Int) + "\n" + \
                    repr(option_count) + "\n" + \
                    repr(option) + "\n" + \
                    repr(option_ans) + "\n" + \
                    repr(condiname) + "\n" + \
                    repr(condi) + "\n" + \
                    repr(dcOptions) + "\n" + \
                    repr(dcOptionAns) + "\n" + \
                    repr(extraInfo) + "\n" + \
                    repr(dc_specialVar) + "\n" + \
                    repr(custom_cam) + "\n" + \
                    repr(survey_option) + "\n" + \
                    repr(survey_ans) + "\n" + \
                    repr(extraInfoName) + "\n" + \
                    repr(specialVar) + "\n" + \
                    repr(tmpCode) + "\n" + \
                    repr(finalCode))
            '''
            '''
                f.write('survey_count = ' + repr(survey_count) + "\n" + 
                        'option_count = ' + repr(option_count) + "\n" + 
                        'option = ' + repr(option) + "\n" + 
                        'option_ans = ' + repr(option_ans) + "\n" + 
                        'condiname = ' + repr(condiname) + "\n" + 
                        'condi = ' + repr(condi) + "\n"
                        
                        'dcOption_dropDown = ' + repr(dcOptions) + "\n" + 
                        'dcOptionAns_dropDown = ' + repr(dcOptionAns) + "\n" + 
                        'extraInfo_dropdown = ' + repr(extraInfo) + "\n" + 
                        'dc_specialVar_dropdown = ' + repr(dc_specialVar) + "\n" + 
                        'custom_cam_dropdown = ' + repr(custom_cam) + "\n" + 
                        'survey_option_dropdown = ' + repr(survey_option) + "\n" + 
                        'survey_ans_dropdown = ' + repr(survey_ans) + "\n" + 
                        'extraInfoName_dropdown = ' + repr(extraInfoName) + "\n" + 
                        'specialVar_dropdown = ' + repr(specialVar) + "\n" + 

                        'tmp_condition = ' + repr(tmpCode) + "\n" +
                        'code = ' + repr(finalCode))
            '''
            self.notify['QString', 'QString', int, bool].emit('Config saved as\n' + configName + '.pickle', 'success', 5000, True)

    def loadConfig(self):
        global survey_count, option_count, option, option_ans, condiname, condi
        
        configName = self.settingNameField.text()
        file_exists = os.path.exists(configName + '.pickle')
        if file_exists:
            _warning = QMessageBox.warning(self, 'Load Config', 'Load other config will overwrite existing values. Once overwrite there is no revert.\nDo you want load?',QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
            if _warning == QMessageBox.Ok:                
                self.notify['QString', 'QString', int, bool].emit("Loaded", "success", 10000, True)
                
                #remove all code * 2
                self.tmp_condition.clear()
                self.code.clear()
                #remove table * 1
                self.condi_tableview.clear() 

                #remove PIDlist * 1
                self.idList.clear() ##這個失敗

                #remove droplist * 9
                self.dcOption_dropDown.clear()
                self.dcOptionAns_dropDown.clear()
                self.extraInfo_dropdown.clear()
                self.dc_specialVar_dropdown.clear()
                self.custom_cam_dropdown.clear()
                self.survey_option_dropdown.clear()
                self.survey_ans_dropdown.clear()
                self.extraInfoName_dropdown.clear()
                self.specialVar_dropdown.clear()
                
                #remove text fileds
                self.dc_qIdField.clear()
                self.dc_qAns.clear()
                self.extra_nameField.clear()
                self.dc_specialVar.clear()
                self.customize_cam.clear()
                self.freeTextBox.clear()
                self.productId_field.clear()
                self.condi_name.clear()
                self.settingNameField.clear()

                
                #path = r'C:\Users\Administrator\Desktop\Work\pfu\skincare_js'
                #fr = open(path +'\\' + configName + '.pickle','rb')
                fr = open(configName + '.pickle','rb')
                survey_count = pickle.load(fr)
                self.count_survey.setText(str(survey_count))
                option_count = pickle.load(fr)

                #option = pickle.load(fr)
                data = pickle.load(fr) #偷個懶
                for i in data: self.dcOption_dropDown.addItem(i) #沒法直接用addsurvey func啊。。。以後再改
                #option_ans = pickle.load(fr)
                data = pickle.load(fr)
                for i in data: self.dcOptionAns_dropDown.addItem(i)
                #dc_extraInfo = pickle.load(fr)
                data = pickle.load(fr)
                for i in data: self.extraInfo_dropdown.addItem(i)
                data = pickle.load(fr)
                for i in data: self.dc_specialVar_dropdown.addItem(i)
                data = pickle.load(fr)
                for i in data: self.custom_cam_dropdown.addItem(i)
                data = pickle.load(fr)
                for i in data: self.survey_option_dropdown.addItem(i)
                data = pickle.load(fr)
                for i in data: self.survey_ans_dropdown.addItem(i)
                data = pickle.load(fr)
                for i in data: self.extraInfoName_dropdown.addItem(i)
                data = pickle.load(fr)
                for i in data: self.specialVar_dropdown.addItem(i)
                condiname = pickle.load(fr) #填回condiname的list
                self.condiTableView() #舒服 直接func
                condi = pickle.load(fr) #填回condi的dict
                data = pickle.load(fr) #tmp code
                self.tmp_condition.append(data)
                data = pickle.load(fr) #final code
                #print(data)
                self.code.append(data)
                self.nicee()

            else:
                pass
        else:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setStyleSheet("QLabel{ color: black}")
            msgbox.setWindowTitle('File not exist')
            msgbox.setIcon(msgbox.Warning)
            msgbox.setText("The file does not exist.")
            msgbox.exec()
            
            
    def advanced(self):
        self.insert_elseif.show()
        self._letbtn.show()
        self._elsebtn.show()
        self.switchBtn.show()
        self.caseBtn.show()
        self.BreakBtn.show()
        self._left_bracket.show()
        self._right_bracket.show()
        self._left_curlybracket.show()
        self._right_curlybracket.show()
        #self.next_surveyBtn_2.show()
        #self._closeif_btn_2.show()
        self._semicom.show()
        #exinfoname
        self.label_4.show()
        self.code_5.show()
        self.extra_nameField.show()
        self.dc_extraInfoBtn.show()
        self.code_6.show()
        self.extraInfo_dropdown.show()
        self.decear_extrainfo_btn.show()
        self.line_5.show()
        #specname
        self.label_10.show()
        self.code_12.show()
        self.dc_specialVar.show()
        self.dc_specialVarBtn.show()
        self.code_10.show()
        self.dc_specialVar_dropdown.show()
        self.dc_specialVarDetailBtn.show()

    def validate(self):
        testdata = {
            "detectResult": self.skin_scores.toPlainText(),
            "script": self.code.toPlainText(),
            "surveyOptions": self.survey_result.toPlainText()
        }
        #print(testdata['detectResult'])
        #print(testdata['script'])
        #print(testdata['surveyOptions'])
        try:
            self.url = 'http://k8s-bc-scrdemoi-7ee69197d0-713182356.ap-northeast-1.elb.amazonaws.com/store-backend/recommendation/validate-js.action'
            self.HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
            x = requests.post(self.url, headers=self.HEADERS, data = testdata)
            self.checker_output.setText(x.text)
            #print(x.text)
        except KeyError:
            print("error")
            pass


def au():
    print("Token is" + _token)
    print(cmsdata)

class popdisplay(QWidget):
    def __init__(self):
        super(popdisplay, self).__init__()
        loadUi("help.ui",self)

#main

app = QApplication(sys.argv)
#apply_stylesheet(app, theme='light_purple.xml')
#welcome = MainUi() remove login UNcomment加回login
welcome = LoginScreen()
#widget = QStackedWidget()
#widget.setWindowTitle("Skincare Logic")
#widget.addWidget(welcome)
#console = pfconsole.MainWindow()
#widget.addWidget(console)
#welcome.setMaximumWidth(1600)
#welcome.setMaximumHeight(800)
welcome.setMinimumWidth(1600)
welcome.setMinimumHeight(900)
#welcome.setWindowFlag(Qt.FramelessWindowHint)  remove login UNcomment加回login
#welcome.setAttribute(Qt.WA_TranslucentBackground) remove login UNcomment加回login
welcome.show()
#widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exit")
