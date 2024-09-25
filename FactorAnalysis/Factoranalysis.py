import sys
from bertopic import BERTopic
import pandas as pd
import argparse
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#run the iterface.py to get an easier time using this 

#Input: csv filename
# -s size of each topic 
# -t number of topics 

#output:
# topic: topic number 
# Count: number of docs in this topic 
# Name: a possible name for teh topic
# Representation: main words found in this topic including stop words 
# Representitive_docs: examples of elements in this topic 
# this file will be saved in the same location as the file being studied 

 
# Make sure to download the stopwords and punkt data if you haven't already
# Download punkt if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
nltk.download('stopwords')

def main():
    # Check if any arguments were passed
    parser = argparse.ArgumentParser(description='Run BERTopic with specified parameters.')

    if len(sys.argv) > 1:
        # print("Arguments passed:", sys.argv[1:])
        parser.add_argument('input_file', type=str, help='Input CSV file with text data.')
        parser.add_argument('-s', '--topic_size', type=int, default=2, help='Number of topics to generate (default is 2).')
        parser.add_argument('-t', '--number_of_topics', type=int, default=5, help='Number of topics to generate (default is 5).')
    
    else:
        print("No arguments were passed.")
    args = parser.parse_args()
    topic_size = args.topic_size
    number_of_topics = args.number_of_topics
    input_file = sys.argv[1]
    run_Factor_analysis(input_file, topic_size, number_of_topics)\
    
def remove_stop_words(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    
    filtered_text = [word for word in word_tokens if word.lower() not in stop_words]
    return ' '.join(filtered_text)

def run_Factor_analysis(input_file, topic_size, number_of_topics, save_file = True, include_stop_words=False):  
    if isinstance(input_file, str): 
        output_file_name = f'{input_file[:-4]}_Factor_analysis.csv'
    else:
        output_file_name = 'Output_Factor_analysis.csv'
    if isinstance(input_file, pd.DataFrame):
        df = input_file
    else:
        df = pd.read_csv(input_file)
    docs = [i if not isinstance(i, float) else '' for i in df['text']]

    filtered_docs = [remove_stop_words(doc) for doc in docs]

    topic_model = BERTopic(min_topic_size=topic_size, nr_topics = number_of_topics, )
    # Fit the model on the documents
    topics, probabilities = topic_model.fit_transform(filtered_docs)

    topic_info = topic_model.get_topic_info()
    # print(topic_info)
    output = pd.DataFrame(columns=['Topic', 'Count', 'Name', 'Representation', 'Representative_Docs'])
    #get the main sentences 
    for index, topic in topic_info.iterrows():
        if topic['Topic'] == -1:
            continue 
        new_row = topic[['Topic', 'Count', 'Name', 'Representation', 'Representative_Docs']]
        new_row['Representative_Docs'] = docs[index]  # Using original docs
        output.loc[len(output)] = new_row
    if save_file:
        output[:].to_csv(output_file_name)
        print(f"Output file name: {output_file_name}")
    return output

  
if __name__ == "__main__":
    main()
