import gzip
import codecs


def main():
    data = []
    str_count = 1000 * 4
    filename = 'R39-L6-READ2.gz'
    new_filename = 'test_' + filename.split('.')[0] + '-Sequences.txt'

    with gzip.open(filename, 'rb') as file:
        for pos, line in enumerate(file):
            if pos >= str_count:
                break
            line = codecs.decode(line, 'UTF-8')
            data.append(line)

    with open(new_filename, 'w') as file:
        for line in data:
            file.write(line)


if __name__ == '__main__':
    main()

