import json
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
    username='d6739ba1-970e-4b5a-9e38-f037fde2b299',
    password='z7pTaPSvgx8T',
    version='2016-02-11')
js = tone_analyzer.tone(text='I am very happy', tones='social', sentences=False)
print(json.dumps(js, indent=2))
