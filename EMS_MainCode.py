from PyQt5 import QtCore,QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import MySQLdb
from PyQt5.uic import loadUiType
import datetime
import re
from datetime import datetime
from PyQt5 import QtPrintSupport
import urllib.request
import time
import threading
from EMS_GUI_Code import Ui_S1_Designation
Qt = QtCore.Qt

#ui, _ = loadUiType('emsgui.ui')


def start():
    global m
    m = Main_Window()
    m.connect()
    m.show()
    


def ConnectDatabase():
    try:
        global cur
        global conn
        conn = MySQLdb.connect(host='emsdatabase.cihtsb96tcbg.ap-south-1.rds.amazonaws.com', user='mainbanda',
                               password='mainbanda', db='EMS_DB')
        cur = conn.cursor()
        print("db connected")
    except:
        print("not connected")





def generateid(v):
    c = v
    ids = ""
    cur.execute('''select * from ids''')
    data = cur.fetchall()
    for row in data:
        if (row[0] == c):
            ids = row[1]
            break
    if (ids == ""):
        print("Variable entered is not present in the table")
    else:
        s = re.search(r"\d+(\.\d+)?", ids)
        n = int(s.group(0))

        n += 1
        num = str(n).zfill(3)  # fromdb
        final_id = c + num
        # print(final_id)
    return final_id


ch1 = 'X'    #for User Type
ch = 'X'     #for Table
Userid='U999'
cur = {}
conn = {}
_list = set()
v = []
p_index = -1
_list_2 = set()
v_2 = []

class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()


class Choose_Designation(QMainWindow, QWidget, Ui_S1_Designation):
    def __init__(self):
        QMainWindow.__init__(self)
        QWidget.__init__(self)
        self.setupUi(self)
        self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView { font: bold 18px; }");
        self.ViewTablePrint.horizontalHeader().setStyleSheet("QHeaderView { font: bold 18px; }");
        self.ViewTable.horizontalHeader().setStyleSheet("QHeaderView { font: bold 18px; }");
        self.update_tableWidget.horizontalHeader().setStyleSheet("QHeaderView { font: bold 18px; }");

        self.stackedWidget.setCurrentIndex(0)

        if ((self.stackedWidget.currentIndex() == 0) or (self.stackedWidget.currentIndex() == 1)):
            self.signout_button.setVisible(False)
            self.changepass_button.setVisible(False)
            self.myprofile_button.setVisible(False)

        self.Handel_Buttons()

    def DeleteTableView(self, datain, headerdata, tableW):
        self.arraydata = datain
        rows = len(self.arraydata)
        columns = len(self.arraydata[0])
        self.table = tableW
        print(rows, columns)
        # self.table = tableW(self)
        self.table.setRowCount(rows)
        self.table.setColumnCount(columns)
        # self.table = QTableWidget(rows, columns, self)
        self.table.setHorizontalHeaderLabels(headerdata)
        rowNo = 0
        for line in self.arraydata:
            colNo = 0
            for col in line:
                if (type(col) == type(1)):
                    if colNo == 0:
                        oneitem = QTableWidgetItem()
                        oneitem.setData(Qt.EditRole, col)
                        oneitem.setTextAlignment(Qt.AlignCenter)
                        oneitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        oneitem.setCheckState(QtCore.Qt.Unchecked)

                    else:
                        oneitem = QTableWidgetItem()
                        oneitem.setData(Qt.EditRole, col)
                        oneitem.setTextAlignment(Qt.AlignCenter)
                else:
                    if colNo == 0:
                        oneitem = QTableWidgetItem(col)
                        oneitem.setTextAlignment(Qt.AlignCenter)
                        oneitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        oneitem.setCheckState(QtCore.Qt.Unchecked)

                    else:
                        oneitem = QTableWidgetItem(col)
                        oneitem.setTextAlignment(Qt.AlignCenter)

                self.table.setItem(rowNo, colNo, oneitem)
                colNo += 1
            rowNo += 1

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

        self.table.itemClicked.connect(self.handleItemClicked)


    def handleItemClicked(self, item):
        if (self.table == self.tableWidget):
            if item.column() == 0:
                if item.checkState() == QtCore.Qt.Checked:
                    # print('"%s" Checked' % item.text())
                    # QTableWidgetSelectionRange(1,1,1,1)
                    _list.add(item.text())
                    # print(_list)
                elif item.checkState() == QtCore.Qt.Unchecked:
                    # print('"%s" Unchecked' % item.text())
                    if item.text() in _list:
                        _list.remove(item.text())
                    # print(_list)
                else:
                    w = 0
                    # print('"%s" Clicked' % item.text())
        elif (self.table == self.update_tableWidget):
            if item.column() == 0:
                if item.checkState() == QtCore.Qt.Checked:
                    # print('"%s" Checked' % item.text())
                    # QTableWidgetSelectionRange(1,1,1,1)
                    _list.add(item.text())
                    v.append(item.row())
                    # print(_list,v)

                elif item.checkState() == QtCore.Qt.Unchecked:
                    # print('"%s" Unchecked' % item.text())
                    if item.text() in _list:
                        _list.remove(item.text())
                        v.remove(item.row())
                    # print(_list,v)
                else:
                    w = 0
                    # print('"%s" Clicked' % item.text())
                # print(_list, v)

               # print(len(_list))
                if (len(_list) == 2):
                    # print('ds')
                    self.table.item(list(v)[0], 0).setCheckState(QtCore.Qt.Unchecked)
                    # print(self.table.item(list(v)[0], 0).text())
                    _list.remove(self.table.item(list(v)[0], 0).text())
                    v.remove(self.table.item(list(v)[0], 0).row())
                    print(_list, v)
    def DeleteTableView_2(self, datain, headerdata, tableW):
        self.arraydata = datain
        rows = len(self.arraydata)
        columns = len(self.arraydata[0])
        self.table = tableW
        #print(rows, columns)
        # self.table = tableW(self)
        self.table.setRowCount(rows)
        self.table.setColumnCount(columns)
        # self.table = QTableWidget(rows, columns, self)
        self.table.setHorizontalHeaderLabels(headerdata)
        rowNo = 0
        for line in self.arraydata:
            colNo = 0
            for col in line:
                if (type(col) == type(1)):
                    if colNo == 0:
                        oneitem = QTableWidgetItem()
                        oneitem.setData(Qt.EditRole, col)
                        oneitem.setTextAlignment(Qt.AlignCenter)
                        oneitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        oneitem.setCheckState(QtCore.Qt.Unchecked)

                    else:
                        oneitem = QTableWidgetItem()
                        oneitem.setData(Qt.EditRole, col)
                        oneitem.setTextAlignment(Qt.AlignCenter)
                else:
                    if colNo == 0:
                        oneitem = QTableWidgetItem(col)
                        oneitem.setTextAlignment(Qt.AlignCenter)
                        oneitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        oneitem.setCheckState(QtCore.Qt.Unchecked)

                    else:
                        oneitem = QTableWidgetItem(col)
                        oneitem.setTextAlignment(Qt.AlignCenter)

                self.table.setItem(rowNo, colNo, oneitem)
                colNo += 1
            rowNo += 1

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        
        self.table.itemClicked.connect(self.handleItemClicked_2)


    def handleItemClicked_2(self, item):
        global v_2
        global _list_2
        if (self.table == self.tableWidget):
            if item.column() == 0:
                if item.checkState() == QtCore.Qt.Checked:
                    # print('"%s" Checked' % item.text())
                    # QTableWidgetSelectionRange(1,1,1,1)
                    _list_2.add(item.text())
                    # print(_list)
                elif item.checkState() == QtCore.Qt.Unchecked:
                    # print('"%s" Unchecked' % item.text())
                    if item.text() in _list_2:
                        _list_2.remove(item.text())
                    # print(_list)
                else:
                    w = 0
                    # print('"%s" Clicked' % item.text())
        elif (self.table == self.update_tableWidget):
            if item.column() == 0:
                if item.checkState() == QtCore.Qt.Checked:
                    # print('"%s" Checked' % item.text())
                    # QTableWidgetSelectionRange(1,1,1,1)
                    _list_2.add(item.text())
                    v_2.append(item.row())
                    print("line 186",_list_2,v_2)

                elif item.checkState() == QtCore.Qt.Unchecked:
                    # print('"%s" Unchecked' % item.text())
                    if item.text() in _list_2:
                        _list_2.remove(item.text())
                        v_2.remove(item.row())
                    print("line 193",_list_2,v_2)
                else:
                    w = 0
                    # print('"%s" Clicked' % item.text())
                # print(_list, v)
                
                # print(len(_list))
                if (len(_list_2) == 2):
                    # print('ds')
                    self.table.item(list(v_2)[0], 0).setCheckState(QtCore.Qt.Unchecked)
                    # print(self.table.item(list(v)[0], 0).text())
                    _list_2.remove(self.table.item(list(v_2)[0], 0).text())
                    v_2.remove(self.table.item(list(v_2)[0], 0).row())

                    #v.remove(list(v)[0])
                    #v.pop(0)
                    #del v[1]
                    print("Line 204",_list_2, v_2)

    def Handel_Buttons(self):
        self.pushButton_ok.clicked.connect(self.addItemInComboBox_designation)

    def addItemInComboBox_designation(self):  # pushButton_ok
        cur.execute('''SELECT * FROM EMS_DB.Users''')
        data = cur.fetchall()
        # print(data)
        for row in data:
            if (row[2] == 'Admin'):
                if (self.comboBox_designation.currentText() == "Admin"):
                    self.comboBox_input_username.addItem(row[0])
                    self.stackedWidget.setCurrentIndex(1)
            elif (row[2] == 'Receptionist'):

                if (self.comboBox_designation.currentText() == "Receptionist"):
                    self.comboBox_input_username.addItem(row[0])
                    self.stackedWidget.setCurrentIndex(1)
            elif (row[2] == 'Staff Manager'):

                if (self.comboBox_designation.currentText() == "Staff Manager"):
                    self.comboBox_input_username.addItem(row[0])
                    self.stackedWidget.setCurrentIndex(1)
            elif (row[2] == 'Event Manager'):

                if (self.comboBox_designation.currentText() == "Event Manager"):
                    self.comboBox_input_username.addItem(row[0])
                    self.stackedWidget.setCurrentIndex(1)
            elif (row[2] == 'Inventory Manager'):

                if (self.comboBox_designation.currentText() == "Inventory Manager"):
                    self.comboBox_input_username.addItem(row[0])
                    self.stackedWidget.setCurrentIndex(1)

            else:
                QMessageBox.warning(self, "User Type Selection", "choose any one designation")



