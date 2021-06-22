import codecs
import gzip
import sys
import os
from datetime import datetime
from itertools import islice

from PyQt5.Qt import *
from PyQt5 import uic, QtCore

import warnings

warnings.filterwarnings('ignore')

plot_window = None
coefficient_per_tile = {}
max_read = 0

class Main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_files/main_window.ui', self)
        self.file_path = []
        self.ranges = []
        self.tiles = []

        self.progressBar_label.hide()
        self.progressBar.hide()

        self.ranges_list.setSelectionMode(QListWidget.MultiSelection)
        self.choose_file_button.clicked.connect(self.choose_file)
        self.add_range_button.clicked.connect(self.add_range)
        self.start_processing_button.clicked.connect(self.start_processing)
        self.paint.clicked.connect(self.painting)
        if os.name == "nt":
            os.system("wsl if [ -f patterns ]; then rm patterns; fi;")
        else:
            os.system(" if [ -f patterns ]; then rm patterns; fi;")

    def painting(self):
        global plot_window
        plot_window = Plot_window()
        plot_window.show()

    def choose_file(self):
        self.file_path = QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "GZ archive(*.gz);;")
        if len(self.file_path) != 0:
            if str(self.file_path[0]) != '':
                self.current_path_label.setText(str(self.file_path[0]))
                # self.progressBar_label.show()
                # self.progressBar.show()
                msg = QMessageBox()
                msg.setText('процесс загрузки файла, ожидайте')
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
                self.parse()
                msg.accept()
                msg.setText('Готово')
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                self.createAllTileList()
                self.update()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            listItems = self.ranges_list.selectedItems()
            if not listItems:
                return
            for item in listItems:
                self.ranges_list.takeItem(self.ranges_list.row(item))
                for pos, j in enumerate(self.ranges):
                    if j == int(item.text()):
                        self.ranges.pop(pos)

        open('patterns', 'w').close()
        patterns_file = open("patterns", "a")
        for i in range(len(self.ranges)):
            patterns_file.write(str(self.ranges[i]) + '\n')
        patterns_file.close()
        event.accept()

    def createAllTileList(self):
        self.list_tail.clear()
        for pos, i in enumerate(self.tiles):
            self.list_tail.addItem(i)

    def add_range(self):
        temp_ranges = self.from_line_edit.text()
        if len(temp_ranges) <= 0:
            return
        for char in temp_ranges:
            if char.isalpha():
                return
        temp_ranges = temp_ranges.replace(' ', '').replace(',', ' ').split()

        for i in temp_ranges:
            if i.find('-') != -1:
                temp_temp_ranges = list(map(int, i.replace('-', ' ').split()))
                for i in range(temp_temp_ranges[0], temp_temp_ranges[1] + 1):
                    self.ranges.append(i)
            else:
                self.ranges.append(int(i))
        self.ranges = sorted(list(map(int, set(self.ranges))))

        open('patterns', 'w').close()
        patterns_file = open("patterns", "a")
        self.ranges_list.clear()
        for i in range(len(self.ranges)):
            patterns_file.write(str(self.ranges[i]) + '\n')
            self.ranges_list.addItem(str(self.ranges[i]))
        patterns_file.close()

    def start_processing(self):
        if os.name == "nt":
            temp_path = self.file_path[0]
            temp_path = '/mnt/' + temp_path[0].lower() + temp_path[2:]
            os.system("wsl ./filter.sh " + temp_path + " patterns")
            os.rename("output",
                      "output" + "".join(str(datetime.now())
                                         .replace(' ', '_')).replace(':', '').split('.')[0] + ".fastq")
        else:
            os.system("./filter.sh " + self.file_path[0] + " patterns")
            os.rename("output",
                      "output" + "".join(str(datetime.now()).replace(' ', '_')).split('.')[0] + ".fastq")

    def parse(self):
        global max_read
        with gzip.open(self.file_path[0], 'rb') as file:
            for line in islice(file, 1, 2):  # <--- change 1 to 2 and 16 to None314871519
                max_read = len(line)
        with gzip.open(self.file_path[0], 'rb') as file:
            for pos, line in enumerate(file):
                line = codecs.decode(line, 'UTF-8')
                self.__file_iteration(pos, line)

    def __file_iteration(self, pos, line):
        if pos % 4 == 0:
            self.cur_tile = line.split(':')[2]

        if self.cur_tile not in self.tiles:
            self.num_of_read = 0
            self.tiles.append(self.cur_tile)
        if pos % 4 == 1:
            if self.num_of_read == 0:  # init self.__num_of_n
                self.num_of_n = [0] * max_read
                coefficient_per_tile[self.cur_tile] = [0] * max_read
            self.num_of_read += 1
            for i in range(max_read):
                if line[i].lower() == 'n':
                    self.num_of_n[i] += 1
                coefficient_per_tile[self.cur_tile][i] = self.num_of_n[i] / self.num_of_read


class Plot_window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_files/plot_window.ui', self)
        self.setWindowTitle("График")

    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawBrushes(painter)

    def drawBrushes(self, qp):
        data = dict()

        for row in coefficient_per_tile:
            r = list()
            for column in coefficient_per_tile[row]:
                value = column * 5220
                if value > 256:
                    r.append(256)
                else:
                    r.append(value)
            data[row] = r

        total_width = 500
        total_height = 550
        global max_read
        width = total_width / max_read
        height = total_height / len(coefficient_per_tile)

        x = 20
        y = 0

        count = 0
        for row in data:
            x = 0
            qp.setBrush(QColor(200, 0, 0))
            qp.setPen(QColor(0, 0, 0))
            qp.drawText(330, y + height / 2, 30, height, 0, row)

            for column in data[row]:
                brush = QBrush(Qt.SolidPattern)
                pen = QPen(Qt.SolidLine)
                pen.setColor(QColor(column, column, column))
                brush.setColor(QColor(column, column, column))

                qp.setBrush(brush)
                qp.setPen(pen)

                qp.drawRect(x, y, width, height)
                x = x + width

            y = y + height

        x = 0
        qp.setBrush(QColor(200, 0, 0))
        qp.setPen(QColor(0, 0, 0))

        total_potracheno = 0

        current_number = 1

        chegoto_per_symbol = 9

        while total_potracheno < total_width and current_number < max_read:
            current_width = len(str(current_number)) * chegoto_per_symbol
            qp.drawText(x, y, current_width, height, 0, str(current_number))
            x += current_width
            current_number += round(len(str(current_number)) * 1.3)
            total_potracheno += current_width


app = QApplication(sys.argv)
start_window = Main_window()
start_window.show()

sys.exit(app.exec_())
