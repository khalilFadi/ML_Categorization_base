import streamlit as st
import pandas as pd

def main():
    st.title("Persona Creation Program")

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # File upload section
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)

        # Number of personas to display
        num_personas = st.number_input("Persons will be after it:", min_value=1, max_value=100, value=5)

        # Display personas
        st.subheader("Personas:")
        personas = df['name'].tolist()[:num_personas]  # Assuming 'name' column exists
        for persona in personas:
            st.write(persona)

        # Chat-like model
        st.subheader("Chat:")
        chat_placeholder = st.empty()

        # User input
        user_input = st.text_input("Type your message:")
        if st.button("Send"):
            st.session_state.chat_history.append(f"User: {user_input}")
            # Here you can add logic to process the user input and generate a response
            st.session_state.chat_history.append(f"AI: This is a placeholder response to '{user_input}'\n")

        # Display chat history
        chat_content = "\n".join(st.session_state.chat_history)
        chat_placeholder.text_area("Chat History:", value=chat_content, height=300)

if __name__ == "__main__":
    main()