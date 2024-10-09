# Persona Creation Tool



## Requirements

- Python 3.x
- pandas
- FactorAnalysis 0.0.2 (local file)
- zhipuai
- Torch

## Installation

1. Clone this repository or download the files.
2. Navigate to the directory in your terminal.
3. Install the required packages:

        pip install -r requirements.txt 
4. Run the program:  

        streamlit run datapresentation.py

# Process
## Finding a Persona
Create a list of personas and some data and information about them 
I will use factor analysis to be able to do that
1. get a list of the main topics 
2. get the average age of for each topic
3. get the median gender 
4. get the median state  

the peronas each include:
- age, state, gender and title it is derived from 
- name generated based on previous data 
- Personality created using glm-4-plus 
