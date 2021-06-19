import gzip
import codecs


class FileParser:
    def __init__(self, filename):
        self.__filename = filename

        # to return
        self.__tiles = []
        self.__max_read = 0
        self.__coefficient_per_tile = {}

        # for get data from file
        self.__cur_tile = str()
        self.__num_of_n = []
        self.__num_of_read = 0

    def createFiles(self, useful, useless, tiles_pool):
        print('Creating files....')
        if '.gz' in self.__filename:
            with gzip.open(self.__filename, 'rb') as default_file, \
                    gzip.open(useless, 'wb') as useless_file, \
                    gzip.open(useful, 'wb') as useful_file:
                for pos, line in enumerate(default_file):
                    line = codecs.decode(line, 'UTF-8')
                    self.__write(pos, line, useless_file, useful_file,
                                 tiles_pool)
        else:
            with open(self.__filename, 'r') as default_file, \
                    gzip.open(useless, 'wb') as useless_file, \
                    gzip.open(useful, 'wb') as useful_file:
                for pos, line in enumerate(default_file):
                    self.__write(pos, line, useless_file, useful_file,
                                 tiles_pool)

    def __write(self, pos, line, useless_file, useful_file, tiles_pool):
        if pos % 4 == 0:
            self.__cur_tile = line.split(':')[2]

        if self.__cur_tile not in self.__tiles:
            print(self.__cur_tile)
            self.__tiles.append(self.__cur_tile)

        if self.__cur_tile in tiles_pool:
            useless_file.write(codecs.encode(line, 'UTF-8'))
        else:
            useful_file.write(codecs.encode(line, 'UTF-8'))

    def parse(self):
        print('Reading file...')
        if '.gz' in self.__filename:
            self.__gz_parse()
        else:
            self.__txt_parse()
        return self.__tiles, self.__max_read, self.__coefficient_per_tile

    def __txt_parse(self):
        with open(self.__filename, 'r') as file:
            for pos, line in enumerate(file):
                self.__file_iteration(pos, line)

    def __gz_parse(self):
        with gzip.open(self.__filename, 'rb') as file:
            for pos, line in enumerate(file):
                line = codecs.decode(line, 'UTF-8')
                self.__file_iteration(pos, line)

    def __file_iteration(self, pos, line):
        if pos % 4 == 0:
            self.__cur_tile = line.split(':')[2]

        if self.__cur_tile not in self.__tiles:
            print(self.__cur_tile)
            self.__num_of_read = 0
            self.__tiles.append(self.__cur_tile)

        if pos % 4 == 1:
            str_len = len(line)
            self.__max_read = max(self.__max_read, str_len)
            if self.__num_of_read == 0:  # init self.__num_of_n
                self.__num_of_n = [0] * self.__max_read
                self.__coefficient_per_tile[self.__cur_tile] = \
                    [0] * self.__max_read
            self.__num_of_read += 1
            for i in range(str_len):
                if line[i].lower() == 'n':
                    self.__num_of_n[i] += 1
                self.__coefficient_per_tile[self.__cur_tile][i] = \
                    self.__num_of_n[i] / self.__num_of_read