class Login(Choose_Designation):
    def __init__(self):
        Choose_Designation.__init__(self)

    def Handel_Buttons_Login(self):
        self.pushButton_7.clicked.connect(self.Login)
        self.loginpage_backbutton.clicked.connect(self.BackButtonfunction_login)

    def Login(self):  # pushButton_7(login button)
        username = self.comboBox_input_username.currentText()  # 'A001'
        password = self.lineEdit_input_password.text()  # 'utkarsh'

        if (username and password):
            cur.execute('''SELECT * FROM EMS_DB.Users''')
            data = cur.fetchall()
            c = 0
            for row in data:
                if (username == row[0] and password == row[3]):
                    # print('user match')
                    type = row[2]
                    global ch1
                    ch1 = type[:1]
                    global Userid
                    Userid=row[0]
                    c += 1
                    if (ch1):  # this function can be optimized using loops and list
                        QMessageBox.information(self, "Login Status", "you are logged in successfully")
                        if (ch1 == 'A'):
                            self.stackedWidget.setCurrentIndex(2)
                        elif (ch1 == 'R'):
                            self.stackedWidget.setCurrentIndex(5)
                        elif (ch1 == 'S'):
                            self.stackedWidget.setCurrentIndex(3)
                        elif (ch1 == 'E'):
                            self.stackedWidget.setCurrentIndex(6)
                        elif (ch1 == 'I'):
                            self.stackedWidget.setCurrentIndex(4)
                        else:
                            QMessageBox.information(self, "Login Status", "This user does not have a designation")
                    break;
            if (c == 0):
                QMessageBox.information(self, "Login Status", "username or password entered is incorrect")

        else:
            QMessageBox.warning(self, "Login Status", "Either Username or password is Empty")

        #self.comboBox_input_username.clearEditText()
        #self.lineEdit_input_password.clear()
        #self.comboBox_input_username.clear()
        #  self.lineEdit_input_password.clear()

        if ((self.stackedWidget.currentIndex() is not 0) and (self.stackedWidget.currentIndex() is not 1)):
            self.signout_button.setVisible(True)
            self.changepass_button.setVisible(True)
            self.myprofile_button.setVisible(True)

    def BackButtonfunction_login(self):  # loginpage_backbutton
        self.comboBox_input_username.clearEditText()
        self.lineEdit_input_password.clear()
        self.comboBox_input_username.clear()
        self.stackedWidget.setCurrentIndex(0)

class Tableoptions(Login):
    def __init__(self):
        Login.__init__(self)
        Login.Handel_Buttons_Login(self)

    def Handel_Buttons_Afterlogin(self):
        self.user_login_table_backbutton.clicked.connect(self.backbuttonfunction_tableoptions)

    def backbuttonfunction_tableoptions(self):  # user_login_table_backbutton
        if (ch1 == 'A'):
            self.stackedWidget.setCurrentIndex(2)
        elif (ch1 == 'R'):
            self.stackedWidget.setCurrentIndex(5)
        elif (ch1 == 'S'):
            self.stackedWidget.setCurrentIndex(3)
        elif (ch1 == 'E'):
            self.stackedWidget.setCurrentIndex(6)
        elif (ch1 == 'I'):
            self.stackedWidget.setCurrentIndex(4)
        else:
            QMessageBox.warning(self, "ERROR",
                                "No User is choosed before (in designation screen), which can't be happen")


class Receptionst(Tableoptions):
    def __init__(self):
        Tableoptions.__init__(self)
        Tableoptions.Handel_Buttons_Afterlogin(self)

    def Handel_Buttons_Receptionist(self):
        self.R_login_eventbutton.clicked.connect(self.fn_R_login_eventbutton)
        self.R_login_clientbutton.clicked.connect(self.fn_R_login_clientbutton)

    def fn_R_login_eventbutton(self):  # R_login_eventbutton
        global ch
        ch = 'E'
        self.stackedWidget.setCurrentIndex(7)

    def fn_R_login_clientbutton(self):  # R_login_clientbutton
        global ch
        ch = 'C'
        self.stackedWidget.setCurrentIndex(7)

class Admin(Tableoptions):
    def __init__(self):
        Tableoptions.__init__(self)
        Tableoptions.Handel_Buttons_Afterlogin(self)

    def Handel_Buttons_Admin(self):
        self.admin_login_eventbutton.clicked.connect(self.fn_admin_login_eventbutton)
        self.admin_login_userbutton.clicked.connect(self.fn_admin_login_userbutton)
        self.admin_login_staffbutton.clicked.connect(self.fn_admin_login_staffbutton)
        self.admin_login_inventorybutton.clicked.connect(self.fn_admin_login_inventorybutton)
        self.admin_login_venuebutton.clicked.connect(self.fn_admin_login_venuebutton)
        self.admin_login_clientbutton.clicked.connect(self.fn_admin_login_clientbutton)

        self.admin_login_table_backbutton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

    def fn_admin_login_eventbutton(self):  # admin_login_eventbutton
        global ch
        ch = 'E'
        self.stackedWidget.setCurrentIndex(7)

    def fn_admin_login_userbutton(self):  # admin_login_userbutton
        global ch
        ch = 'U'
        self.stackedWidget.setCurrentIndex(8)

    def fn_admin_login_staffbutton(self):  # admin_login_staffbutton
        global ch
        ch = 'S'
        self.stackedWidget.setCurrentIndex(7)

    def fn_admin_login_inventorybutton(self):  # admin_login_inventorybutton
        global ch
        ch = 'I'
        self.stackedWidget.setCurrentIndex(7)

    def fn_admin_login_venuebutton(self):  # admin_login_venuebutton
        global ch
        ch = 'V'
        self.stackedWidget.setCurrentIndex(7)

    def fn_admin_login_clientbutton(self):  # admin_login_clientbutton
        global ch
        ch = 'C'
        self.stackedWidget.setCurrentIndex(7)

class EventManager(Tableoptions):
    def __init__(self):
        Tableoptions.__init__(self)
        Tableoptions.Handel_Buttons_Afterlogin(self)

    def Handel_Buttons_EventManger(self):
        self.EM_login_eventbutton.clicked.connect(self.fn_EM_login_eventbutton)
        self.EM_login_staffbutton.clicked.connect(self.fn_EM_login_staffbutton)
        self.EM_login_inventorybutton.clicked.connect(self.fn_EM_login_inventorybutton)
        self.EM_login_venuebutton.clicked.connect(self.fn_EM_login_venuebutton)

        self.EM_viewpage_backbutton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(6))

    def fn_EM_login_eventbutton(self):  # EM_login_eventbutton
        global ch
        ch = 'E'
        self.stackedWidget.setCurrentIndex(25)

    def fn_EM_login_staffbutton(self):  # EM_login_staffbutton
        global ch
        ch = 'S'
        self.stackedWidget.setCurrentIndex(25)

    def fn_EM_login_inventorybutton(self):  # EM_login_inventorybutton
        global ch
        ch = 'I'
        self.stackedWidget.setCurrentIndex(25)

    def fn_EM_login_venuebutton(self):  # EM_login_venuebutton
        global ch
        ch = 'V'
        self.stackedWidget.setCurrentIndex(25)

class StaffManager(Tableoptions):
    def __init__(self):
        Tableoptions.__init__(self)
        Tableoptions.Handel_Buttons_Afterlogin(self)

    def Handel_Buttons_StaffManager(self):
        self.staff_login_eventbutton.clicked.connect(self.fn_staff_login_eventbutton)
        self.staff_login_staffbutton.clicked.connect(self.fn_staff_login_staffbutton)

    def fn_staff_login_eventbutton(self):  # staff_login_eventbutton
        global ch
        ch = 'E'
        self.stackedWidget.setCurrentIndex(7)

    def fn_staff_login_staffbutton(self):  # staff_login_staffbutton
        global ch
        ch = 'S'
        self.stackedWidget.setCurrentIndex(7)

class InventoryManager(Tableoptions):
    def __init__(self):
        Tableoptions.__init__(self)
        Tableoptions.Handel_Buttons_Afterlogin(self)

    def Handel_Buttons_InventoryManager(self):
        self.Inventory_login_eventbutton.clicked.connect(self.fn_Inventory_login_eventbutton)
        self.Inventory_login_inventorybutton.clicked.connect(self.fn_Inventory_login_inventorybutton)

    def fn_Inventory_login_eventbutton(self):  # Inventory_login_eventbutton
        global ch
        ch = 'E'
        self.stackedWidget.setCurrentIndex(7)

    def fn_Inventory_login_inventorybutton(self):  # Inventory_login_inventorybutton
        global ch
        ch = 'I'
        self.stackedWidget.setCurrentIndex(7)


class User(Admin,Receptionst,EventManager,StaffManager,InventoryManager):
    def __init__(self):
        Admin.__init__(self)
        Receptionst.__init__(self)
        EventManager.__init__(self)
        StaffManager.__init__(self)
        InventoryManager.__init__(self)

        Admin.Handel_Buttons_Admin(self)
        Receptionst.Handel_Buttons_Receptionist(self)
        EventManager.Handel_Buttons_EventManger(self)
        StaffManager.Handel_Buttons_StaffManager(self)
        InventoryManager.Handel_Buttons_InventoryManager(self)


