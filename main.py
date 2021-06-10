import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
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
        uic.loadUi('main.ui', self)
        openFile = self.actionOpen
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)
        self.deleteTilesButton.clicked.connect(self.deleteTiles)
        self.acceptAddTileButton.clicked.connect(self.addUselessTile)
        self.exportToFilesButton.clicked.connect(self.exportToFiles)
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
        if tile in self.tiles_pool or tile not in self.all_data:
            return
        self.addTileTextEdit.clear()
        self.tiles_pool.append(tile)
        self.createUselessTileList()

    def createUselessTileList(self):
        self.uselessTileList.clear()
        for pos, i in enumerate(self.tiles_pool):
            self.uselessTileList.addItem(i)

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
        self.createUselessTileList()

    def exportToFiles(self):
        if not self.useless_data:
            return
        FileParser('cut_sequence.txt.gz').createFile(self.all_data)
        FileParser('useless_sequence.txt.gz').createFile(self.useless_data)
        self.useless_data = {}
        msg = QMessageBox()
        msg.setText('Done')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
