import streamlit as st
import pandas as pd
import Factoranalysis
import matplotlib.pyplot as plt
import numpy as np

# Sample data
df = pd.DataFrame()

st.title('Factor Analysis')
st.caption('A factor analysis program is a statistical tool that examines relationships between multiple variables to uncover underlying patterns or structures within a dataset, grouping them into a smaller number of latent factors. This technique helps researchers reduce data complexity, identify hidden constructs, and explore interrelationships among observed variables, making it valuable in fields such as psychology, social sciences, and market research.')

# df = pd.DataFrame(data)
uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
# Process the file if it has been uploaded

topic_Size = st.number_input('Enter a value for topic Size', value=2)
number_of_topics = st.number_input('Enter a max number of topics', value=5)
info = None
if uploaded_file is not None:
    # Read the file into a DataFrame
    df = pd.read_csv(uploaded_file)
    cols = df.columns

    option = st.selectbox(
        "Which column would you like to analyze?",
        (cols),
        placeholder="Select column name method...",
    )
    if info is None:
        df, info = Factoranalysis.run_Factor_analysis(df, topic_size=topic_Size,col_name=option, number_of_topics=number_of_topics, save_file=False, return_topic_info=True)
    
    # Display the table
    st.write(df)
    titles = df['Name']
    title = st.selectbox(
        "which title would you like to analyze", 
        (titles),
        placeholder="Select Title"
    )
    #Analyze title:\
    if info is not None:
       
        
        st.write("Title Analysis")
        #show age information
        #TODO: change to work with other datasets
        age_info = Factoranalysis.get_age_info(info, 'Q21', df)
        # Create a plot
        plt.figure(figsize=(10, 6))

        # Plot each list of ages
        for i, ages in enumerate(age_info):
            ages = age_info[ages]
            mean = np.mean(ages)
            std_dev = np.std(ages)
            # Ensure std_dev is not zero
            if std_dev > 0:
                x = np.linspace(mean - 3*std_dev, mean + 3*std_dev, 100)
                pdf = (1/(std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev)**2)
                plt.plot(x, pdf, label=f'{df['Name'][i]}')
            else:
                plt.axvline(mean, color='red', linestyle='--', label=f'Title {i+1} Mean')
        # Customize the plot
        plt.title('Age Distribution for Different Titles')
        plt.xlabel('Age')
        plt.ylabel('Probability Density')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

        #State 
        state_info = Factoranalysis.get_state_info(info, 'Q19', df)
        
        states = {x: 0 for x in set(state_info[0])}
        for i in state_info[0]:
            states[i] += 1
        states = dict(sorted(states.items(), key=lambda item: item[1]))
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xticklabels([f'{i}' for i in states], rotation=45)
        ax.bar(list(states.keys()), list(states.values()))
        plt.tight_layout()
        plt.title('State Distribution of first title')
        st.pyplot(fig)

        #Gender 
        gender_info = Factoranalysis.get_gender_info(info, 'Q17', df)
        print(gender_info)
        
        # print(state_info)
    

