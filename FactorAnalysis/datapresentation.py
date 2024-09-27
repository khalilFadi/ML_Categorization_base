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

if uploaded_file is not None:
    # Read the file into a DataFrame
    df = pd.read_csv(uploaded_file)
    cols = df.columns

    option = st.selectbox(
        "Which column would you like to analyze?",
        (cols),
        placeholder="Select column name method...",
    )
    df, info = Factoranalysis.run_Factor_analysis(df, topic_size=topic_Size,col_name=option, number_of_topics=number_of_topics, save_file=False, return_topic_info=True)
    
    # Display the table
    st.write(df)
    
    #Analyze title:\
    st.write("Title Analysis")
    titles = df['Name']
    title = st.selectbox(
        "which title would you like to analyze", 
        (titles),
        placeholder="Select Title"
    )
    #show age information
    age_info = Factoranalysis.get_age_info(info, 'Q21', df)
    print(age_info)   
    # Create a plot
    plt.figure(figsize=(10, 6))

    # Plot each list of ages
    for i, ages in enumerate(age_info):
        ages = age_info[ages]
        print(f"AGES: {ages}" )
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

    

