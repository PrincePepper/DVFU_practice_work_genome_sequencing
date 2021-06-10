import gzip
import codecs


class FileParser:
    def __init__(self, filename):
        self.__filename = filename
        self.__data = {}
        self.__read = []
        self.__tile_num = str()

    def parse(self):
        if '.gz' in self.__filename:
            self.__gz_parse()
        else:
            self.__txt_parse()
        return self.__data

    def createFile(self, data):
        with gzip.open(self.__filename, 'wb') as file:
            for tile in data.values():
                for read in tile:
                    for line in read:
                        file.write(codecs.encode(line, 'UTF-8'))

    def __file_iteration(self, pos, line):
        if pos % 4 == 0:
            self.__tile_num = line.split(':')[2]
        self.__read.append(line)

        if pos % 4 == 3:
            if self.__tile_num not in self.__data:
                self.__data[self.__tile_num] = []
            self.__data[self.__tile_num].append(self.__read.copy())
            self.__read = []

    def __txt_parse(self):
        with open(self.__filename, 'r') as file:
            for pos, line in enumerate(file):
                self.__file_iteration(pos, line)

    def __gz_parse(self):
        with gzip.open(self.__filename, 'rb') as file:
            for pos, line in enumerate(file):
                line = codecs.decode(line, 'UTF-8')
                self.__file_iteration(pos, line)
