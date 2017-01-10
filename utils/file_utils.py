# from datetime import datetime as dt
import csv

# s = dt.fromtimestamp(1318118400000).strftime('%Y-%m-%d %H:%M:%S')


def load_corpus(filename, type='txt', delim=";"):
    _file = open(filename, "rb")
    if type == 'txt':
        reader = _file.readlines()
    elif type == 'csv':
        reader = csv.reader(_file, delimiter=delim)
    return reader, _file


def save_corpus(corpus, filename, delim=';'):
    with open(filename, 'wb') as _file:
        writer = csv.writer(_file, delimiter=delim)
        for row in corpus:
            try:
                writer.writerow(row)
            except Exception:
                pass
    _file.close()


def load_core_team_members(filename):
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



