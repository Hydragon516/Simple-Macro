from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QLabel, QDialog, QApplication, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout
import pyautogui as pag
import datetime
import time

class MyMainGUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.macro_state = 'STOP'

        self.target_hour = 0
        self.target_min = 0
        self.target_sec = 0
        self.target_time = ''
        self.update_target_time()

        self.target_x = 0
        self.target_y = 0
        self.target_position = ''
        self.update_target_position()

        self.time_state = 'READY'
        self.h_time_state = 'READY'
        self.m_time_state = 'READY'
        self.s_time_state = 'READY'

        self.position_state = 'READY'
        self.x_position_state = 'READY'
        self.y_position_state = 'READY'

        self.time_label = QLabel(self)
        self.mouse_label = QLabel(self)
        self.time_state_label = QLabel(self)
        self.position_state_label = QLabel(self)

        self.btn1 = QPushButton("START", self)
        self.btn1.move(100, 100)
        self.btn1.setCheckable(True)
        self.btn1.toggled.connect(self.slot_toggle)

        self.target_hour_qline = QLineEdit(self)
        self.target_min_qline = QLineEdit(self)
        self.target_sec_qline = QLineEdit(self)

        self.target_x_position_qline = QLineEdit(self)
        self.target_y_position_qline = QLineEdit(self)

        self.target_hour_qline.textChanged[str].connect(self.h_set)
        self.target_min_qline.textChanged[str].connect(self.m_set)
        self.target_sec_qline.textChanged[str].connect(self.s_set)

        self.target_x_position_qline.textChanged[str].connect(self.x_set)
        self.target_y_position_qline.textChanged[str].connect(self.y_set)

        time_hbox = QHBoxLayout()
        time_hbox.addWidget(QLabel('Current Time : ', self))
        time_hbox.addWidget(self.time_label)
        time_hbox.addStretch(1)

        mouse_hbox = QHBoxLayout()
        mouse_hbox.addWidget(QLabel('Mouse Position : ', self))
        mouse_hbox.addWidget(self.mouse_label)
        mouse_hbox.addStretch(1)

        set_time_hbox = QHBoxLayout()
        set_time_hbox.addWidget(QLabel('Target Time : ', self))
        set_time_hbox.addWidget(self.target_hour_qline)
        set_time_hbox.addWidget(self.target_min_qline)
        set_time_hbox.addWidget(self.target_sec_qline)
        set_time_hbox.addStretch(1)

        time_state_hbox = QHBoxLayout()
        time_state_hbox.addWidget(QLabel('Time State : ', self))
        time_state_hbox.addWidget(self.time_state_label)
        time_state_hbox.addStretch(1)

        set_position_hbox = QHBoxLayout()
        set_position_hbox.addWidget(QLabel('Target Position : ', self))
        set_position_hbox.addWidget(self.target_x_position_qline)
        set_position_hbox.addWidget(self.target_y_position_qline)
        set_position_hbox.addStretch(1)

        position_state_hbox = QHBoxLayout()
        position_state_hbox.addWidget(QLabel('Position State : ', self))
        position_state_hbox.addWidget(self.position_state_label)
        position_state_hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addLayout(time_hbox)
        vbox.addLayout(mouse_hbox)
        vbox.addLayout(set_time_hbox)
        vbox.addLayout(time_state_hbox)
        vbox.addLayout(set_position_hbox)
        vbox.addLayout(position_state_hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

        self.setWindowTitle('Simple Macro')
        self.setGeometry(100, 50, 300, 400)
    
    def slot_toggle(self, state):
        self.btn1.setText({True: "STOP", False: "START"}[state])
    
    def update_target_time(self):
        self.target_time = str(self.target_hour) \
        + ':' + str(self.target_min) \
        + ':' + str(self.target_sec)

    def update_target_position(self):
        self.target_positon = str(self.target_x) + ':' + str(self.target_y)
    
    def update_time_state_label(self):
        if (self.h_time_state == 'READY' and self.m_time_state == 'READY' and self.s_time_state == 'READY'):
            self.time_state = 'READY'
        
        else:
            self.time_state = 'ERROR'
        
        self.time_state_label.setText(self.time_state)

    def update_position_state_label(self):
        if (self.x_position_state == 'READY' and self.y_position_state == 'READY'):
            self.position_state = 'READY'
        
        else:
            self.position_state = 'ERROR'
        
        self.position_state_label.setText(self.position_state)

    def h_set(self, text):
        if text.isdigit():
            self.target_hour = int(text)

            if (self.target_hour > 23 or self.target_hour < 0):
                self.h_time_state = 'ERROR'
            
            else:
                self.h_time_state = 'READY'
                self.update_target_time()
        
        else:
            self.h_time_state = 'ERROR'
            
        self.update_time_state_label()
        
    def m_set(self, text):
        if text.isdigit():
            self.target_min = int(text)

            if (self.target_min > 59 or self.target_min < 0):
                self.m_time_state = 'ERROR'
            
            else:
                self.m_time_state = 'READY'
                self.update_target_time()
        
        else:
            self.m_time_state = 'ERROR'
            
        self.update_time_state_label()

    def s_set(self, text):
        try:
            self.target_sec = float(text)

            if (self.target_sec >= 60 or self.target_sec < 0):
                self.s_time_state = 'ERROR'
            
            else:
                self.s_time_state = 'READY'
                self.update_target_time()
            
            self.update_time_state_label()
        
        except:
            self.s_time_state = 'ERROR'
            self.update_time_state_label()
    
    def x_set(self, text):
        if text.isdigit():
            self.target_x = int(text)
            self.x_position_state = 'READY'
            self.update_target_position()

        else:
            self.x_position_state = 'ERROR'
            
        self.update_position_state_label()
    
    def y_set(self, text):
        if text.isdigit():
            self.target_y = int(text)
            self.y_position_state = 'READY'

        else:
            self.y_position_state = 'ERROR'
            
        self.update_position_state_label()

    
class MyMain(MyMainGUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.th = Worker(parent=self)
        self.th.start()

        self.btn1.clicked.connect(self.macro_ready)

        self.th.current_time.connect(self.time_update)
        self.th.mouse_position.connect(self.mouse_update)

        self.show()

    def macro_ready(self):
        if (self.position_state == 'READY' and self.time_state == 'READY'):
            if self.macro_state == 'STOP':
                self.macro_state = 'START'
                
            elif self.macro_state == 'START':
                self.macro_state = 'STOP'
        
        else:
            self.slot_toggle(False)

    def time_update(self, msg):
        self.time_label.setText(msg)
        msg = msg.split(':')
        h = msg[0]
        m = msg[1]
        s = msg[2]

        if self.macro_state == 'START':
            if (self.target_hour == int(h) and self.target_min == int(m) and self.target_sec <= float(s)):
                self.macro_start()
    
    def mouse_update(self, msg):
        self.mouse_label.setText(msg)
    
    def macro_start(self):
        pag.moveTo(self.target_x, self.target_y)

        cnt = 0
        while True:
            pag.click()
            pag.press('enter')
            cnt = cnt + 1

            if cnt > 3:
                self.macro_state = 'STOP'
                self.slot_toggle(False)
                break


class Worker(QThread):
    current_time = pyqtSignal(str)
    mouse_position = pyqtSignal(str)

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.working = False

    def run(self):
        while True:
            # get current time
            dt = datetime.datetime.now()
            time.sleep(0.001)
            date = str(dt).split()
            day_time = date[1]
            self.current_time.emit(day_time)

            # get mouse position
            x, y = pag.position()
            pos = str(x) + ', ' + str(y)
            self.mouse_position.emit(pos)



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = MyMain()
    app.exec_()