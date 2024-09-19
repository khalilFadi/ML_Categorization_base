from transformers import pipeline
import pandas as pd 
sentiment_analyzer_distilbert = pipeline("sentiment-analysis")

#input: full file find columns with text and apply sentiment analysis then output the full file plus the sentiment 
def SentimentAnalysis(df, question = '', numerical_output=True):
    col = df['text']
    outputCol = []
    for i in col:
        if isinstance(i, str) and len(i) < 510:
            i = question + i
            outputCol.append(sentiment_analyzer_distilbert(i)[0]['label'])
        else:
            outputCol.append('NEUTRAL')
    #change to numbers 
    if numerical_output:
        outputCol = list(map(lambda x: 1 if x == 'POSITIVE' else (-1 if x == 'NEGATIVE' else 0), outputCol))
    df['sent'] = outputCol
    return df

pdf = pd.read_csv('SympathyAnalysis\Q16_preds.csv')
print(SentimentAnalysis(pdf))
# print(sentiment_analyzer_distilbert("Im angry ")[0]['label'])