import os
from time import strptime

from utils import file_utils


def __build_dataset(dataset, pr_reader, committer_ids):
    row_num = 0  # skip header
    for row in pr_reader:
        if row_num != 0:
            url, owner, committer_commenter, decision, submission_date, _ = [x.strip() for x in
                                                                             row.strip().split(';', 6)]
            if owner not in committer_ids:
                _, month, year = [x.strip() for x in submission_date.strip().split(' ', 3)]
                # score = __retrieve_trust_score_by_month(committer_commenter, month, year)
                score = __retrieve_trust_score_by_param(committer_commenter, 'overall')
                # score = __retrieve_trust_score_by_param(committer_commenter, 'average')
                # score = __retrieve_trust_score_by_param(committer_commenter, 'min')
                # score = __retrieve_trust_score_by_param(committer_commenter, 'max')
                if score != 'NA':
                    if decision == 'merged':
                        successful = 'TRUE'
                    else:
                        successful = 'FALSE'
                    _, pr_id = url.split('/pull/')
                    r = (pr_id, successful, str(score).strip())
                    # r = '{0};{1};{2}'.format(pr_id, successful, score).strip()
                    dataset.append(r)
        row_num += 1


def __retrieve_trust_score_by_param(dev, param="overall"):
    score = 'NA'
    filename = 'results{0}{1}.csv'.format(os.sep, dev)
    try:
        dev_reader, _file = file_utils.load_corpus(filename)
        for row in dev_reader:
            t, s = [x.strip() for x in row.split(';', 2)]
            if t == param:
                s = float(s)
                if s < 0.5:
                    score = 'LOW'
                else:
                    score = 'HIGH'
                break
        _file.close()
    except IOError:
        pass

    return score


def __retrieve_trust_score_by_month(dev, month, year):
    score = 'NA'
    filename = 'results{0}{1}.csv'.format(os.sep, dev)
    month_no = __as_number(month)
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


def __as_number(month):
    m = str(strptime(month, '%b').tm_mon)
    if len(m) == 1:
        m = '0' + m
    return m


def main():
    print("Building dataset for logistic regression")
    dataset = list()
    header = ('PRid', 'Successful', 'PropensityToTrust')
    dataset.append(header)

    # core team
    committers = file_utils.load_core_team_members(os.curdir + os.sep + 'groovy-coreteam.csv')
    committer_ids = list()
    for c in committers:
        committer_ids.append(c['id'])

    # open PR
    open_pr_reader, _file = file_utils.load_corpus('open-pullrequests.csv')
    __build_dataset(dataset, open_pr_reader, committer_ids)
    _file.close()

    # closed PR
    closed_pr_reader, _file = file_utils.load_corpus('closed-pullrequests.csv')
    __build_dataset(dataset, closed_pr_reader, committer_ids)
    _file.close()

    file_utils.save_corpus(dataset, 'logit-dataset.csv')


if __name__ == "__main__":
    main()
