import streamlit as st
import pandas as pd
import sympathyanalyser
import matplotlib.pyplot as plt

# Sample data
df = pd.DataFrame()
st.title('Sentiment Analysis')
st.caption('This program analyzes a column of comments from a CSV file, providing sentiment ratings (positive, neutral, or negative) for each comment and an overall summary. It offers insights into the emotional tone of the comments and allows for further exploration of the dataset.')
# df = pd.DataFrame(data)
uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
# Process the file if it has been uploaded
if uploaded_file is not None:
    # Read the file into a DataFrame
    df = pd.read_csv(uploaded_file)
    cols = df.columns
    st.write("#####")
    option = st.selectbox(
        "Which column would you like to analyze?",
        (cols),
        placeholder="Select column name method...",
    )
    st.write("#####")

    present_as_numbers = st.checkbox('Show as numbers ', value= False)
    st.caption('When selected, this option displays sentiment ratings as numerical values instead of text labels. Positive is 1, Neutral is 0, and Negative is -1.')
    
    ask_about_the_model = st.chat_input("ask about the dataset")

    question = st.text_input("Question: *Adding the question allows for more accurate results")
    st.caption('Enter a specific question here to analyze the text based on question phrasing')
    st.write("#####")
    
    
    if option is not None:
    # Display the DataFrame
    # st.write("Uploaded DataFrame:")
    # st.dataframe(df)
        df = sympathyanalyser.SentimentAnalysis(df, question=question, numerical_output=present_as_numbers, col_name=option)


    # pie chart of the data         
    # collecting piechart data
    amount_of_negative_comments = 0
    amount_of_positive_comments = 0 
    amount_of_neutral_comments = 0
    for i in df['sent']:
        if i == 'NEGATIVE' or i == -1:
            amount_of_negative_comments += 1
        elif i == "POSITIVE" or i == 1:
            amount_of_positive_comments += 1
        elif i == "NEUTRAL" or i == 0:
            amount_of_neutral_comments += 1
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [amount_of_positive_comments, amount_of_negative_comments, amount_of_neutral_comments]
    colors = ['gold', 'lightcoral', 'lightskyblue']
    explode = (0.1, 0, 0)  # explode the 1st slice

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, autopct='', labels=labels, colors=colors, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is a circle.
    for i, atext in enumerate(autotexts):
        atext.set_text(f'{(sizes[i]/len(df['sent']))*100:.2f}%')  # Customize label text
        atext.set_color('white')  # Set text color based on background
        atext.set_fontweight('bold')  # Make text bold

    # Display the pie chart in Streamlit
    st.title("Pie Chart Example")
    st.pyplot(fig)


    # Display the table
    st.write(df)
    st.caption('This table displays each comment with its analyzed sentiment and emotion. Double-click on a comment to view it in full. The sentiment column shows whether the comment is positive, neutral, or negative, while the emotion column provides a more specific emotional classification')
