import codecs
import sys
import gzip
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


class FileParser:
    def __init__(self, filename):
        self.__filename = filename
        self.data = {}
        self.read = []
        self.tile_num = str()

    def parse(self):
        if '.gz' in self.__filename:
            self.__gz_parse()
        else:
            self.__txt_parse()
        return self.data

    def __file_iteration(self, pos, line):
        if pos % 4 == 0:
            self.tile_num = line.split(':')[2]
        self.read.append(line)

        if pos % 4 == 3:
            if self.tile_num not in self.data:
                self.data[self.tile_num] = []
            self.data[self.tile_num].append(self.read.copy())
            self.read = []

    def __txt_parse(self):
        with open(self.__filename, 'r') as file:
            for pos, line in enumerate(file):
                self.__file_iteration(pos, line)

    def __gz_parse(self):
        with gzip.open(self.__filename, 'rb') as file:
            for pos, line in enumerate(file):
                line = codecs.decode(line, 'UTF-8')
                self.__file_iteration(pos, line)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.all_data = {}
        # {'tile'': [['id', 'нуклеотид', 'id', 'quality'],[...]]}
        self.useless_data = {}
        # тоже что и all_data, но то что будет выброшено при чистке
        self.tiles_pool = []
        # список тайлов которые необходимо удалить

        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)
        openFile = self.actionOpen
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)
        self.deleteTilesButton.clicked.connect(self.deleteTiles)
        self.acceptAddTileButton.clicked.connect(self.addUselessTile)
        self.exportToFilesButton.clicked.connect(self.exportToFiles)

    def addUselessTile(self):
        tile = self.addTileTextEdit.toPlainText()
        if tile in self.tiles_pool or tile not in self.all_data:
            return
        self.tiles_pool.append(tile)
        self.createDeleteTileList()

    def createDeleteTileList(self):
        self.deleteTileList.clear()
        for pos, i in enumerate(self.tiles_pool):
            self.deleteTileList.addItem(i)

    def showDialog(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        if file_name == '':
            return
        self.all_data = FileParser(file_name).parse()
        self.createAllTileList()

    def createAllTileList(self):
        self.allTileList.clear()
        for pos, i in enumerate(self.all_data):
            self.allTileList.addItem(i)

    def deleteTiles(self):
        for pos, i in enumerate(self.tiles_pool):
            self.useless_data[i] = self.all_data[i]
            self.all_data.pop(i)
        self.tiles_pool = []
        self.createAllTileList()
        self.createDeleteTileList()

    def exportToFiles(self):
        with gzip.open('cut_sequence.txt.gz', 'wb') as file:
            for tile in self.all_data.values():
                for read in tile:
                    for line in read:
                        file.write(codecs.encode(line, 'UTF-8'))
        with gzip.open('useless_sequence.txt.gz', 'wb') as file:
            for tile in self.useless_data.values():
                for read in tile:
                    for line in read:
                        file.write(codecs.encode(line, 'UTF-8'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
