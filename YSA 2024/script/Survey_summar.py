# Description of Package
# This is a sentiment analysis pipeline that combines the outputs of a pre-trained Roberta model and a pre-trained SafeTensors model. 
# A random Forest is used to predict when the Roberta Model will miss, so that the SafeTensors improves those results. 


print("Loading Packages and models")

import subprocess

# List of required packages
required_packages = ["nltk", "nrclex"]
# torch and transformers should have been previously installed

for package in required_packages:
    try:
        __import__(package)
        print(f"{package} is already installed.")
    except ImportError:
        print(f"{package} is not installed. Installing...")
        subprocess.check_call(["pip", "install", package])

#### Load Packages and models ####

import sys
import pandas as pd
import numpy as np

from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

from joblib import load
# rf_model = load("will_roberta_miss2_rebuilt.joblib")

# FOR will_roberta_miss4.joblib MODEL
    # from sklearn.linear_model import LogisticRegression
    # from sklearn.ensemble import RandomForestClassifier
    # base_learners = [
    #     ('lr', LogisticRegression(random_state=42)),
    #     ('rf', RandomForestClassifier(random_state=42))
    # ]
    # # Load base learners (assuming you have the original list with classifier names) 
    # for i, (clf_name, _) in enumerate(base_learners):  
    #     filename = f'base_learner_{clf_name}.joblib'
    #     base_learners[i] = (clf_name, load(filename))  # Modify the existing base_learners list

from transformers import pipeline
sentiment_analyzer_distilbert = pipeline("sentiment-analysis")

import string
import nltk
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nrclex import NRCLex

#### Functions ####

def get_sentiment_roberta(text):
    try:
        # Try analyzing sentiment on the entire text
        if pd.isna(text) or text == "":
            print("It was an NA")
            sentiment_label = {
                'negative': 0,
                'neutral': 0,
                'positive': 0
            }
            max_sentiment = "neutral"
            return max_sentiment, sentiment_label
        
        encoded_text = tokenizer(text, return_tensors='pt')
        output = model(**encoded_text)
        scores = output.logits[0].detach().numpy()
        scores = softmax(scores)

        sentiment_label = {
            'negative': scores[0],
            'neutral': scores[1],
            'positive': scores[2]
        }
        
        max_sentiment = max(sentiment_label, key=sentiment_label.get)
        return max_sentiment, sentiment_label
    
    except Exception as e:
        # return negative
        print("Too long, split and cacluclate")
        sentences = text.split('.')
        pos = 0
        neg = 0
        sentence_scores = []
        
        for sentence in sentences:
            
            encoded_text = tokenizer(sentence, return_tensors='pt')
            output = model(**encoded_text)
            scores = output.logits[0].detach().numpy()
            scores = softmax(scores)

            sentiment_label = {
                'negative': scores[0],
                'neutral': scores[1],
                'positive': scores[2]
            }
            sentence_scores.append(sentiment_label)
            
            max_sentiment = max(sentiment_label, key=sentiment_label.get)

            if max_sentiment == 'positive':
                pos += 1
            else:
                neg += 1
        mean_dict = {
            key: np.mean([sentence[key] for sentence in sentence_scores])
            for key in ['negative', 'neutral', 'positive']
        }
        if neg >= pos:
            return 'negative', mean_dict
        return 'positive', mean_dict

def analyze_sentiment_distilbert(text):
    if text == '':
        return 'neutral'
    text = 'Why did you rate the session director the way you did?' + text
    try:
        # Try analyzing sentiment on the entire text
        if pd.isna(text) or text == "":
            max_sentiment = "neutral"
            return max_sentiment
        result = sentiment_analyzer_distilbert(text)
        return result[0]['label'].lower()
    except Exception as e:
        sentences = text.split('.')
        pos = 0
        neg = 0
        for sentence in sentences:
            result = sentiment_analyzer_distilbert(sentence)
            result = result[0]['label'].lower()
            if result == 'positive':
                pos += 1
            else:
                neg += 1
        if neg >= pos:
            return 'negative'   
        return 'positive'

