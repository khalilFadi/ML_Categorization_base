import transformers
import pandas as pd 
import numpy as np 
import math
from collections import Counter
from faker import Faker
from transformers import BartForConditionalGeneration, BartTokenizer
from openai import OpenAI

import os
import torch
# Create a list of personas and some data and information about them 
# I will use factor analysis to be able to do that
# 1. get a list of the main topics 
# 2. get the average age of for each topic
# 3. get the median gender 
# 4. get the median state 

# Here I am using a locally saved FactorAnalysis version 0.0.1
import Factoranalysis
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)
OpenAI.api_key = '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'

client = OpenAI()
def generate_name(title, age, gender, state):
    fake = Faker('en_US')
        
    # Set the seed based on the attributes to ensure consistency
    seed = hash(f"{title}{age}{gender}{state}")
    Faker.seed(seed)
    
    # Generate the name
    if gender.lower() == 'female':
        first_name = fake.first_name_female()
    elif gender.lower() == 'male':
        first_name = fake.first_name_male()
    else:
        first_name = fake.first_name()
    
    last_name = fake.last_name()
    
    full_name = f"{first_name} {last_name}"
    
    return full_name
from transformers import BertForSequenceClassification, BertTokenizer
import torch

def generate_personality(age, gender, state, responses):
    # Load pre-trained BERT model and tokenizer
    model_name = "Minej/bert-base-personality"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name)

    # Prepare input text
    input_text = f"age: {age}\ngender: {gender}\nstate: {state}\nresponses: {' '.join(responses)}"
    
    # Tokenize input
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512, padding=True)
    
    # Generate personality traits
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.sigmoid(logits)
    
    # Map probabilities to personality traits
    traits = ["Extroversion", "Neuroticism", "Agreeableness", "Conscientiousness", "Openness"]
    personality_scores = {trait: float(prob) for trait, prob in zip(traits, probabilities[0])}
    
    # Generate personality description
    description = generate_personality_paragraph(personality_scores, age, gender, state)
    
    return description

def find_Personas(input_file: pd.DataFrame, Topics: pd.DataFrame, number_of_personas, responses_used = 10) -> list:
    #input_file includes an extra column connecting each row to a topic 
    #Each persona includes:
        # topic it is representing[0], age[1], gender[2], and state[3]
    Personas = []
    #printing out information about the average age of each topic 
    #TODO: Make this work for different column names 
    ages_per_topic = Factoranalysis.get_age_info(input_file, 'Q21', Topics)
    gender_per_topic = Factoranalysis.get_gender_info(input_file, 'Q17', Topics)
    state_per_topic = Factoranalysis.get_state_info(input_file, 'Q19', Topics)
    #Creating the personas 
    for i in Topics['Topic']:
        Persona = {}
        Persona['Title'] = i
        Persona['age'] = np.random.normal(np.mean(ages_per_topic[i]), np.std(ages_per_topic[i]))
        total_collected_genders = math.fsum(gender_per_topic[i].values())
        for n in gender_per_topic[i]:
            gender_per_topic[i][n] /= total_collected_genders
        Persona['gender'] = np.random.choice(list(gender_per_topic[i].keys()), p = list(gender_per_topic[i].values()))
        state_counts = Counter(state_per_topic[i])
        total_counts = sum(state_counts.values())
        state_probabilities = {state: count / total_counts for state, count in state_counts.items()}
        Persona['state'] = np.random.choice(list(state_probabilities.keys()), p=list(state_probabilities.values()))
        Persona['name'] = generate_name(Persona['Title'], Persona['age'], Persona['gender'], Persona['state'])
        #Getting the responses that will be used for the personality
        filtered_df = input_file[input_file['Topic'] == i]
        #TODO: Change text to another column 
        Persona['responses'] = [u if not isinstance(u, float) else '' for u in filtered_df.sample(n=responses_used, replace=True)['text']]
        print(f"Personality: {generate_personality(Persona['age'], Persona['gender'], Persona['state'], Persona['responses'])}")

        Personas.append(Persona)
    # Adding a name to the Personas 
    # Adding some more background info using the input file 
    # grouping that info and creating a personality
    pass

def run_Persona_Creation(input_file: pd.DataFrame, number_of_personas=5):
    topics, df = Factoranalysis.run_Factor_analysis(input_file, number_of_topics=number_of_personas, topic_size=2, return_topic_info=True)
    find_Personas(df, topics, number_of_personas)

run_Persona_Creation(pd.read_csv('recomendationFilInput.csv'))