import transformers
import pandas as pd 
import numpy as np 
import math
from collections import Counter
from faker import Faker
# Create a list of personas and some data and information about them 
# I will use factor analysis to be able to do that
# 1. get a list of the main topics 
# 2. get the average age of for each topic
# 3. get the median gender 
# 4. get the median state 

# Here I am using a locally saved FactorAnalysis version 0.0.1
from zhipuai import ZhipuAI

import Factoranalysis

from huggingface_hub import login
login(token="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")

# Use a pipeline as a high-level helper# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text2text-generation", model="google/flan-t5-large")

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

def generate_persona(persona_text):

    client = ZhipuAI(api_key="63da1283335c112c90d32c0aeaf095b6.pXJbNVY0dQk5NgkR") # Please fill in your own APIKey

    tools = [
        {
            "type": "function",
            "function": {
                "name": "query_train_info",
                "description": "Query train schedules based on user-provided information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "departure": {
                            "type": "string",
                            "description": "Departure city or station",
                        },
                        "destination": {
                            "type": "string",
                            "description": "Destination city or station",
                        },
                        "date": {
                            "type": "string",
                            "description": "Date of the train to be queried",
                        },
                    },
                    "required": ["departure", "destination", "date"],
                },
            }
        }
    ]

    messages = [
        {
            "role": "user",
            "content": f"{persona_text}"
        }
    ]
    response = client.chat.completions.create(
        model="glm-4-plus", # Please fill in the model name you want to call
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    return response.choices[0].message.content

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
        Persona['Title'] = Topics['Name'][i]
        Persona['age'] = np.random.normal(np.mean(ages_per_topic[i]), np.std(ages_per_topic[i]))
        total_collected_genders = math.fsum(gender_per_topic[i].values())
        for n in gender_per_topic[i]:
            gender_per_topic[i][n] /= total_collected_genders
        Persona['gender'] = np.random.choice(list(gender_per_topic[i].keys()), p = list(gender_per_topic[i].values()))
        state_counts = Counter(state_per_topic[i])
        total_counts = sum(state_counts.values())
        state_probabilities = {state: count / total_counts for state, count in state_counts.items()}
        Persona['state'] = np.random.choice(list(state_probabilities.keys()), p=list(state_probabilities.values()))
        # Adding a name to the Personas 
        Persona['name'] = generate_name(Persona['Title'], Persona['age'], Persona['gender'], Persona['state'])
        #Getting the responses that will be used for the personality
        filtered_df = input_file[input_file['Topic'] == i]
        #TODO: Change text to another column 
        Persona['responses'] = [u if not isinstance(u, float) else '' for u in filtered_df.sample(n=responses_used, replace=True)['text']]
        # Adding some more background info using the input file 
        Persona['personality']  = generate_persona('I want you to create a personality based on these traits and responses from a survey give, be creative: '.join([str(Persona[i]) for i in Persona]))
        # grouping that info and creating a personality
        Persona['Chat_history'] = []
        print(f"Personality: {Persona['personality']}")

        Personas.append(Persona)
    return Personas

def chat_with_persona(Persona, question, backgroud = ''):
    
    inputCase = 'this is a persona, I want to chat with it, for all future questions answer as if your this persona, all questions will start with (Q: ), make sure answers are not too long answer as if your a human having a normal chat, this is a persona that will be used in a focus group:'.join(Persona['personality']) + "\n\n Q: " + question
    
    generated_text = pipe(inputCase)
    return generated_text

def run_Persona_Creation(input_file: pd.DataFrame, number_of_personas=5):
    topics, df = Factoranalysis.run_Factor_analysis(input_file, number_of_topics=number_of_personas, topic_size=2, return_topic_info=True)
    Personas = find_Personas(df, topics, number_of_personas)
    pd.DataFrame(Personas).to_csv('Personas.csv', sep='%')
    return Personas

# run_Persona_Creation(pd.read_csv('recomendationFilInput.csv'))