import streamlit as st
import pandas as pd
import sympathyanalyser
# Sample data
df = pd.DataFrame()
# df = pd.DataFrame(data)
uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
# Process the file if it has been uploaded

topic_Size = st.number_input('Enter a value for topic Size', value=2)
number_of_topics = st.number_input('Enter a max number of topics', value=5)
present_as_numbers = st.checkbox('Show as numbers ', value= False)
# use stream lit to get a boolen value?
if uploaded_file is not None:
    # Read the file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Display the DataFrame
    st.write("Uploaded DataFrame:")
    st.dataframe(df)
    df = sympathyanalyser.SentimentAnalysis(df)
# User input


# Display the table
st.write(df)
