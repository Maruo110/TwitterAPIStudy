# -*- coding: utf-8 -*-

def getSentiment(analyze_text):

    from google.cloud import language
    from google.cloud.language import enums
    from google.cloud.language import types

    client = language.LanguageServiceClient()

    document = types.Document(content=analyze_text, type=enums.Document.Type.PLAIN_TEXT)

    sentiment = client.analyze_sentiment(document=document).document_sentiment

    #print('Text: {}'.format(text))
    #print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

    return sentiment

"""
if __name__ == '__main__':
    text = '明日雨降るみたいね。'
    getSentiment(text)
"""
