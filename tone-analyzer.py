import collections
import csv
import glob
import os
import sys
import time

import numpy
from watson_developer_cloud import ToneAnalyzerV3

from utils import file_utils, db_utils

tone_analyzer = ToneAnalyzerV3(
    username='d6739ba1-970e-4b5a-9e38-f037fde2b299',
    password='z7pTaPSvgx8T',
    version='2016-02-11')


def main(argv):
    ml_name = argv[0]
    committers = file_utils.load_core_team_members(os.curdir + os.sep + '{0}-coreteam.csv'.format(ml_name))
    base_dir = os.curdir + os.sep + ml_name + os.sep + 'emails'
    if not os.path.exists(base_dir):
        cnx = db_utils.connect()
        print ('Retrieving developers\' emails from the db')
        db_utils.process_raw_emails(cnx, ml_name, committers, base_dir)
        db_utils.disconnect(cnx)

    results_dir = os.curdir + os.sep + ml_name + os.sep + 'results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    print ('Computing developers\' agreeableness scores from \'{0}\' (everything in \'{1}\' will be overwritten)'.
           format(base_dir, results_dir))
    for dev in committers:
        file_name = '{0}{1}{2}.csv'.format(results_dir, os.sep, dev['id'])
        with open(file_name, 'wb') as results:
            wr = csv.writer(results, delimiter=';')
            header = ('year_month', 'agreeableness')
            # social_tones = {'Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Emotional Range'}
            wr.writerow(header)

            rows = dict()
            lookup = '{0}{1}{2}{1}*.txt'.format(base_dir, os.sep, dev['id'])
            rows = dict()
            overall_content = list()
            scores = list()
            # compute agreeableness score from email bodies per month
            for email in glob.glob(lookup):
                y_m, _ = email.split('.txt', 1)
                _, y_m = y_m.split(base_dir + os.sep + dev['id'] + os.sep)
                y, m = y_m.split('-')
                if len(m) == 1:
                    y_m = '{0}-0{1}'.format(y, m)
                with open(email, 'rb') as f:
                    content = f.read()
                    js = tone_analyze(content)
                    agreeableness_score = js['document_tone']['tone_categories'][0]['tones'][3]['score']
                    scores.append(agreeableness_score)
                    rows[y_m] = agreeableness_score
                    # Wait for a bit
                    time.sleep(.150)
                    overall_content.append(content)

            # average agreeableness computed per month
            rows['average'] = numpy.mean(scores)
            # max agreeableness
            rows['max'] = numpy.max(scores)
            # max agreeableness
            rows['min'] = numpy.min(scores)
            # agreeableness computed on the overall email bodies
            overall_content = '\n'.join(overall_content)
            js = tone_analyze(overall_content)
            overall_agreeableness_score = js['document_tone']['tone_categories'][0]['tones'][3]['score']
            rows['overall'] = overall_agreeableness_score
            time.sleep(.150)

            rows = collections.OrderedDict(sorted(rows.items()))
            for key, value in rows.items():
                wr.writerow([key, value])

        results.close()


def tone_analyze(text, tones='social', sentences=False):
    js = tone_analyzer.tone(text, tones, sentences)
    return js


if __name__ == "__main__":
    main(sys.argv[1:])
