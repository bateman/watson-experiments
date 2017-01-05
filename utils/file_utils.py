# from datetime import datetime as dt
import csv

# s = dt.fromtimestamp(1318118400000).strftime('%Y-%m-%d %H:%M:%S')


def load_corpus(filename, type='txt'):
    _file = open(filename, "rb")
    if type == 'txt':
        reader = _file.readlines()
    elif type == 'csv':
        reader = csv.reader(_file, delimiter=";")
    return reader


def load_emails(filename):
    committers = list()
    with open(filename, "rb") as _file:
        reader = csv.reader(_file, delimiter=";")
        reader.next()  # skip header

        # keys: 'id', 'email', 'alias'
        for line in reader:
            dev = dict()
            dev['id'] = line[0]
            try:
                dev['email'], dev['alias'] = line[2].split(':', 2)
            except ValueError:
                dev['email'] = dev['alias'] = line[2]
            committers.append(dev)

    return committers