class Add(User):
    def __init__(self):
        User.__init__(self)

    def Handel_Buttons_Add(self):
        self.user_login_table_addbutton.clicked.connect(self.onClickAddButton)
        self.admin_login_table_createuserbutton.clicked.connect(self.onClickAddButton)

        #Submit button
        self.Event_submit.clicked.connect(self.addFormSubmitButton)
        self.pushButton_2.clicked.connect(self.addFormSubmitButton)
        self.pushButton_3.clicked.connect(self.addFormSubmitButton)
        self.pushButton_4.clicked.connect(self.addFormSubmitButton)
        self.pushButton_5.clicked.connect(self.addFormSubmitButton)
        self.pushButton_6.clicked.connect(self.addFormSubmitButton)

        #Backbuttons
        self.event_addform_backbutton.clicked.connect(self.Backbuttonaddform)
        self.staff_addform_backbutton.clicked.connect(self.Backbuttonaddform)
        self.inventory_addform_backbutton.clicked.connect(self.Backbuttonaddform)
        self.client_addform_backbutton.clicked.connect(self.Backbuttonaddform)
        self.venue_addform_backbutton.clicked.connect(self.Backbuttonaddform)
        self.user_addform_backbutton.clicked.connect(self.Backbuttonaddform)
    
    def Backbuttonaddform(self):
        if (ch == 'E'):    
            self.comboBox_clientid.clearEditText()
            self.comboBox_clientid.clear()
            self.lineEdit_5.clear()
            self.plainTextEdit_des.clear()
            self.comboBox_venue.clearEditText()
            self.comboBox_venue.clear()

            self.stackedWidget.setCurrentIndex(7)

        elif (ch == 'I'):
            self.lineEdit_17.clear()
            self.comboBox_3.clearEditText()
            self.comboBox_3.clear()

            self.stackedWidget.setCurrentIndex(7)

        elif (ch == 'S'):
            self.lineEdit_8.clear()
            self.lineEdit_7.clear()
            self.lineEdit_6.clear()
            self.lineEdit_37.clear()
            self.lineEdit_11.clear()
            self.comboBox_2.clearEditText()
            self.comboBox_2.clear()

            self.stackedWidget.setCurrentIndex(7)
            
        elif (ch == 'V'):
            self.lineEdit_25.clear()
            self.lineEdit_29.clear()
            
            self.stackedWidget.setCurrentIndex(7)
        elif (ch == 'C'):            
            self.lineEdit_23.clear()
            self.lineEdit_21.clear()
            self.lineEdit_20.clear()
            self.plainTextEdit.clear()
            self.lineEdit_22.clear()
            self.lineEdit_24.clear()
            self.comboBox_21.clearEditText()
            self.comboBox_21.clear()
            self.comboBox_17.clearEditText()
            self.comboBox_17.clear()

            self.stackedWidget.setCurrentIndex(7)

        elif (ch == 'U'):
            self.lineEdit_33.clear()
            self.lineEdit_31.clear()
            self.lineEdit_38.clear()
            self.lineEdit_32.clear()
            self.lineEdit_26.clear()
            self.lineEdit_39.clear()
            self.comboBox_20.clearEditText()
            self.comboBox_20.clear()

            self.stackedWidget.setCurrentIndex(8)
        else:
            QMessageBox.warning(self, "ERROR",
                                "No table is choosed before in afterlogin(tables) screen, which cann't be happen")

    def onClickAddButton(self):  # user_login_table_addbutton
        if (ch == 'E'):
            print("asd")
            ##fetch Venue name client id and event id
            cur.execute(''' SELECT v_name FROM venue''')
            venuename = cur.fetchall()
            cur.execute(''' SELECT c_id FROM client;''')
            cid = cur.fetchall()
            for data in venuename:
                self.comboBox_venue.addItem(data[0])
            for data in cid:
                self.comboBox_clientid.addItem(data[0])
            self.lineEdit_eventid.setText(generateid(ch))
            self.stackedWidget.setCurrentIndex(10)

        elif (ch == 'I'):
            cur.execute(''' SELECT event_id FROM event''')
            eventid = cur.fetchall()
            for data in eventid:
                self.comboBox_3.addItem(data[0])
            self.lineEdit_13.setText(generateid(ch))
            self.stackedWidget.setCurrentIndex(12)

        elif (ch == 'S'):
            cur.execute(''' SELECT distinct s_type FROM staff''')
            stype = cur.fetchall()

            for data in stype:
                self.comboBox_2.addItem(data[0])
            self.lineEdit_10.setText(generateid(ch))
            self.stackedWidget.setCurrentIndex(11)

        elif (ch == 'V'):
            self.lineEdit_27.setText(generateid(ch))
            self.stackedWidget.setCurrentIndex(14)

        elif (ch == 'C'):
            self.lineEdit_19.setText(generateid(ch))
            #cur.execute(''' SELECT distinct client_type  FROM client;''')
            #client_type = cur.fetchall()
            #for data in client_type:
            #    self.comboBox_21.addItem(data[0])
            self.stackedWidget.setCurrentIndex(13)
        elif (ch == 'U'):

            #cur.execute(''' SELECT distinct user_designation FROM Users;''')
            #user_type = cur.fetchall()
            #for data in user_type:
            #    self.comboBox_20.addItem(data[0])
            #k = generateid(ch)
            self.lineEdit_28.setText(generateid(ch))
            #print(k)
            self.stackedWidget.setCurrentIndex(15)
        else:
            QMessageBox.warning(self, "ERROR",
                                "No table is choosed before in afterlogin(tables) screen, which cann't be happen")


    def addFormSubmitButton(self):  # all add form submit buttons
        if (ch == 'E'):
            Event_Name = self.lineEdit_5.text()
            Event_date = self.dateEdit.date().toString("yyyy.MM.dd")
            Event_time = self.timeEdit.time().toString("hh:mm")
            Client_id = self.comboBox_clientid.currentText()
            Event_id = self.lineEdit_eventid.text()
            venue_name = self.comboBox_venue.currentText()
            event_description = self.plainTextEdit_des.toPlainText()
            if(Event_Name==""  or  event_description =="" ):
                QMessageBox.warning(self, "ERROR","Event Name or Description fields cannot be empty")
            else:
                cur.execute("select venue_id from venue where v_name='%s'" % venue_name)
                data = cur.fetchall()
                v_id = data[0][0]
                cur.execute("insert into event(event_id,e_name,c_id,venue_id) values('%s','%s','%s','%s')" % (
                    Event_id, Event_Name, Client_id, v_id))
                cur.execute(
                    "insert into event_schedule(event_id,c_id,venue_id,e_date,e_start_time,e_description) values('%s','%s','%s','%s','%s','%s')" % (
                        Event_id, Client_id, v_id, Event_date, Event_time, event_description))
                cur.execute("UPDATE ids SET latest_id='%s' WHERE category='%s' " % (Event_id, ch))
                conn.commit()
                QMessageBox.information(self, "Event Add Status","Event added successfully")

                self.lineEdit_5.clear()
                self.plainTextEdit_des.clear()
                self.lineEdit_eventid.setText(generateid(ch))

        elif (ch == 'I'):
            itemid = self.lineEdit_13.text()
            eventid = self.comboBox_3.currentText()
            itemname = self.lineEdit_17.text()
            if(itemname =="" ):
                QMessageBox.warning(self, "ERROR","Item Name cannot be empty")
            else:
                cur.execute("insert into inventory(model_no, item_name, event_id) values('%s','%s','%s')" % (
                    itemid, itemname, eventid))
                cur.execute("UPDATE ids SET latest_id='%s' WHERE category='%s' " % (itemid, ch))
                conn.commit()
                QMessageBox.information(self, "Inventory Add Status","Inventory Item added successfully")

                self.lineEdit_17.clear()
                self.lineEdit_13.setText(generateid(ch))
            

        elif (ch == 'S'):
            sid = self.lineEdit_10.text()
            stype = self.comboBox_2.currentText()
            sname = self.lineEdit_8.text()
            scontact = self.lineEdit_7.text()
            ssalary = self.lineEdit_6.text()
            semail = self.lineEdit_37.text()
            saddress = self.lineEdit_11.text()
            if(sname =="" or scontact=="" or ssalary==""or semail=="" or saddress=="" ):
                QMessageBox.warning(self, "ERROR","Staff Name or Contact No or Salary or Email or Address can not be Empty")
            else:
                cur.execute("insert into staff(s_id, s_type) values('%s','%s')" % (
                sid, stype))
                if (stype == "Waiter" or stype == "Caterer"):
                    cur.execute("insert into catering_info(s_id,ca_name) values('%s','%s')" % (
                        sid, sname))
                    cur.execute(
                        "insert into ca_contact_details(contact_no, s_id, ca_address, ca_emailid) values('%s','%s','%s','%s')" % (
                            scontact, sid, saddress, semail))
                    cur.execute("insert into ca_salary_details(s_id,salary) values('%s','%s')" % (
                        sid, ssalary))
                else:
                    cur.execute("insert into production_info(s_id,p_name) values('%s','%s')" % (
                        sid, sname))
                    cur.execute(
                        "insert into p_contact_details(contact_no, s_id, p_address, p_emailid) values('%s','%s','%s','%s')" % (
                            scontact, sid, saddress, semail))
                    cur.execute("insert into p_salary_details(s_id,salary) values('%s','%s')" % (
                        sid, ssalary))
                
                cur.execute("UPDATE ids SET latest_id='%s' WHERE category='%s' " % (sid, ch))
                conn.commit()
                QMessageBox.information(self, "Staff Add Status","Staff Added successfully")

                self.lineEdit_8.clear()
                self.lineEdit_7.clear()
                self.lineEdit_6.clear()
                self.lineEdit_37.clear()
                self.lineEdit_11.clear()
                self.lineEdit_10.setText(generateid(ch))


        elif (ch == 'V'):
            venueid = self.lineEdit_27.text()
            location = self.lineEdit_29.text()
            venuename = self.lineEdit_25.text()
            if(venuename=="" or location=="" ):
                QMessageBox.warning(self, "ERROR","location or venuename Cannot be empty")
            else:
                cur.execute("insert into venue(v_name, location, venue_id) values('%s','%s','%s')" % (
                    venuename, location, venueid))
                cur.execute("UPDATE ids SET latest_id='%s' WHERE category='%s' " % (venueid, ch))
                conn.commit()
                QMessageBox.information(self, "Venue Add status","Staff Added successfully")

                self.lineEdit_25.clear()
                self.lineEdit_29.clear()
                self.lineEdit_27.setText(generateid(ch))

        elif (ch == 'C'):
            Client_id = self.lineEdit_19.text()
            Client_name = self.lineEdit_23.text()
            Client_Contactno = self.lineEdit_21.text()
            Client_Email = self.lineEdit_20.text()
            Client_address = self.plainTextEdit.toPlainText()
            Client_Type = self.comboBox_21.currentText()
            Client_paymentstatus = self.comboBox_17.currentText()
            Client_advancepayment = self.lineEdit_22.text()
            Client_totalpayment = self.lineEdit_24.text()
            if(Client_name =="" or Client_Contactno=="" or Client_advancepayment==""or Client_totalpayment=="" or Client_address=="" ):
                QMessageBox.warning(self, "ERROR","Client Name or Contact No or Salary or Email or Address or payments can not be Empty")
            else:    
                cur.execute(
                    "insert into client(c_id,payment_status, advance_payment, total_payment,client_type) values('%s','%s','%s','%s','%s')" % (
                        Client_id, Client_paymentstatus, Client_advancepayment, Client_totalpayment, Client_Type))
                if (Client_Type == "Conference" or Client_Type == "Other"):
                    cur.execute(
                        "insert into conference_info(c_id,c_name) values('%s','%s')" % (
                            Client_id, Client_name))
                    cur.execute(
                        "insert into c_contact_details(c_id,contact_No, c_address, c_emailid) values('%s','%s','%s','%s')" % (
                            Client_id, Client_Contactno, Client_address, Client_Email))
                elif (Client_Type == "Seminar"):
                    cur.execute(
                        "insert into seminar_info(c_id,c_name) values('%s','%s')" % (
                            Client_id, Client_name))
                    cur.execute(
                        "insert into s_contact_details(c_id,contact_No, c_address, c_emailid) values('%s','%s','%s','%s')" % (
                            Client_id, Client_Contactno, Client_address, Client_Email))

                elif (Client_Type == "Wedding"):
                    cur.execute(
                        "insert into wedding_info(c_id,c_name) values('%s','%s')" % (Client_id, Client_name))
                    cur.execute(
                        "insert into w_contact_details(c_id,contact_No, c_address, c_emailid) values('%s','%s','%s','%s')" % (
                            Client_id, Client_Contactno, Client_address, Client_Email))
                QMessageBox.information(self, "Client Add status","Client Added successfully")
                cur.execute("UPDATE ids SET latest_id='%s' WHERE category='%s' " % (Client_id, ch))
                conn.commit()
                self.lineEdit_23.clear()
                self.lineEdit_21.clear()
                self.lineEdit_20.clear()
                self.plainTextEdit.clear()
                self.lineEdit_22.clear()
                self.lineEdit_24.clear()
                self.lineEdit_19.setText(generateid(ch))

        elif (ch == 'U'):
            User_id = self.lineEdit_28.text()
            User_name = self.lineEdit_33.text()
            User_Contactno = self.lineEdit_31.text()
            User_Email = self.lineEdit_38.text()
            User_address = self.lineEdit_32.text()
            User_Type = self.comboBox_20.currentText()
            User_Salary = self.lineEdit_26.text()
            User_password = self.lineEdit_39.text()
            if(User_name =="" or User_Contactno=="" or User_Email==""or User_address=="" or User_Salary=="" or User_password=="" ):
                QMessageBox.warning(self, "ERROR","User Name or Contact No or Salary or Email or Address or password can not be Empty")
            else:    
                cur.execute(
                    "insert into Users(u_id,user_name, user_designation, user_password,user_contact_no,user_email,user_address,user_salary) values('%s','%s','%s','%s','%s','%s','%s','%s')" % (
                        User_id, User_name, User_Type, User_password, User_Contactno, User_Email, User_address,
                        User_Salary))
                conn.commit()
                QMessageBox.information(self, "User Add status","User Added successfully")

                self.lineEdit_33.clear()
                self.lineEdit_31.clear()
                self.lineEdit_38.clear()
                self.lineEdit_32.clear()
                self.lineEdit_26.clear()
                self.lineEdit_39.clear()
                self.lineEdit_28.setText(generateid(ch))
        else:
            QMessageBox.warning(self, "ERROR",
                                "No table is choosed before in afterlogin(tables) screen, which cann't be happen")

