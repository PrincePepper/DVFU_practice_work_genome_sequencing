import re
import sys
import os
import subprocess
from datetime import datetime

from PyQt5.Qt import QMainWindow, QDialog, QApplication, QFileDialog, QListWidget
from qtpy import uic, QtCore


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_files/main_window.ui', self)
        self.file_path = []
        self.ranges_list.setSelectionMode(QListWidget.MultiSelection)
        self.choose_file_button.clicked.connect(self.choose_file)
        self.add_range_button.clicked.connect(self.add_range)
        self.start_processing_button.clicked.connect(self.start_processing)
        if os.name == "nt":
            os.system("wsl if [ -f patterns ]; then rm patterns; fi;")
        else:
            os.system(" if [ -f patterns ]; then rm patterns; fi;")
        self.ranges = []

    def choose_file(self):
        self.file_path = QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "GZ archive(*.gz);;")
        self.current_path_label.setText(str(self.file_path[0]))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            listItems = self.ranges_list.selectedItems()
            if not listItems:
                return
            for item in listItems:
                self.ranges_list.takeItem(self.ranges_list.row(item))
        event.accept()

    def add_range(self):
        if len(self.from_line_edit.text()) <= 0:
            return

        temp_ranges = self.from_line_edit.text()
        temp_ranges = temp_ranges.replace(',', ' ').split()

        for i in temp_ranges:
            if i.find('-') != -1:
                temp_temp_ranges = list(map(int, i.replace('-', ' ').split()))
                for i in range(temp_temp_ranges[0], temp_temp_ranges[1] + 1):
                    self.ranges.append(i)
            else:
                self.ranges.append(int(i))
        self.ranges = list(set(self.ranges))
        patterns_file = open("patterns", "a")
        for i in range(len(self.ranges)):
            patterns_file.write(str(self.ranges[i]) + '\n')
            self.ranges_list.addItem(str(self.ranges[i]))
        patterns_file.close()

    def start_processing(self):
        if len(self.file_path) != 0:
            if str(self.file_path[0]) != "\"":
                if os.name == "nt":
                    os.system("wsl ./filter.sh " + self.file_path[0] + " patterns")
                    os.rename("output","output_" + "".join(str(datetime.now()).replace(' ', '_')).split('.')[0] + ".fastq")
                else:
                    os.system("./filter.sh " + self.file_path[0] + " patterns")
                    os.rename("output", "output_" + "".join(str(datetime.now()).replace(' ', '_')).split('.')[0] + ".fastq")


app = QApplication(sys.argv)
start_window = MainWindow()
start_window.show()

sys.exit(app.exec_())
