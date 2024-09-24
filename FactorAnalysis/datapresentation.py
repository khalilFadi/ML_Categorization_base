import streamlit as st
import pandas as pd
import io
import Factoranalysis
import plotly.express as px

# Sample data
df = pd.DataFrame()
# df = pd.DataFrame(data)
uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
# Process the file if it has been uploaded

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    processed_data = output.getvalue()
    return processed_data

topic_Size = st.number_input('Enter a value for topic Size', value=4)
number_of_topics = st.number_input('Enter a max number of topics', value=10)
question_text = st.text_input('Question text: *For better results please fill this out')
include_empty = st.checkbox('Include empty columns in analysis', value = False)
if uploaded_file is not None:
    # Read the file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Display the DataFrame
    df = Factoranalysis.run_Factor_analysis(df, question_text=question_text, include_empty=include_empty, topic_size=topic_Size, number_of_topics=number_of_topics, save_file=False)
    title = st.selectbox(
        "Which title would you like to look at?",
        (df['Name']),
        placeholder="Select title name...",
    )

    
    # Create the bar chart using Plotly
    fig = px.bar(df, x='Name', y='Count', title='Title Counts')

    # Customize the layout
    fig.update_layout(
        xaxis_title="Titles",
        yaxis_title="Count",
        xaxis_tickangle=-45  # Rotate x-axis labels for better readability
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)
    
    st.write("Updated DataFrame:")
    st.write(df)
    col1, col2, cl3, cl4 = st.columns(4)
    with col1:
        csv = convert_df_to_csv(df)  # Assuming you have this function defined
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='data.csv',
            mime='text/csv',
        )
    with col2:
        excel_file = to_excel(df)
        st.download_button(
            label="Download Excel file",
            data=excel_file,
            file_name="data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        # exl = 
    # if title is not None:

# User input


# Display the table