class Delete(User):
    def __init__(self):
        User.__init__(self)
        

    def Handel_Buttons_Delete(self):
        self.user_login_table_deletebutton.clicked.connect(self.onClickDeleteButton)
        self.admin_login_table_removeuserbutton.clicked.connect(self.onClickDeleteButton)

        self.DeleteSubmit.clicked.connect(self.fn_DeleteSubmit)

        self.delete_backbutton.clicked.connect(self.BackButtonfunction_Delete)

    def onClickDeleteButton(self):
        self.stackedWidget.setCurrentIndex(17)
        global _list
        if (ch == 'E'):
            cur.execute('''SELECT event.event_id,e_name,e_description,v_name,e_date,e_start_time,events.venue_id,location,event.c_id
                                FROM  (SELECT event_id,e_description,v_name,e_date,e_start_time,venue.venue_id,location,c_id 
    		                            FROM event_schedule left join venue on event_schedule.venue_id = venue.venue_id) as events right JOIN event 
    		                            on event.event_id=events.event_id''')
            data = cur.fetchall()
            headerdata = ["Event Id", "Event Name", "Description", "Venue Name", "Event Date", "Event Start Time",
                          "Venue Id",
                          "Location", "Client Id"]
            self.DeleteTableView(data, headerdata, self.tableWidget)
            for i in range(0,len(headerdata)):
                self.tableWidget.setColumnWidth(i, 1201/len(headerdata));
            
        elif (ch == 'I'):
            cur.execute('''select *
                               from inventory;''')
            data = cur.fetchall()
            headerdata = ["Item Id", "Item Name", "Event Id"]
            self.DeleteTableView(data, headerdata, self.tableWidget)
            for i in range(0,len(headerdata)):
                self.tableWidget.setColumnWidth(i, 1201/len(headerdata));
        elif (ch == 'S'):
            cur.execute('''select s_id ,ca_name, s_type, contact_no, ca_emailid, salary ,ca_address 
                               from staff natural join ca_contact_details natural join ca_salary_details natural join catering_info
                               UNION
                               select s_id ,p_name, s_type, contact_no, p_emailid, salary ,p_address 
                               from staff natural join p_contact_details natural join p_salary_details natural join production_info;
                            ''')
            data = cur.fetchall()
            headerdata = ["Staff Id ", "Name", "Type", "Contact No.", "Email Id", "Salary", "Address"]
            self.DeleteTableView(data, headerdata, self.tableWidget)
            for i in range(0,len(headerdata)):
                self.tableWidget.setColumnWidth(i, 1201/len(headerdata));
        elif (ch == 'V'):
            cur.execute('''select venue_id, v_name, location
                                from venue''')
            data = cur.fetchall()
            headerdata = ["Venue Id", "Venue Name", "Location"]
            self.DeleteTableView(data, headerdata, self.tableWidget)
            for i in range(0,len(headerdata)):
                self.tableWidget.setColumnWidth(i, 1201/len(headerdata));
        elif (ch == 'C'):
            cur.execute('''select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                               from client natural join c_contact_details natural join conference_info
                               UNION
                               select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                               from client natural join s_contact_details natural join seminar_info
                               UNION
                               select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                               from client natural join w_contact_details natural join wedding_info;''')
            data = cur.fetchall()
            headerdata = ["Client Id", "Client Name", "Client Type", "Payment Status", "Advance Payment",
                          "Total Payment", "Contact No.", "Address", "Email Id"]
            self.DeleteTableView(data, headerdata, self.tableWidget)
            for i in range(0,len(headerdata)):
                self.tableWidget.setColumnWidth(i, 1201/len(headerdata));
        elif (ch == 'U'):
            cur.execute('''select * from Users''')
            data = cur.fetchall()
            headerdata = ["User Id", "Name", "Designation", "Password", "Contact No", "Address"]
            self.DeleteTableView(data, headerdata, self.tableWidget)
            for i in range(0,len(headerdata)):
                self.tableWidget.setColumnWidth(i, 1201/len(headerdata));

    def BackButtonfunction_Delete(self):  # delete_backbutton
        if (ch == 'U'):
            self.stackedWidget.setCurrentIndex(8)
        else:
            self.stackedWidget.setCurrentIndex(7)

    def fn_DeleteSubmit(self):  # delete submit button
        global _list
        if(len(_list)==0):
            QMessageBox.information(self, "Warning","Please Select atleast one row to Delete")
        else:
            if (ch == 'E'):
                for i in _list:
                    cur.execute("DELETE FROM event WHERE (event_id = '%s')" % i)
                    conn.commit()
                self.onClickDeleteButton()
                _list.clear()
            elif (ch == 'I'):
                for i in _list:
                    cur.execute("DELETE FROM inventory WHERE (model_no = '%s')" % i)
                    conn.commit()
                self.onClickDeleteButton()
                _list.clear()

            elif (ch == 'S'):
                for i in _list:
                    cur.execute("DELETE FROM staff WHERE (s_id = '%s')" % i)
                    conn.commit()
                self.onClickDeleteButton()
                _list.clear()

            elif (ch == 'V'):
                for i in _list:
                    cur.execute("DELETE FROM venue WHERE (venue_id = '%s')" % i)
                    conn.commit()
                self.onClickDeleteButton()
                _list.clear()

            elif (ch == 'C'):
                for i in _list:
                    cur.execute("DELETE FROM client WHERE (c_id = '%s')" % i)
                    conn.commit()
                self.onClickDeleteButton()
                _list.clear()

            elif (ch == 'U'):
                for i in _list:
                    cur.execute("DELETE FROM Users WHERE (u_id = '%s')" % i)
                    conn.commit()
                self.onClickDeleteButton()
                _list.clear()