def roberta_plus_distilbert(row):
    #delete when the model is fixed
    return analyze_sentiment_distilbert(row['text']) # Apply distilbert function

    if row['rf_preds']:
        # Apply this function if 'caught_distilbert' is True
        return analyze_sentiment_distilbert(row['text']) # Apply distilbert function
    else:
        # Apply this function if 'caught_distilbert' is False
        return row['roberta']

def get_emotion_scores(text):
    emotions_with_scores = NRCLex(text).affect_frequencies
    emotions_without_negative_positive = {key: value for key, value in emotions_with_scores.items() if key not in ['negative', 'positive']}
    return dict(emotions_without_negative_positive)

def calculate_final_emotion(row):
    emotions = row['emotions']
    max_score = 0
    max_emotions = []
    if row['text'] == "":
        return 'neutral'
    if row['sent'] == "negative":
        for key, value in emotions.items():
            if key in ['anger', 'disgust', 'fear', 'sadness']:
                if value == max_score:
                    max_emotions.append(key)
                elif value > max_score:
                    max_score = value
                    max_emotions = [key]
        if len(max_emotions) == 1:
            return max_emotions[0]
        else:
            return "negative"
        
    elif row['sent'] == "positive":
        for key, value in emotions.items():
            if key in ['joy', 'trust']:
                if value == max_score:
                    max_emotions.append(key)
                elif value > max_score:
                    max_score = value
                    max_emotions = [key]
        if len(max_emotions) == 1:
            return max_emotions[0]
        else:
            return "positive"
        
    else:
        for key, value in emotions.items():
            if key in ['anticipation', 'surprise', 'anticip']:
                if value == max_score:
                    max_emotions.append(key)
                elif value > max_score:
                    max_score = value
                    max_emotions = [key]
        if len(max_emotions) == 1:
            return max_emotions[0]
        else:
            return "neutral"

#### Main ####
def main():
    # Load Data
    if len(sys.argv) < 2:
        print("Not enough command-line arguments provided.")
        return
    file_path = sys.argv[1]
    print("Loading file")
    df = pd.read_csv(file_path, encoding='latin1') # Change to read from input
    df.fillna({'text': ''}, inplace=True) # Fill NA with blank text

    # Run Roberta model on text
    print("Running roberta model")
    df[['roberta', 'roberta_scores']] = df['text'].apply(get_sentiment_roberta).apply(pd.Series)
    normalized_scores = pd.json_normalize(df['roberta_scores']) # Use pd.json_normalize to create separate columns for each key
    result_df = pd.concat([df, normalized_scores], axis=1) # Concatenate the original DataFrame with the new columns
    df = result_df.drop('roberta_scores', axis=1) # Drop the original 'roberta_scores' column if needed

    # Identify which columns Distilbert might do better
    print("Running random forest to identify rows that will need to use Distilbert")
    X_test = df[['negative', 'neutral', 'positive']]
    
    # For will_roberta_miss4 model
        # meta_X_new = np.zeros((X_test.shape[0], len(base_learners)))
        # for i, (_, clf) in enumerate(base_learners):
        #     predictions = clf.predict_proba(X_test)[:, 1]  
        #     meta_X_new[:, i] = predictions

    # df['rf_preds'] = rf_model.predict(X_test)

    # Create new column with roberta model and distilbert for the ones roberta might not get right
    print("Running Distilbert")
    df['sent'] = df.apply(roberta_plus_distilbert, axis=1)
    print("Fixed long text")

    # Tokenize, remove stopwords, and lemmatize
    print("Getting Emotions")
    all_feed = df.drop(['roberta', 'negative', 'neutral', 'positive'], axis=1)
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    def preprocess_text(text):
        tokens = word_tokenize(text)
        tokens = [lemmatizer.lemmatize(token) for token in tokens if token.lower() not in stop_words]
        return ' '.join(tokens)

    all_feed['processed_text'] = all_feed['text'].apply(preprocess_text) 
    
    # Get Top emotion
    all_feed['emotions'] = all_feed['processed_text'].apply(get_emotion_scores)
    all_feed['emotion'] = all_feed.apply(calculate_final_emotion, axis=1)

    #Remove unnecesary Columns
    final_df = all_feed.drop(columns=['emotions', 'processed_text'])

    final_df.to_csv('preds.csv', index=False)

    print("Done! New WW_preds.csv file has been created")

#### Run Main ####
if __name__ == "__main__":
    main()