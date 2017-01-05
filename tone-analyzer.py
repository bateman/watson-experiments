import csv
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
    db_utils.build_corpus(cnx, committers, base_dir)
    db_utils.disconnect(cnx)

    # corpus = file_utils.load_corpus('PR-corpus.csv', 'csv')

    # results = open('results.csv', 'wb')
    # wr = csv.writer(results, quoting=csv.QUOTE_ALL)
    # header = list()
    # header.append('Content')
    # writing_tones = {'Analytical', 'Confident', 'Tentative'}
    # for x in writing_tones:
    #     header.append(x)
    # social_tones = {'Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Emotional Range'}
    # for x in social_tones:
    #     header.append(x)
    # wr.writerow(header)
    #
    # scores = dict()
    # for content in corpus:
    #     js = tone_analyze(content[0])
    #     categories = js['document_tone']['tone_categories']
    #     for c in categories:
    #         # writing
    #         _scores = c['tones']
    #         for s in _scores:
    #             scores[s['tone_name']] = s['score']
    #     # write a row
    #     row = list()
    #     row.append(content[0])
    #     for x in writing_tones:
    #         row.append(scores[x])
    #     for x in social_tones:
    #         row.append(scores[x])
    #     wr.writerow(row)
    #     # Wait for a bit
    #     time.sleep(.500)
    #
    # results.close()


def tone_analyze(text, tones='social,language', sentences=False):
    js = tone_analyzer.tone(text, tones, sentences)
    return js


if __name__ == "__main__":
    main()
