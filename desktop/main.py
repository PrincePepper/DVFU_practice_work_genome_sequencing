import sys
import os

from datetime import datetime

from PyQt5.Qt import QMainWindow, QDialog, QApplication, QFileDialog, QScrollArea, QWidget, QVBoxLayout, QLabel
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtWidgets import QLineEdit, QTableWidgetItem, QDialog, QDialogButtonBox, QDesktopWidget
from PyQt5.QtGui import QKeyEvent, QPixmap, QFont, QFontDatabase


class Main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_files/main_window.ui', self)
        self.setWindowTitle("Фильтрация")
        self.choose_file_button.clicked.connect(self.choose_file)
        self.add_range_button.clicked.connect(self.add_range)
        self.start_processing_button.clicked.connect(self.start_processing)
        os.system("if [ -f patterns ]; then rm patterns; fi;")
        self.ranges = []

    def choose_file(self):
        self.file_path = QFileDialog.getOpenFileName(self,
                        "Выбрать файл",
                        ".",
                        "GZ archive(*.gz);;")
        self.current_path_label.setText("".join(self.file_path[0]))

    def add_range(self):
        if int(self.from_line_edit.text()) > int(self.to_line_edit.text()):
            return
        self.ranges.append([int(self.from_line_edit.text()), int(self.to_line_edit.text())])
        patterns_file = open("patterns", "a")
        for i in range(self.ranges[-1][0], self.ranges[-1][1] + 1):
            patterns_file.write(str(i) + '\n')
        patterns_file.close()
        if self.ranges[-1][0] != self.ranges[-1][1]:
            self.ranges_list.addItem(str(self.ranges[-1][0]) + " - " + str(self.ranges[-1][1]))
        else:
            self.ranges_list.addItem(str(self.ranges[-1][0]))

    def start_processing(self):
        os.system("./filter.sh " + self.file_path[0] + " patterns")
        os.rename("output", "output_" + "".join(str(datetime.now()).replace(' ', '_')).split('.')[0] + ".fastq")


app = QApplication(sys.argv)
start_window = Main_window()
start_window.show()

sys.exit(app.exec_())
