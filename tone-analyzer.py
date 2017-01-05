import csv
import os
import glob
import time

from utils import file_utils, db_utils
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
    username='d6739ba1-970e-4b5a-9e38-f037fde2b299',
    password='z7pTaPSvgx8T',
    version='2016-02-11')


def main():
    committers = file_utils.load_emails('./groovy-coreteam.csv')
    cnx = db_utils.connect()
    base_dir = './emails'
    print ('building email corpus')
    #db_utils.build_corpus(cnx, committers, base_dir)
    db_utils.disconnect(cnx)

    results_dir = './results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    print ('analyzing tone')
    for dev in committers:
        file_name = '{0}/{1}.csv'.format(results_dir, dev['id'])
        with open(file_name, 'wb') as results:
            wr = csv.writer(results, delimiter=';')
            header = ('year-month', 'agreeableness')
            # social_tones = {'Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Emotional Range'}
            wr.writerow(header)

            lookup = '{0}/{1}/*.txt'.format(base_dir, dev['id'])
            for email in glob.glob(lookup):
                y_m = email.split('.', 1)
                with open(email, 'rb') as f:
                    content = f.read()
                    js = tone_analyze(content)
                    agreeableness_score = js['document_tone']['tone_categories'][0]['tones'][3]['score']
                    row = (y_m, agreeableness_score)
                    wr.writerow(row)
                    # Wait for a bit
                    time.sleep(.300)

        results.close()


def tone_analyze(text, tones='social', sentences=False):
    js = tone_analyzer.tone(text, tones, sentences)
    return js


if __name__ == "__main__":
    main()
