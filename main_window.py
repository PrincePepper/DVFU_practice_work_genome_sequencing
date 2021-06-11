from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5 import QtCore
from file_parser import FileParser


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
        uic.loadUi('main_window.ui', self)
        openFile = self.actionOpen
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.parseFileToData)
        self.deleteTilesButton.clicked.connect(self.deleteTiles)
        self.acceptAddTileButton.clicked.connect(self.addUselessTile)
        self.exportToFilesButton.clicked.connect(self.exportToFiles)
        self.clearUselessTilesButton.clicked.connect(self.clearUselessTiles)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key.Key_Delete:
            self.deleteUselessTile()

    # удаляет из списка тайлов, которые необходимо удалить, выделенный тайл
    def deleteUselessTile(self):
        items = self.uselessTileList.selectedItems()
        for i in items:
            self.tiles_pool.remove(i.text())
        self.createUselessTileList()

    # очищает списко тайлов, которые необходимо удалить
    def clearUselessTiles(self):
        self.uselessTileList.clear()
        self.tiles_pool = []

    # добавляет в список тайл, который необходимо удалить, из text edit
    def addUselessTile(self):
        tile = self.addTileTextEdit.toPlainText()
        if tile in self.tiles_pool or tile not in self.all_data:
            return
        self.addTileTextEdit.clear()
        self.tiles_pool.append(tile)
        self.createUselessTileList()

    # создает список тайлов, которые необходимо удалить, из self.tiles_pool
    def createUselessTileList(self):
        self.uselessTileList.clear()
        for pos, i in enumerate(self.tiles_pool):
            self.uselessTileList.addItem(i)

    # создает окно выбора файла и парсит файл в self.all_data
    def parseFileToData(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open File With Data')[0]
        if file_name == '':
            return
        self.all_data = FileParser(file_name).parse()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Done')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.createAllTileList()

    # создает список тайлов, которые присутствуют в файле
    def createAllTileList(self):
        self.allTileList.clear()
        for pos, i in enumerate(self.all_data):
            self.allTileList.addItem(i)

    # удаляет лишние тайлы из self.all_data и записывает их в self.useless_data
    def deleteTiles(self):
        for pos, i in enumerate(self.tiles_pool):
            self.useless_data[i] = self.all_data[i]
            self.all_data.pop(i)
        self.tiles_pool = []
        self.createAllTileList()
        self.createUselessTileList()

    # экспортит данные в два файла: с полезными и лишними данными
    def exportToFiles(self):
        if not self.useless_data:
            return
        name_useless = QFileDialog.getSaveFileName(self, 'Save Useless Data')[0]
        name_all = QFileDialog.getSaveFileName(self, 'Save Useful Data')[0]
        if name_all == '':
            name_all = 'useful.txt.gz'
        if name_useless == '':
            name_useless = 'useless_sequence.txt.gz'
        name_all = ''.join(name_all.split('.')) + '.txt.gz'
        name_useless = ''.join(name_useless.split('.')) + '.txt.gz'
        FileParser(name_useless).createFile(self.useless_data)
        FileParser(name_all).createFile(self.all_data)
        self.useless_data = {}
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Done')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