class Update(User):
    def __init__(self):
        User.__init__(self)

    def Handel_Buttons_Update(self):
        self.update_backbutton.clicked.connect(self.onClickUpdateButton_2) # *updateEvent_backbutton
        self.updateStaff_backbutton.clicked.connect(self.onClickUpdateButton_2)
        self.updateInventory_backbutton.clicked.connect(self.onClickUpdateButton_2)
        self.updateClient_backbutton.clicked.connect(self.onClickUpdateButton_2)
        self.updateVenue_backbutton.clicked.connect(self.onClickUpdateButton_2)
        self.changeUserPass_backbutton.clicked.connect(self.onClickUpdateButton_2)  # UpdateUserProfile page backbutton

        self.update_select_row_backbutton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(7))

        self.user_login_table_updatebutton.clicked.connect(self.onClickUpdateButton)
        self.admin_login_table_changeUserPassbutton.clicked.connect(self.onClickUpdateButton)  # update user profile button

        self.update_select_row_submitbutton.clicked.connect(self.onClickUpdate)

        # update form submit buttons
        self.Event_submit_2.clicked.connect(self.UpdateSubmit)
        self.pushButton_16.clicked.connect(self.UpdateSubmit)
        self.pushButton_17.clicked.connect(self.UpdateSubmit)
        self.pushButton_18.clicked.connect(self.UpdateSubmit)
        self.pushButton_30.clicked.connect(self.UpdateSubmit)
        self.changepass_okbutton_4.clicked.connect(self.UpdateSubmit)

    def onClickUpdateButton(self):
        self.stackedWidget.setCurrentIndex(28)
        global _list
        if (ch == 'E'):
            cur.execute('''SELECT event.event_id,e_name,e_description,v_name,e_date,e_start_time,events.venue_id,location,event.c_id
                           FROM  (SELECT event_id,e_description,v_name,e_date,e_start_time,venue.venue_id,location,c_id 
 	                       FROM event_schedule left join venue on event_schedule.venue_id = venue.venue_id) as events right JOIN event 
 	                       on event.event_id=events.event_id''')
            data = cur.fetchall()
            headerdata = ["Event Id", "Event Name", "Description", "Venue Name", "Event Date", "Event Start Time",
                          "Venue Id", "Location", "Client Id"]
            self.DeleteTableView(data, headerdata, self.update_tableWidget)
            for i in range(0,len(headerdata)):
                self.update_tableWidget.setColumnWidth(i, 1201/len(headerdata));

        elif (ch == 'I'):
            cur.execute('''select *
                           from inventory;''')
            data = cur.fetchall()
            headerdata = ["Model No.", "Item Name", "Event Id"]
            self.DeleteTableView(data, headerdata, self.update_tableWidget)
            for i in range(0,len(headerdata)):
                self.update_tableWidget.setColumnWidth(i, 1201/len(headerdata));
        elif (ch == 'S'):
            cur.execute('''select s_id ,ca_name, s_type, contact_no, ca_emailid, salary ,ca_address 
                           from staff natural join ca_contact_details natural join ca_salary_details natural join catering_info
                           UNION
                           select s_id ,p_name, s_type, contact_no, p_emailid, salary ,p_address 
                           from staff natural join p_contact_details natural join p_salary_details natural join production_info;''')
            data = cur.fetchall()
            headerdata = ["Staff Id ", "Name", "Type", "Contact No.", "Email Id", "Salary", "Address"]
            self.DeleteTableView(data, headerdata, self.update_tableWidget)
            for i in range(0,len(headerdata)):
                self.update_tableWidget.setColumnWidth(i, 1201/len(headerdata));
        elif (ch == 'V'):
            cur.execute('''select venue_id, v_name, location
                                    from venue''')
            data = cur.fetchall()
            headerdata = ["Venue Id", "Venue Name", "Location"]
            self.DeleteTableView(data, headerdata, self.update_tableWidget)
            for i in range(0,len(headerdata)):
                self.update_tableWidget.setColumnWidth(i, 1201/len(headerdata));
        elif (ch == 'C'):
            cur.execute(''' select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                            from client natural join c_contact_details natural join conference_info
                            UNION
                            select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                            from client natural join s_contact_details natural join seminar_info
                            UNION
                            select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                            from client natural join w_contact_details natural join wedding_info''')
            data = cur.fetchall()
            headerdata = ["Client Id", "Client Name", "Client Type", "Payment Status", "Advance Payment",
                          "Total Payment", "Contact No.", "Address", "Email Id"]
            self.DeleteTableView(data, headerdata, self.update_tableWidget)
            for i in range(0,len(headerdata)):
                self.update_tableWidget.setColumnWidth(i, 1201/len(headerdata));

        elif (ch == 'U'):
            cur.execute('''select * from Users''')
            data = cur.fetchall()
            headerdata = ["User Id", "Name", "Designation", "Password", "Contact No", "Address"]
            self.DeleteTableView(data, headerdata, self.update_tableWidget)
            for i in range(0,len(headerdata)):
                self.update_tableWidget.setColumnWidth(i, 1201/len(headerdata));
            
    def onClickUpdateButton_2(self):
        self.stackedWidget.setCurrentIndex(28)
        global _list
        if (ch == 'E'):
            cur.execute('''SELECT event.event_id,e_name,e_description,v_name,e_date,e_start_time,events.venue_id,location,event.c_id
                           FROM  (SELECT event_id,e_description,v_name,e_date,e_start_time,venue.venue_id,location,c_id 
 	                       FROM event_schedule left join venue on event_schedule.venue_id = venue.venue_id) as events right JOIN event 
 	                       on event.event_id=events.event_id''')
            data = cur.fetchall()
            headerdata = ["Event Id", "Event Name", "Description", "Venue Name", "Event Date", "Event Start Time",
                          "Venue Id", "Location", "Client Id"]
            self.DeleteTableView_2(data, headerdata, self.update_tableWidget)
            for i in range(0,len(headerdata)):
                self.update_tableWidget.setColumnWidth(i, 1201/len(headerdata));

        elif (ch == 'I'):
            cur.execute('''select *
                           from inventory;''')
            data = cur.fetchall()
            headerdata = ["Model No.", "Item Name", "Event Id"]
            self.DeleteTableView_2(data, headerdata, self.update_tableWidget)
            for i in range(0,len(headerdata)):
                self.update_tableWidget.setColumnWidth(i, 1201/len(headerdata));
        elif (ch == 'S'):
            cur.execute('''select s_id ,ca_name, s_type, contact_no, ca_emailid, salary ,ca_address 
                           from staff natural join ca_contact_details natural join ca_salary_details natural join catering_info
                           UNION
                           select s_id ,p_name, s_type, contact_no, p_emailid, salary ,p_address 
                           from staff natural join p_contact_details natural join p_salary_details natural join production_info;''')
            data = cur.fetchall()
            headerdata = ["Staff Id ", "Name", "Type", "Contact No.", "Email Id", "Salary", "Address"]
            self.DeleteTableView_2(data, headerdata, self.update_tableWidget)
            for i in range(0,len(headerdata)):
                self.update_tableWidget.setColumnWidth(i, 1201/len(headerdata));
        elif (ch == 'V'):
            cur.execute('''select venue_id, v_name, location
                                    from venue''')
            data = cur.fetchall()
            headerdata = ["Venue Id", "Venue Name", "Location"]
            self.DeleteTableView_2(data, headerdata, self.update_tableWidget)
            for i in range(0,len(headerdata)):
                self.update_tableWidget.setColumnWidth(i, 1201/len(headerdata));
        elif (ch == 'C'):
            cur.execute(''' select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                            from client natural join c_contact_details natural join conference_info
                            UNION
                            select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                            from client natural join s_contact_details natural join seminar_info
                            UNION
                            select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                            from client natural join w_contact_details natural join wedding_info''')
            data = cur.fetchall()
            headerdata = ["Client Id", "Client Name", "Client Type", "Payment Status", "Advance Payment",
                          "Total Payment", "Contact No.", "Address", "Email Id"]
            self.DeleteTableView_2(data, headerdata, self.update_tableWidget)
            for i in range(0,len(headerdata)):
                self.update_tableWidget.setColumnWidth(i, 1201/len(headerdata));

        elif (ch == 'U'):
            cur.execute('''select * from Users''')
            data = cur.fetchall()
            headerdata = ["User Id", "Name", "Designation", "Password", "Contact No", "Address"]
            self.DeleteTableView_2(data, headerdata, self.update_tableWidget)
            for i in range(0,len(headerdata)):
                self.update_tableWidget.setColumnWidth(i, 1201/len(headerdata));

    def onClickUpdate(self):  # update_select_row_submitbutton/admin_login_table_changeUserPassbutton
        global _list
        if(len(_list)==0):
            QMessageBox.information(self, "Warning","Please Select a row to update")
        else:    
            if (ch == 'E'):
                #print(_list)
                # v=list(_list)(0)
                global v
                
                #self.update_tableWidget.item(list(v)[0], 0).setCheckState(QtCore.Qt.Unchecked)
                
                v.clear()
                w = _list.pop()
                
                cur.execute('''SELECT event.event_id, e_name, e_description, v_name, e_date, e_start_time, events.venue_id, location,event.c_id
                                    FROM  (SELECT event_id,e_description,v_name,e_date,e_start_time,venue.venue_id,location,c_id 
                                            FROM event_schedule left join venue on event_schedule.venue_id = venue.venue_id) as events right JOIN event 
                                            on event.event_id=events.event_id
                                            where events.event_id= "%s"''' % (w))

                data = cur.fetchall()
                self.lineEdit_9.setText(data[0][1])

                do = datetime.strptime(data[0][4], '%Y.%m.%d').date()
                self.dateEdit_2.setDate(do)
                to = datetime.strptime(data[0][5], '%H:%M').time()
                self.timeEdit_2.setTime(to)

                self.comboBox_clientid_2.addItem(data[0][8])

                self.lineEdit_eventid_2.setText(data[0][0])

                self.comboBox_venue_2.addItem(data[0][3])
                self.plainTextEdit_des_2.insertPlainText(data[0][2])
                self.stackedWidget.setCurrentIndex(18)
                _list.clear()
                v.clear()

                cur.execute(''' SELECT v_name FROM venue''')
                venuename = cur.fetchall()
                cur.execute(''' SELECT c_id FROM client;''')
                cid = cur.fetchall()
                for data_ in venuename:
                    if (data_[0] != data[0][3]):
                        self.comboBox_venue_2.addItem(data_[0])
                for data_ in cid:
                    if (data_[0] != data[0][8]):
                        self.comboBox_clientid_2.addItem(data_[0])

            elif (ch == 'I'):
                v = _list.pop()
                cur.execute(""" 
                            select *
                            from inventory
                            where model_no = "%s"
                            """ % (v))

                data = cur.fetchall()
                self.lineEdit_78.setText(data[0][0])
                self.lineEdit_79.setText(data[0][1])
                self.comboBox_9.addItem(data[0][2])
                cur.execute(''' SELECT event_id FROM event''')
                eventids = cur.fetchall()
                for data_ in eventids:
                    if (data_[0] != data[0][2]):
                        self.comboBox_9.addItem(data_[0])
                

                self.stackedWidget.setCurrentIndex(20)
                _list.clear()
            
            elif (ch == 'S'):
                v = _list.pop()
                cur.execute(''' 
                                Select s_id ,ca_name, s_type, contact_no, ca_emailid, salary ,ca_address
                                From (
                                select s_id ,ca_name, s_type, contact_no, ca_emailid, salary ,ca_address 
                                from staff natural join ca_contact_details natural join ca_salary_details natural join catering_info
                                UNION
                                select s_id ,p_name, s_type, contact_no, p_emailid, salary ,p_address 
                                from staff natural join p_contact_details natural join p_salary_details natural join production_info) as Staff
                                where Staff.s_id = "%s"
                            ''' % (v))
                data = cur.fetchall()
                self.lineEdit_72.setText(data[0][0])
                self.lineEdit_71.setText(data[0][1])
                self.lineEdit_73.setText(data[0][3])
                self.comboBox_8.addItem(data[0][2])
                self.lineEdit_74.setText(data[0][4])
                self.lineEdit_76.setText(data[0][5])
                self.lineEdit_75.setText(data[0][6])

                
                for type in ("Caterer","Planner","Waiter","Manager"):
                    if(type!=data[0][2]):
                        self.comboBox_8.addItem(type)
                self.stackedWidget.setCurrentIndex(19)
                _list.clear()
                
            elif (ch == 'V'):
                v = _list.pop()
                cur.execute('''select venue_id, v_name, location
                            from venue
                            where venue.venue_id= "%s"''' % (v))

                data = cur.fetchall()
                self.lineEdit_81.setText(data[0][0])
                self.lineEdit_82.setText(data[0][1])
                self.lineEdit_80.setText(data[0][2])

                self.stackedWidget.setCurrentIndex(21)
                
                _list.clear()
                

            elif (ch == 'C'):
                v = _list.pop()
                cur.execute(''' select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                                from(
                                select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                                from client natural join c_contact_details natural join conference_info
                                UNION
                                select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                                from client natural join s_contact_details natural join seminar_info
                                UNION
                                select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                                from client natural join w_contact_details natural join wedding_info ) as C
                                where C.c_id= "%s"''' % (v))

                data = cur.fetchall()
                self.lineEdit_138.setText(data[0][0])
                self.lineEdit_132.setText(data[0][1])
            
                self.comboBox_22.addItem(data[0][2])
                self.comboBox_16.addItem(data[0][3])
                
                self.lineEdit_133.setText(data[0][4])
                self.lineEdit_136.setText(data[0][5])
                self.lineEdit_134.setText(data[0][6])

                self.plainTextEdit_2.insertPlainText(data[0][7])

                self.lineEdit_135.setText(data[0][8])
                
                self.stackedWidget.setCurrentIndex(22)
                _list.clear()

                if (data[0][2]!= "Conference"):
                    self.comboBox_22.addItem("Conference")
                if(data[0][2]!= "Seminar"):
                    self.comboBox_22.addItem("Seminar")
                if(data[0][2]!= "Other"):
                    self.comboBox_22.addItem("Other")
                if (data[0][2] != "Wedding"):
                    self.comboBox_22.addItem("Wedding")

                if (data[0][3]!= "PAID"):
                    self.comboBox_16.addItem("PAID")
                else: 
                    self.comboBox_16.addItem("UNPAID")
                
                            
            elif (ch == 'U'):
                v = _list.pop()
                #["User Id", "Name", "Designation", "Password", "Contact No", "Address", "Email", "Salary"]
                cur.execute("""
                                select * 
                                from EMS_DB.Users
                                where u_id="%s"
                                """ % (v) )
                data = cur.fetchall()
                self.lineEdit_64.setText(data[0][1])
                self.lineEdit_63.setText(data[0][4])
                self.lineEdit_61.setText(data[0][7])
                self.lineEdit_65.setText(data[0][5])
                self.lineEdit_62.setText(data[0][6])
                self.comboBox_18.addItem(data[0][2])
                self.lineEdit_66.setText(data[0][0])
                self.lineEdit_140.setText(data[0][3])

                
                for type in ("Admin","Event Manager","Staff Manager","Inventory Manager","Receptionist"):
                    if(type!=data[0][2]):
                        self.comboBox_18.addItem(type)
                _list.clear()
                self.stackedWidget.setCurrentIndex(23)
            else:
                QMessageBox.warning(self, "ERROR",
                                    "No table is choosed before in afterlogin(tables) screen, which cann't be happen")

    def UpdateSubmit(self):
        if (ch == 'E'):
            Event_Name = self.lineEdit_9.text()
            Event_date = self.dateEdit_2.date().toString("yyyy.MM.dd")
            Event_time = self.timeEdit_2.time().toString("hh:mm")
            Client_id = self.comboBox_clientid_2.currentText()
            Event_id = self.lineEdit_eventid_2.text()
            venue_name = self.comboBox_venue_2.currentText()
            event_description = self.plainTextEdit_des_2.toPlainText()

            if(Event_Name==""  or  event_description =="" ):
                QMessageBox.warning(self, "ERROR","Event Name or Description fields cannot be empty")
            else: 
                cur.execute("select venue_id from venue where v_name='%s'" % venue_name)
                data = cur.fetchall()
                v_id = data[0][0]

                cur.execute("UPDATE event SET e_name='%s',c_id='%s',venue_id='%s' WHERE event_id='%s'" % (
                    Event_Name, Client_id, v_id, Event_id))

                cur.execute(
                    "UPDATE event_schedule SET c_id='%s',venue_id='%s',e_date='%s',e_start_time='%s',e_description='%s' where event_id='%s'" % (
                        Client_id, v_id, Event_date, Event_time, event_description, Event_id))
                conn.commit()
                QMessageBox.information(self, "Update Status", "Event Table's row is updated successfully")

        elif (ch == 'I'):
            itemid = self.lineEdit_78.text()
            eventid = self.comboBox_9.currentText()
            itemname = self.lineEdit_79.text()
            if(itemname =="" ):
                QMessageBox.warning(self, "ERROR","Item Name cannot be empty")
            else:
                cur.execute("UPDATE inventory SET event_id='%s',item_name='%s' WHERE model_no='%s' " % (
                    eventid, itemname, itemid))
            
                conn.commit()
                QMessageBox.information(self, "Update Status", "Inventory Table's row is updated successfully")


        elif (ch == 'S'):
            sid = self.lineEdit_72.text()
            stype = self.comboBox_8.currentText()
            sname = self.lineEdit_71.text()
            scontact = self.lineEdit_73.text()
            ssalary = self.lineEdit_76.text()
            semail = self.lineEdit_74.text()
            saddress = self.lineEdit_75.text()

            if(sname =="" or scontact=="" or ssalary==""or semail=="" or saddress=="" ):
                QMessageBox.warning(self, "ERROR","Staff Name or Contact No or Salary or Email or Address can not be Empty")
            else:
                cur.execute("UPDATE staff SET s_type='%s' WHERE s_id='%s'" % (
                    stype, sid))
                if (stype == "Waiter" or stype == "Caterer"):
                    cur.execute(''' Update catering_info SET ca_name="%s" Where s_id="%s" '''% (
                        sname,  sid))
                        
                    cur.execute(
                        ''' Update ca_contact_details SET contact_no="%s" ca_address="%s"  ca_emailid="%s" where s_id="%s" ''' % (
                            scontact, saddress ,semail,sid))
                            
                    cur.execute('''Update ca_salary_details Set salary="%s" where s_id="%s"''' % (
                        ssalary,sid))

                else:
                    cur.execute(''' Update production_info SET p_name="%s" Where s_id="%s" ''' % (
                        sname,  sid))
                
                    cur.execute(
                        ''' Update p_contact_details SET contact_no="%s" p_address="%s"  p_emailid="%s" where s_id="%s" ''' % (
                            scontact, semail, saddress, sid))

                    cur.execute('''Update p_salary_details Set salary="%s" where s_id="%s"''' % (
                        ssalary,sid))
            
                conn.commit()
                QMessageBox.information(self, "Update Status", "Staff Table's row is updated successfully")


        elif (ch == 'V'):
            venueid = self.lineEdit_81.text()
            location = self.lineEdit_29.text()
            venuename = self.lineEdit_25.text()
            
            if(venuename=="" or location=="" ):
                QMessageBox.warning(self, "ERROR","location or venuename Cannot be empty")
            else:
                cur.execute("UPDATE venue SET location='%s',v_name='%s' WHERE venue_id='%s' " % (
                location, venuename, venueid ))
                conn.commit()
                QMessageBox.information(self, "Update Status", "Venue Table's row is updated successfully")


        elif (ch == 'C'):
            Client_id = self.lineEdit_138.text()
            Client_name = self.lineEdit_132.text()
            Client_Contactno = self.lineEdit_134.text()
            Client_Email = self.lineEdit_135.text()
            Client_address = self.plainTextEdit_2.toPlainText()
            Client_Type = self.comboBox_22.currentText()
            Client_paymentstatus = self.comboBox_16.currentText()
            Client_advancepayment = self.lineEdit_133.text()
            Client_totalpayment = self.lineEdit_136.text()
            
            if(Client_name =="" or Client_Contactno=="" or Client_advancepayment==""or Client_totalpayment=="" or Client_address=="" ):
                QMessageBox.warning(self, "ERROR","Client Name or Contact No or Salary or Email or Address or payments can not be Empty")
            else:
                cur.execute("UPDATE client SET payment_status='%s', advance_payment='%s', total_payment='%s',client_type='%s' WHERE c_id='%s'" % (
                    Client_paymentstatus, Client_advancepayment, Client_totalpayment, Client_Type,Client_id ))
                
                if (Client_Type == "Conference" or Client_Type == "Other"):


                    cur.execute(''' Update conference_info SET c_name="%s" Where c_id="%s" '''% (
                        Client_name,  Client_id))
                    cur.execute(
                        ''' Update c_contact_details SET contact_No="%s" c_address="%s"  c_emailid="%s" where c_id="%s" ''' % (
                            Client_Contactno,Client_Email , Client_address, Client_id))
                elif (Client_Type == "Seminar"):

                    cur.execute(''' Update seminar_info SET c_name="%s" Where c_id="%s" '''% (
                        Client_name,  Client_id))
                    cur.execute(
                        ''' Update s_contact_details SET contact_No="%s" c_address="%s"  c_emailid="%s" where c_id="%s" ''' % (
                            Client_Contactno,Client_Email , Client_address, Client_id))

                elif (Client_Type == "Wedding"):
        
                    cur.execute(''' Update wedding_info SET c_name="%s" Where c_id="%s" '''% (
                        Client_name,  Client_id))
                    cur.execute(
                        ''' Update w_contact_details SET contact_No="%s" c_address="%s"  c_emailid="%s" where c_id="%s" ''' % (
                            Client_Contactno,Client_Email , Client_address, Client_id))
                
                conn.commit()
                QMessageBox.information(self, "Update Status", "Client Table's row is updated successfully")


        elif (ch == 'U'):
            User_id = self.lineEdit_66.text()
            User_name = self.lineEdit_64.text()
            User_Contactno = self.lineEdit_63.text()
            User_Email = self.lineEdit_62.text()
            User_address = self.lineEdit_65.text()
            User_Type = self.comboBox_18.currentText()
            User_Salary = self.lineEdit_61.text()
            User_password = self.lineEdit_139.text()
            
            if(User_name =="" or User_Contactno=="" or User_Email==""or User_address=="" or User_Salary=="" or User_password==""):
                QMessageBox.warning(self, "ERROR","User Name or Contact No or Salary or Email or Address or password can not be Empty")            
            elif (self.lineEdit_139.text() != self.lineEdit_137.text()):
                QMessageBox.warning(self, "ERROR", "Re-entered new password doesn't match")
            else:
                cur.execute(
                    '''Update Users SET  user_name="%s" user_designation="%s" user_password="%s" user_contact_no="%s" user_email="%s" user_address="%s" user_salary="%s" where u_id="%s" ''' % (
                        User_name, User_Type, User_password, User_Contactno, User_Email, User_address, User_Salary, User_id))
                conn.commit()
                QMessageBox.information(self, "Update Status", "User profile is updated successfully")

        else:
            QMessageBox.warning(self, "ERROR",
                                "No table is choosed before in afterlogin(tables) screen, which cann't be happen")


