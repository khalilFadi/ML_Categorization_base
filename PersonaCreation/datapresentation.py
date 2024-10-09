import streamlit as st
import pandas as pd
import json

from personaCreation import chat_with_persona as chat

def display_persona_popup(persona):
    st.markdown(f"## {persona['name']}")
    st.write(f"**Age:** {persona['age']}")
    st.write(f"**Gender:** {persona['gender']}")
    st.write(f"**State:** {persona['state']}")
    st.markdown(persona['personality'])

def main():
    st.title("Persona Creation Program")

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # File upload section
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file, sep="%")

        # Number of personas to display
        num_personas = st.number_input("Number of personas to display:", min_value=1, max_value=100, value=5)

        # Display personas
        st.subheader("Personas:")
        personas = df.head(num_personas).to_dict('records')
        for persona in personas:
            if st.button(persona['name']):
                st.session_state.selected_persona = persona

        # Display selected persona
        if 'selected_persona' in st.session_state:
            with st.expander(f"Selected Persona: {st.session_state.selected_persona['name']}", expanded=True):
                display_persona_popup(st.session_state.selected_persona)

        # Chat-like model
        st.subheader("Chat:")
        chat_placeholder = st.empty()

        # User input
        user_input = st.text_input("Type your message:")
        if st.button("Send"):
            response = chat(st.session_state.selected_persona, user_input)
            print("Response: ", response)
            st.session_state.chat_history.append(f"\nUser: {user_input}\n")
            # Here you can add logic to process the user input and generate a response
            st.session_state.chat_history.append(f"{st.session_state.selected_persona['name']}: {response}'\n")

        # Display chat history
        chat_content = "\n".join(st.session_state.chat_history)
        chat_placeholder.text_area("Chat History:", value=chat_content, height=300)

if __name__ == "__main__":
    main()