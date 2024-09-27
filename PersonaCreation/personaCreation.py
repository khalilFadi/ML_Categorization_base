import transformers
import pandas as pd 

# Create a list of personas and some data and information about them 
# I will use factor analysis to be able to do that
# 1. get a list of the main topics 
# 2. get the average age of for each topic
# 3. get the median gender 
# 4. get the median state 

# Here I am using a locally saved FactorAnalysis version 0.0.1
import Factoranalysis

def find_Personas(input_file: pd.DataFrame, Topics: pd.DataFrame, number_of_personas) -> list:
    #input_file includes an extra column connecting each row to a topic 
    #Each persona includes:
        # topic it is representing[0], age[1], gender[2], and state[3]
    Personas = []
    #printing out information about the average age of each topic 
    #TODO: Make this work for different column names 
    Topics_average_ages = []
    for current_topic in Topics:
        total_age_for_this_topic = 0
        for index, row in input_file.iterrows():
            if row['Topic'] == current_topic['Topic']:
                total_age_for_this_topic += int(row['Q21'])
        Topics_average_ages.append(total_age_for_this_topic/current_topic['Count'])
    print(Topics_average_ages)
    pass

def run_Persona_Creation(input_file: pd.DataFrame, number_of_personas=5):
    topics, df = Factoranalysis.run_Factor_analysis(input_file, number_of_topics=number_of_personas, topic_size=2, return_topic=False)
    find_Personas(df, topics, number_of_personas)

run_Persona_Creation(pd.read_csv('recomendationFilInput.csv'))