class View(User):
    def __init__(self):
        User.__init__(self)

    def Handel_Buttons_View(self):
        self.admin_login_table_viewbutton.clicked.connect(self.onClickViewButton)
        self.user_login_table_viewbutton.clicked.connect(self.onClickViewButton)
        self.user_login_table_viewbutton_2.clicked.connect(self.onClickViewButton)
        self.view_backbutton.clicked.connect(self.BackButtonFunction_View)

    def onClickViewButton(self):  # user_login_table_viewbutton
        self.stackedWidget.setCurrentIndex(24)
        print(ch)
        if (ch == 'E'):
            cur.execute('''SELECT event.event_id,e_name,e_description,v_name,e_date,e_start_time,events.venue_id,location,event.c_id
                             FROM  (SELECT event_id,e_description,v_name,e_date,e_start_time,venue.venue_id,location,c_id 
  	                            FROM event_schedule left join venue on event_schedule.venue_id = venue.venue_id) as events right JOIN event 
  	                            on event.event_id=events.event_id''')
            data = cur.fetchall()
            headerdata = ["Event Id", "Event Name", "Description", "Venue Name", "Event Date", "Event Start Time",
                          "Venue Id",
                          "Location", "Client Id"]
            tablemodel = MyTableModel(data, headerdata, self)
            tableview = self.ViewTable
            for i in range(0,len(headerdata)):
                self.ViewTable.setColumnWidth(i, 1481/len(headerdata));
            tableview.setModel(tablemodel)
            layout = QVBoxLayout(self)
            layout.addWidget(tableview)
            self.setLayout(layout)

        elif (ch == 'I'):
            cur.execute('''select *
                            from inventory;''')
            data = cur.fetchall()
            headerdata = ["Item Id", "Item Name", "Event Id"]
            tablemodel = MyTableModel(data, headerdata, self)
            tableview = self.ViewTable
            tableview.setModel(tablemodel)
            for i in range(0,len(headerdata)):
                self.ViewTable.setColumnWidth(i, 1481/len(headerdata));
            layout = QVBoxLayout(self)
            layout.addWidget(tableview)
            self.setLayout(layout)

        elif (ch == 'S'):
            cur.execute('''select s_id ,ca_name, s_type, contact_no, ca_emailid, salary ,ca_address 
                            from staff natural join ca_contact_details natural join ca_salary_details natural join catering_info
                            UNION
                            select s_id ,p_name, s_type, contact_no, p_emailid, salary ,p_address 
                            from staff natural join p_contact_details natural join p_salary_details natural join production_info;''')
            data = cur.fetchall()
            headerdata = ["Staff Id ", "Name", "Type", "Contact No.", "Email Id", "Salary", "Address"]
            tablemodel = MyTableModel(data, headerdata, self)
            tableview = self.ViewTable
            tableview.setModel(tablemodel)
            for i in range(0,len(headerdata)):
                self.ViewTable.setColumnWidth(i, 1481/len(headerdata));
            layout = QVBoxLayout(self)
            layout.addWidget(tableview)
            self.setLayout(layout)

        elif (ch == 'V'):
            cur.execute('''select venue_id, v_name, location
                             from venue''')
            data = cur.fetchall()
            headerdata = ["Venue Id", "Venue Name", "Location"]
            tablemodel = MyTableModel(data, headerdata, self)
            tableview = self.ViewTable
            tableview.setModel(tablemodel)
            for i in range(0,len(headerdata)):
                self.ViewTable.setColumnWidth(i, 1481/len(headerdata));
            layout = QVBoxLayout(self)
            layout.addWidget(tableview)
            self.setLayout(layout)

        elif (ch == 'C'):
            cur.execute('''select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                            from client natural join c_contact_details natural join conference_info
                            UNION
                            select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                            from client natural join s_contact_details natural join seminar_info
                            UNION
                            select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                            from client natural join w_contact_details natural join wedding_info;''')
            data = cur.fetchall()
            headerdata = ["Client Id", "Client Name", "Client Type", "Payment Status", "Advance Payment",
                          "Total Payment", "Contact No.", "Address", "Email Id"]
            tablemodel = MyTableModel(data, headerdata, self)
            tableview = self.ViewTable
            tableview.setModel(tablemodel)
            for i in range(0,len(headerdata)):
                self.ViewTable.setColumnWidth(i, 1481/len(headerdata));
            layout = QVBoxLayout(self)
            layout.addWidget(tableview)
            self.setLayout(layout)

        elif (ch == 'U'):
            cur.execute('''select * from Users''')
            data = cur.fetchall()
            headerdata = ["User Id", "Name", "Designation", "Password", "Contact No", "Address", "Email", "Salary"]
            tablemodel = MyTableModel(data, headerdata, self)
            tableview = self.ViewTable
            tableview.setModel(tablemodel)
            for i in range(0,len(headerdata)):
                self.ViewTable.setColumnWidth(i, 1481/len(headerdata));
            layout = QVBoxLayout(self)
            layout.addWidget(tableview)
            self.setLayout(layout)

        else:
            QMessageBox.warning(self, "ERROR", "Error")

    def BackButtonFunction_View(self):  # view_backbutton
        if(ch1=='E'):
            self.stackedWidget.setCurrentIndex(25)
        else:
            if (ch == 'U'):
                self.stackedWidget.setCurrentIndex(8)
            else:
                self.stackedWidget.setCurrentIndex(7)


