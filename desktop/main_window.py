import codecs
import gzip
import logging
import os
import sys
import tempfile
from argparse import ArgumentParser
from datetime import datetime
from itertools import islice

import pkg_resources
from PyQt5 import QtCore
from PyQt5.Qt import *

assert sys.version[0] == '3'
from win32api import GetSystemMetrics

parser = ArgumentParser(description='Sequence filter GUI tool')

parser.add_argument("--debug", action='store_true', help="enable debugging")

args = parser.parse_args()

#
# Configuring logging before other packages are imported
#
if args.debug:
    logging_level = logging.DEBUG
else:
    logging_level = logging.INFO

logging.basicConfig(stream=sys.stderr, level=logging_level, format='%(asctime)s %(levelname)s %(name)s %(message)s')

log_file = tempfile.NamedTemporaryFile(mode='w', prefix='sequences_filter-', suffix='.log', delete=False)
file_handler = logging.FileHandler(log_file.name)
file_handler.setLevel(logging_level)
file_handler.setFormatter(logging.Formatter('%(asctime)s [%(process)d] %(levelname)-8s %(name)-25s %(message)s'))
logging.root.addHandler(file_handler)

logger = logging.getLogger(__name__.replace('__', ''))
logger.info('Spawned')


# -------------------------------------------------------------------------------------------------------------------


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        logger.info('Spawn all object and widget')
        self.plot_window = None  # окно графика
        #
        # TODO: нужно дать описание обьектам ниже
        #
        self.coefficient_per_tile = {}  #
        self.size_file = 0  #
        self.new_file_size = 0  #
        self.max_read = 0  #
        self.file_path = []  #
        self.ranges = []  #
        self.tiles = []  #

        self.ranges_list.setSelectionMode(QListWidget.MultiSelection)
        self.chooseFileButton.clicked.connect(self.choose_file)
        self.addRangeButton.clicked.connect(self.add_range)
        self.startProcessingButton.clicked.connect(self.start_processing)
        # self.paintButton.clicked.connect(self.painting)
        logger.info('Connect all activity')

        #
        # TODO: здесь должна быть проверка на присутвие WSL на Windows
        #

        # 'nt' <- windows
        if os.name == "nt":
            os.system("wsl if [ -f patterns ]; then rm patterns; fi;")
        else:
            os.system(" if [ -f patterns ]; then rm patterns; fi;")
        logger.info('Remove file «patterns»')

    def setupUi(self):
        self.setObjectName("FilterSequence")
        self.setWindowModality(QtCore.Qt.NonModal)
        self.setMaximumSize(QtCore.QSize(int(GetSystemMetrics(0) / 1.5), int(GetSystemMetrics(1) / 1.5)))

        self.setFont(get_monospace_font())
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setWindowIcon(get_app_icon())

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setFormat("%p%")
        self.progressBar.setObjectName("progressBar")
        self.progressBar.hide()
        self.verticalLayout.addWidget(self.progressBar)

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.currentPathLabel = QLabel(self.centralwidget)
        self.currentPathLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.currentPathLabel.setObjectName("current_path_label")
        self.verticalLayout.addWidget(self.currentPathLabel)

        self.chooseFileButton = QPushButton(self.centralwidget)
        self.chooseFileButton.setObjectName("choose_file_button")
        self.verticalLayout.addWidget(self.chooseFileButton)

        spacerItem1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem1)

        self.label = QLabel(self.centralwidget)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        spacerItem2 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)

        self.fromLineEdit = QLineEdit(self.centralwidget)
        self.fromLineEdit.setObjectName("from_line_edit")
        self.horizontalLayout_2.addWidget(self.fromLineEdit)

        spacerItem3 = QSpacerItem(10, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.addRangeButton = QPushButton(self.centralwidget)
        self.addRangeButton.setObjectName("add_range_button")
        self.verticalLayout.addWidget(self.addRangeButton)

        spacerItem4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem4)

        self.startProcessingButton = QPushButton(self.centralwidget)
        self.startProcessingButton.setObjectName("start_processing_button")
        self.verticalLayout.addWidget(self.startProcessingButton)

        spacerItem5 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem5)

        self.paintButton = QPushButton(self.centralwidget)
        self.paintButton.setObjectName("paintButton")
        self.verticalLayout.addWidget(self.paintButton)

        spacerItem6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)

        self.ranges_list = QListWidget(self.centralwidget)
        self.ranges_list.setObjectName("ranges_list")
        self.verticalLayout_5.addWidget(self.ranges_list)

        self.horizontalLayout_3.addLayout(self.verticalLayout_5)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)

        self.list_tail = QListWidget(self.centralwidget)
        self.list_tail.setProperty("showDropIndicator", False)
        self.list_tail.setObjectName("list_tail")
        self.verticalLayout_4.addWidget(self.list_tail)

        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.setCentralWidget(self.centralwidget)

        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("FilterSequence", "FilterSequence"))
        self.chooseFileButton.setText(_translate("FilterSequence", "Выбрать файл для обработки"))
        self.label.setText(_translate("FilterSequence", "Введите диапазон или элементы через запятую для удаления"))
        self.addRangeButton.setText(_translate("FilterSequence", "Добавить"))
        self.startProcessingButton.setText(_translate("FilterSequence", "Начать обработку"))
        self.paintButton.setText(_translate("FilterSequence", "Нарисовать график наших данных"))
        self.label_4.setText(_translate("FilterSequence", "Список тайлов на удаления"))
        self.ranges_list.setSortingEnabled(True)
        self.label_2.setText(_translate("FilterSequence", "Список существующих тайлов"))

    def painting(self):
        self.plot_window = PlotWindow()
        self.plot_window.show()
        logger.info('Start drawing the graph')

    def choose_file(self):
        logger.info('File upload process')
        self.file_path = QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "GZ archive(*.gz);;")
        if len(self.file_path) != 0:
            if str(self.file_path[0]) != '':
                # ограничения на длину выводимой строки
                if len(self.file_path[0]) > 40:
                    temp_str = str("..." + self.file_path[0][len(self.file_path[0]) - 40:])
                    self.currentPathLabel.setText(temp_str)
                else:
                    self.currentPathLabel.setText(str(self.file_path[0]))

                self.progressBar.show()
                msg = QMessageBox()
                msg.setText('процесс загрузки файла, ожидайте')
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
                # logger.info('Parsing started')
                # self.parse()
                # logger.info('Parsing finished')
                msg.accept()
                msg.setText('Готово')
                logger.info('Done')

                self.progressBar.hide()

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
        temp_ranges = self.fromLineEdit.text()
        if len(temp_ranges) <= 0:
            return
        for i, char in enumerate(temp_ranges):
            if char.isalpha():
                logger.error(
                    'This string has forbidden characters: ' + '«' + char + '»' + ' in position - ' + str(i + 1))
                # отображение ошибки
                show_error('Ошибка в строке', 'присутвуют буквы', 'они запрешены', blocking=True)
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
            # wsl ./filter.sh 'filepath'  patterns
            os.system("wsl ./filter.sh " + temp_path + " patterns")
            os.rename("output",
                      "output" + "".join(str(datetime.now())
                                         .replace(' ', '_')).replace(':', '').split('.')[0] + ".fastq")
        else:
            os.system("./filter.sh " + self.file_path[0] + " patterns")
            os.rename("output",
                      "output" + "".join(str(datetime.now()).replace(' ', '_')).split('.')[0] + ".fastq")

        msg = QMessageBox()
        msg.setText('Файл готов')
        logger.info('File is ready after the operation')
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def parse(self):
        with gzip.open(self.file_path[0], 'rb') as file:
            old_file_position = file.tell()
            file.seek(0, os.SEEK_END)
            self.size_file = file.tell()
            file.seek(old_file_position, os.SEEK_SET)

            for line in islice(file, 1, 2):  # <--- change 1 to 2 and 16 to None314871519
                self.max_read = len(line)

        with gzip.open(self.file_path[0], 'rb') as file:
            for pos, line in enumerate(file):
                self.new_file_size = file.tell()
                self.progressBar.setProperty("value", remap(self.new_file_size, 0, self.size_file, 0, 100))
                self.update()
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
                self.num_of_n = [0] * self.max_read
                self.coefficient_per_tile[self.cur_tile] = [0] * self.max_read
            self.num_of_read += 1
            for i in range(self.max_read):
                if line[i].lower() == 'n':
                    self.num_of_n[i] += 1
                self.coefficient_per_tile[self.cur_tile][i] = self.num_of_n[i] / self.num_of_read


