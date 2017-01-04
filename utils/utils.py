# from datetime import datetime as dt
import csv

# s = dt.fromtimestamp(1318118400000).strftime('%Y-%m-%d %H:%M:%S')


def load_corpus(filename, type='txt'):
    _file = open(filename, "rb")
    if type == 'txt':
        reader = _file.readlines()
    elif type == 'csv':
        #dialect = csv.Sniffer().sniff(_file.read(1024), delimiters=";,")
        #_file.seek(0)
        reader = csv.reader(_file, delimiter=";")

    return reader