class Print(User):
    def __init__(self):
        User.__init__(self)

    def Handel_Buttons_Print(self):
        self.user_login_table_printbutton.clicked.connect(self.onClickPrint)
        #self.EM_login_table_printbutton.clicked.connect(self.onClickPrint)
        self.print_backbutton.clicked.connect(self.BackButtonFunction_print)
        self.PrintPreview.clicked.connect(self.handlePreview)
        self.Print.clicked.connect(self.handlePrint)
        self.user_login_table_printbutton_2.clicked.connect(self.onClickPrint)

    def handlePrint(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.handlePaintRequest(dialog.printer())

    def handlePreview(self):
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    def handlePaintRequest(self, printer):

        if (ch == 'E'):
            cur.execute('''SELECT event.event_id,e_name,e_description,v_name,e_date,e_start_time,events.venue_id,location,event.c_id
                                 FROM  (SELECT event_id,e_description,v_name,e_date,e_start_time,venue.venue_id,location,c_id 
      	                            FROM event_schedule left join venue on event_schedule.venue_id = venue.venue_id) as events right JOIN event 
      	                            on event.event_id=events.event_id''')
            data = cur.fetchall()
            headerdata = ["Event Id", "Event Name", "Description", "Venue Name", "Event Date", "Event Start Time",
                          "Venue Id",
                          "Location", "Client Id"]
            # tablemodel = MyTableModel(data, headerdata, self)
            # tableview = self.ViewTablePrint

            document = QTextDocument()
            cursor = QTextCursor(document)
            table = cursor.insertTable((len(data) + 1), len(data[0]))

            for column in range(table.columns()):
                cursor.insertText(headerdata[column])
                cursor.movePosition(QTextCursor.NextCell)

            for row in range(1, table.rows()):
                for column in range(table.columns()):
                    cursor.insertText(data[row - 1][column])
                    cursor.movePosition(QTextCursor.NextCell)

            document.print_(printer)

        elif (ch == 'I'):
            cur.execute('''select *
                            from inventory;''')
            data = cur.fetchall()
            headerdata = ["Item Id", "Item Name", "Event Id"]
            document = QTextDocument()
            cursor = QTextCursor(document)
            table = cursor.insertTable((len(data) + 1), len(data[0]))

            for column in range(table.columns()):
                cursor.insertText(headerdata[column])
                cursor.movePosition(QTextCursor.NextCell)

            for row in range(1, table.rows()):
                for column in range(table.columns()):
                    cursor.insertText(data[row - 1][column])
                    cursor.movePosition(QTextCursor.NextCell)
            document.print_(printer)


        elif (ch == 'S'):
            cur.execute('''select s_id ,ca_name, s_type, contact_no, ca_emailid, salary ,ca_address 
                            from staff natural join ca_contact_details natural join ca_salary_details natural join catering_info
                            UNION
                            select s_id ,p_name, s_type, contact_no, p_emailid, salary ,p_address 
                            from staff natural join p_contact_details natural join p_salary_details natural join production_info;''')
            data = cur.fetchall()
            headerdata = ["Staff Id ", "Name", "Type", "Contact No.", "Email Id", "Salary", "Address"]
            document = QTextDocument()
            cursor = QTextCursor(document)
            table = cursor.insertTable((len(data) + 1), len(data[0]))

            for column in range(table.columns()):
                cursor.insertText(headerdata[column])
                cursor.movePosition(QTextCursor.NextCell)

            for row in range(1, table.rows()):
                for column in range(table.columns()):
                    cursor.insertText(data[row - 1][column])
                    cursor.movePosition(QTextCursor.NextCell)
            document.print_(printer)

        elif (ch == 'V'):
            cur.execute('''select venue_id, v_name, location
                             from venue''')
            data = cur.fetchall()
            headerdata = ["Venue Id", "Venue Name", "Location"]
            document = QTextDocument()
            cursor = QTextCursor(document)
            table = cursor.insertTable((len(data) + 1), len(data[0]))

            for column in range(table.columns()):
                cursor.insertText(headerdata[column])
                cursor.movePosition(QTextCursor.NextCell)

            for row in range(1, table.rows()):
                for column in range(table.columns()):
                    cursor.insertText(data[row - 1][column])
                    cursor.movePosition(QTextCursor.NextCell)
            document.print_(printer)

        elif (ch == 'C'):
            cur.execute('''select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                            from client natural join c_contact_details natural join conference_info
                            UNION
                            select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                            from client natural join s_contact_details natural join seminar_info
                            UNION
                            select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                            from client natural join w_contact_details natural join wedding_info;''')
            data = cur.fetchall()
            headerdata = ["Client Id", "Client Name", "Client Type", "Payment Status", "Advance Payment",
                          "Total Payment", "Contact No.", "Address", "Email Id"]
            document = QTextDocument()
            cursor = QTextCursor(document)
            table = cursor.insertTable((len(data) + 1), len(data[0]))

            for column in range(table.columns()):
                cursor.insertText(headerdata[column])
                cursor.movePosition(QTextCursor.NextCell)

            for row in range(1, table.rows()):
                for column in range(table.columns()):
                    cursor.insertText(data[row - 1][column])
                    cursor.movePosition(QTextCursor.NextCell)
            document.print_(printer)

        elif (ch == 'U'):
            cur.execute('''select * from Users''')
            data = cur.fetchall()
            headerdata = ["User Id", "Name", "Designation", "Password", "Contact No", "Address", "Email", "Salary"]
            document = QTextDocument()
            cursor = QTextCursor(document)
            table = cursor.insertTable((len(data) + 1), len(data[0]))

            for column in range(table.columns()):
                cursor.insertText(headerdata[column])
                cursor.movePosition(QTextCursor.NextCell)

            for row in range(1, table.rows()):
                for column in range(table.columns()):
                    cursor.insertText(data[row - 1][column])
                    cursor.movePosition(QTextCursor.NextCell)
            document.print_(printer)

        else:
            QMessageBox.warning(self, "ERROR", "Error")

    def onClickPrint(self):
        self.stackedWidget.setCurrentIndex(16)
        print(ch)
        if (ch == 'E'):
            cur.execute('''SELECT event.event_id,e_name,e_description,v_name,e_date,e_start_time,events.venue_id,location,event.c_id
                             FROM  (SELECT event_id,e_description,v_name,e_date,e_start_time,venue.venue_id,location,c_id 
  	                            FROM event_schedule left join venue on event_schedule.venue_id = venue.venue_id) as events right JOIN event 
  	                            on event.event_id=events.event_id''')
            data = cur.fetchall()
            headerdata = ["Event Id", "Event Name", "Description", "Venue Name", "Event Date", "Event Start Time",
                          "Venue Id",
                          "Location", "Client Id"]
            tablemodel = MyTableModel(data, headerdata, self)
            tableview = self.ViewTablePrint
            tableview.setModel(tablemodel)
            layout = QVBoxLayout(self)
            layout.addWidget(tableview)
            for i in range(0,len(headerdata)):
                self.ViewTablePrint.setColumnWidth(i, 1481/len(headerdata));
            self.setLayout(layout)

        elif (ch == 'I'):
            cur.execute('''select *
                            from inventory;''')
            data = cur.fetchall()
            headerdata = ["Item Id", "Item Name", "Event Id"]
            tablemodel = MyTableModel(data, headerdata, self)
            tableview = self.ViewTablePrint
            tableview.setModel(tablemodel)
            for i in range(0,len(headerdata)):
                self.ViewTablePrint.setColumnWidth(i, 1481/len(headerdata));
            
            layout = QVBoxLayout(self)
            layout.addWidget(tableview)
            self.setLayout(layout)

        elif (ch == 'S'):
            cur.execute('''select s_id ,ca_name, s_type, contact_no, ca_emailid, salary ,ca_address 
                            from staff natural join ca_contact_details natural join ca_salary_details natural join catering_info
                            UNION
                            select s_id ,p_name, s_type, contact_no, p_emailid, salary ,p_address 
                            from staff natural join p_contact_details natural join p_salary_details natural join production_info;''')
            data = cur.fetchall()
            headerdata = ["Staff Id ", "Name", "Type", "Contact No.", "Email Id", "Salary", "Address"]
            tablemodel = MyTableModel(data, headerdata, self)
            tableview = self.ViewTablePrint
            tableview.setModel(tablemodel)
            for i in range(0,len(headerdata)):
                self.ViewTablePrint.setColumnWidth(i, 1481/len(headerdata));
            layout = QVBoxLayout(self)
            layout.addWidget(tableview)
            self.setLayout(layout)

        elif (ch == 'V'):
            cur.execute('''select venue_id, v_name, location
                             from venue''')
            data = cur.fetchall()
            headerdata = ["Venue Id", "Venue Name", "Location"]
            tablemodel = MyTableModel(data, headerdata, self)
            tableview = self.ViewTablePrint
            tableview.setModel(tablemodel)
            for i in range(0,len(headerdata)):
                self.ViewTablePrint.setColumnWidth(i, 1481/len(headerdata));
            layout = QVBoxLayout(self)
            layout.addWidget(tableview)
            self.setLayout(layout)

        elif (ch == 'C'):
            cur.execute('''select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                            from client natural join c_contact_details natural join conference_info
                            UNION
                            select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                            from client natural join s_contact_details natural join seminar_info
                            UNION
                            select c_id ,c_name, client_type, payment_status, advance_payment, total_payment, contact_No, c_address, c_emailid
                            from client natural join w_contact_details natural join wedding_info;''')
            data = cur.fetchall()
            headerdata = ["Client Id", "Client Name", "Client Type", "Payment Status", "Advance Payment",
                          "Total Payment", "Contact No.", "Address", "Email Id"]
            tablemodel = MyTableModel(data, headerdata, self)
            tableview = self.ViewTablePrint
            tableview.setModel(tablemodel)
            for i in range(0,len(headerdata)):
                self.ViewTablePrint.setColumnWidth(i, 1481/len(headerdata));

            layout = QVBoxLayout(self)
            layout.addWidget(tableview)
            self.setLayout(layout)

        elif (ch == 'U'):
            cur.execute('''select * from Users''')
            data = cur.fetchall()
            headerdata = ["User Id", "Name", "Designation", "Password", "Contact No", "Address", "Email", "Salary"]
            tablemodel = MyTableModel(data, headerdata, self)
            tableview = self.ViewTablePrint
            tableview.setModel(tablemodel)
            for i in range(0,len(headerdata)):
                self.ViewTablePrint.setColumnWidth(i, 1481/len(headerdata));
            layout = QVBoxLayout(self)
            layout.addWidget(tableview)
            self.setLayout(layout)

        else:
            QMessageBox.warning(self, "ERROR", "Error")

    def BackButtonFunction_print(self):  # print_backbutton
        if(ch1=='E'):
            self.stackedWidget.setCurrentIndex(25)
        else:
            if (ch == 'U'):
                self.stackedWidget.setCurrentIndex(8)
            else:
                self.stackedWidget.setCurrentIndex(7)

class Change_Password(User):
    def __init__(self):
        User.__init__(self)

    def Handel_Buttons_Change_Password(self):
        self.changepass_button.clicked.connect(self.onClickChangePassword)
        self.changepass_okbutton.clicked.connect(self.onClickChangePasswordOK)
        self.changepass_backbutton.clicked.connect(self.BackButtonfunction_changepassword)

    def onClickChangePasswordOK(self):# changepass_okbutton
        oldp=self.lineEdit_36.text()
        newp=self.lineEdit_35.text()
        re_newp=self.lineEdit_34.text()
        cur.execute('''SELECT * FROM EMS_DB.Users''')
        data = cur.fetchall()
        for row in data:
            if(Userid == row[0]):
                passw=row[3]
        if (oldp != passw):
            QMessageBox.warning(self, "ERROR", "Old password doesn't match")
        elif(re_newp != newp):
            QMessageBox.warning(self, "ERROR", "Re-entered new password doesn't match")
        elif(newp == ''):
            QMessageBox.warning(self, "ERROR", "New password field can't be empty")
        else:
            cur.execute("UPDATE EMS_DB.Users SET user_password='%s' WHERE u_id='%s' " % (
                newp, Userid))
            conn.commit()
            QMessageBox.information(self, "Password Status", "User password is changed successfully")
            self.stackedWidget.setCurrentIndex(0)
            self.signout_button.setVisible(False)
            self.changepass_button.setVisible(False)
            self.myprofile_button.setVisible(False)
            self.comboBox_input_username.clearEditText()
            self.lineEdit_input_password.clear()
            self.comboBox_input_username.clear()
        self.lineEdit_36.clear()
        self.lineEdit_35.clear()
        self.lineEdit_34.clear()
        
    def onClickChangePassword(self):
        self.myprofile_button.setVisible(False)
        global p_index
        p_index = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(9)

    def BackButtonfunction_changepassword(self):
        self.myprofile_button.setVisible(True)
        self.stackedWidget.setCurrentIndex(p_index)

class Sign_Out(User):
    def __init__(self):
        User.__init__(self)

    def Handel_Buttons_Sign_Out(self):
        self.signout_button.clicked.connect(self.onClickSignOut)

    def onClickSignOut(self):  # signout_button
        self.stackedWidget.setCurrentIndex(0)
        self.signout_button.setVisible(False)
        self.changepass_button.setVisible(False)
        self.myprofile_button.setVisible(False)
        self.comboBox_input_username.clearEditText()
        self.lineEdit_input_password.clear()
        self.comboBox_input_username.clear()

class myprofile(User):
    def __init__(self):
        User.__init__(self)

    def Handel_Buttons_Myprofile(self):
        self.myprofile_button.clicked.connect(self.onClickMyprofile)
        self.myprofile_backbutton.clicked.connect(self.BackButtonfunction_myprofile)

    def onClickMyprofile(self):  # myprofile_button
        self.changepass_button.setVisible(False)
        global p_index
        p_index = self.stackedWidget.currentIndex()

        # ["User Id", "Name", "Designation", "Password", "Contact No", "Address", "Email", "Salary"]
        cur.execute("""select * 
                       from EMS_DB.Users
                       where u_id="%s"
                        """ % (Userid))
        data = cur.fetchall()
        self.lineEdit_67.setText(data[0][0])
        self.lineEdit_68.setText(data[0][1])
        self.lineEdit_84.setText(data[0][2])
        self.lineEdit_69.setText(data[0][4])
        self.lineEdit_77.setText(data[0][5])
        self.lineEdit_83.setText(data[0][6])
        self.lineEdit_70.setText(data[0][7])

        self.stackedWidget.setCurrentIndex(27)

    def BackButtonfunction_myprofile(self):
        self.changepass_button.setVisible(True)
        self.stackedWidget.setCurrentIndex(p_index)

class Main_Window(Add, Delete, Update, View, Print, Change_Password, Sign_Out, myprofile,Ui_S1_Designation):
    def __init__(self):
        Add.__init__(self)
        Delete.__init__(self)
        Update.__init__(self)
        View.__init__(self)
        Print.__init__(self)
        Change_Password.__init__(self)
        Sign_Out.__init__(self)
        myprofile.__init__(self)

        Add.Handel_Buttons_Add(self)
        Delete.Handel_Buttons_Delete(self)
        Update.Handel_Buttons_Update(self)
        View.Handel_Buttons_View(self)
        Print.Handel_Buttons_Print(self)
        Change_Password.Handel_Buttons_Change_Password(self)
        Sign_Out.Handel_Buttons_Sign_Out(self)
        myprofile.Handel_Buttons_Myprofile(self)
        self.pushButton.clicked.connect(self.Redirect_function)
    def connect(self,host='http://google.com'):
        try:
            urllib.request.urlopen(host)
            self.label_102.setText("Connected")
            #print("connected")
            self.pushButton.setVisible(True)
        except:
            self.label_102.setText("Not Connected")
            #print("Not connected")
            self.pushButton.setVisible(False)
            self.stackedWidget.setCurrentIndex(26)
        threading.Timer(.5, self.connect).start()

    def Redirect_function(self):
        self.stackedWidget.setCurrentIndex(0)
        self.signout_button.setVisible(False)
        self.changepass_button.setVisible(False)
        self.myprofile_button.setVisible(False)
        self.comboBox_input_username.clearEditText()
        self.lineEdit_input_password.clear()
        self.comboBox_input_username.clear()
# ----------------------------------------------------------------------------------------------------------------------------
# def main():
#    window = start()
#    app.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(':/icon.ico'))
    #connect()
    ConnectDatabase()
    window = start()
    app.exec_()