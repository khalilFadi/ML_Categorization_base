import streamlit as st
import pandas as pd
import Factoranalysis
# Sample data
df = pd.DataFrame()
# df = pd.DataFrame(data)
uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
# Process the file if it has been uploaded

topic_Size = st.number_input('Enter a value for topic Size', value=2)
number_of_topics = st.number_input('Enter a max number of topics', value=5)

if uploaded_file is not None:
    # Read the file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Display the DataFrame
    st.write("Uploaded DataFrame:")
    st.dataframe(df)
    df = Factoranalysis.run_Factor_analysis(df, topic_size=topic_Size, number_of_topics=number_of_topics, save_file=False)
# User input


# Display the table
st.write(df)