from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5 import QtCore
from file_parser import FileParser


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tiles = []
        self.coefficient_per_tile = {}
        self.max_read = 0
        self.file_path = str()

        self.tiles_pool = []

        self.initUI()

    def initUI(self):
        uic.loadUi('main_window.ui', self)
        openFile = self.actionOpen
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.parseFileToData)
        self.deleteTilesButton.clicked.connect(self.deleteTiles)
        self.acceptAddTileButton.clicked.connect(self.addUselessTile)
        # self.exportToFilesButton.clicked.connect(self.exportToFiles)
        self.clearUselessTilesButton.clicked.connect(self.clearUselessTiles)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key.Key_Delete:
            self.deleteUselessTile()

    def deleteUselessTile(self):
        items = self.uselessTileList.selectedItems()
        for i in items:
            self.tiles_pool.remove(i.text())
        self.createUselessTileList()

    def clearUselessTiles(self):
        self.uselessTileList.clear()
        self.tiles_pool = []

    def addUselessTile(self):
        tile = self.addTileTextEdit.toPlainText()
        if tile in self.tiles_pool or tile not in self.tiles:
            return
        self.addTileTextEdit.clear()
        self.tiles_pool.append(tile)
        self.createUselessTileList()

    def createUselessTileList(self):
        self.uselessTileList.clear()
        for pos, i in enumerate(self.tiles_pool):
            self.uselessTileList.addItem(i)

    def parseFileToData(self):
        self.file_path = QFileDialog.getOpenFileName(self, 'Open File With Data')[0]
        if self.file_path == '':
            return
        self.tiles, self.max_read, self.coefficient_per_tile = FileParser(
            self.file_path).parse()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Done')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.createAllTileList()

    def createAllTileList(self):
        self.allTileList.clear()
        for pos, i in enumerate(self.tiles):
            self.allTileList.addItem(i)

    def deleteTiles(self):
        name_useless = QFileDialog.getSaveFileName(self, 'Save Useless Data')[0]
        if name_useless == '':
            name_useless = 'useless_sequence.txt.gz'
        name_all = QFileDialog.getSaveFileName(self, 'Save Useful Data')[0]
        if name_all == '':
            name_all = 'useful_sequence.txt.gz'

        name_all = ''.join(name_all.split('.')) + '.txt.gz'
        name_useless = ''.join(name_useless.split('.')) + '.txt.gz'

        FileParser(self.file_path).createFiles(name_all, name_useless,
                                               self.tiles_pool)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Done')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

        for i in self.tiles:
            if i in self.tiles_pool:
                self.tiles.remove(i)
        self.tiles_pool = []

        self.createAllTileList()
        self.createUselessTileList()