class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("График")
        self.resize(500, 570)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawBrushes(painter)

    def drawBrushes(self, qp):
        data = dict()

        for row in self.coefficient_per_tile:
            r = list()
            for column in self.coefficient_per_tile[row]:
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
        height = total_height / len(self.coefficient_per_tile)

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


#
# установление шрифта в приложении
#
def get_monospace_font():
    preferred = ['Roboto', 'Consolas', 'Monospace', 'Lucida Console', 'Monaco']
    for name in preferred:
        font = QFont(name)
        if QFontInfo(font).fixedPitch():
            logger.debug('Preferred monospace font: %r', font.toString())
            return font

    font = QFont()
    font.setStyleHint(QFont().Monospace)
    font.setFamily('monospace')
    font.setPointSize(11)
    font.setBold(False)
    logger.debug('Using fallback monospace font: %r', font.toString())
    return font


#
# подгрузка иконки приложения
#
def get_app_icon():
    global _APP_ICON_OBJECT
    try:
        return _APP_ICON_OBJECT
    except NameError:
        pass
    # noinspection PyBroadException
    try:  # sequences_filter_gui_tool
        fn = pkg_resources.resource_filename(__name__, os.path.join('icons', 'logo.png'))
        _APP_ICON_OBJECT = QIcon(fn)
    except Exception:
        logger.error('Could not load icon', exc_info=True)
        _APP_ICON_OBJECT = QIcon()
    return _APP_ICON_OBJECT


#
# создание окна с ощибкой
#
def show_error(title, text, informative_text, parent=None, blocking=False):
    mbox = QMessageBox(parent)

    mbox.setWindowTitle(str(title))
    mbox.setText(str(text))
    if informative_text:
        mbox.setInformativeText(str(informative_text))

    mbox.setIcon(QMessageBox.Critical)
    mbox.setStandardButtons(QMessageBox.Ok)

    if blocking:
        mbox.exec()
    else:
        mbox.show()  # Not exec() because we don't want it to block!


#
# каст значений
#
def remap(value, fromLow, fromHigh, toLow, toHigh):
    return (value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow
