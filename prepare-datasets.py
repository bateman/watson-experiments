from utils import file_utils
import os
from time import strptime


def retrieve_trust_score(dev, month, year):
    score = 'NA'
    filename = 'results{0}{1}.csv'.format(os.sep, dev)
    month_no = as_number(month)
    try:
        dev_reader, _file = file_utils.load_corpus(filename)
        for row in dev_reader:
            date, s = row.split(';', 2)
            if date == '{0}-{1}'.format(year, month_no):
                s = float(s.strip())
                if s < 0.5:
                    score = 'LOW'
                else:
                    score = 'HIGH'
                break
        _file.close()
    except IOError:
        pass

    return score


def as_number(month):
    m = str(strptime(month, '%b').tm_mon)
    if len(m) == 1:
        m = '0' + m
    return m


def main():
    dataset = list()
    header = ('PRid', 'Successful', 'PropensityToTrust')
    dataset.append(header)

    # open PR
    open_pr_reader, _file = file_utils.load_corpus('open-pullrequests.csv')
    build_dataset(dataset, open_pr_reader)
    _file.close()

    # closed PR
    closed_pr_reader, _file = file_utils.load_corpus('closed-pullrequests.csv')
    build_dataset(dataset, closed_pr_reader)
    _file.close()

    file_utils.save_corpus(dataset, 'logit-dataset.csv')


def build_dataset(dataset, pr_reader):
    row_num = 0  # skip header
    for row in pr_reader:
        if row_num != 0:
            url, owner, commenter, decision, submission_date, last_comment = [x.strip() for x in row.strip().split(';', 6)]
            _, month, year = [x.strip() for x in submission_date.strip().split(' ', 3)]
            score = retrieve_trust_score(commenter, month, year)
            if decision == 'merged':
                successful = 'TRUE'
            else:
                successful = 'FALSE'
            _, pr_id = url.split('/pull/')
            r = (pr_id, successful, str(score).strip())
            #r = '{0};{1};{2}'.format(pr_id, successful, score).strip()
            dataset.append(r)
        row_num += 1


if __name__ == "__main__":
    main()
