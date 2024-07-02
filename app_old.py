from openai import OpenAI
import streamlit as st

# Create a sidebar in the Streamlit app
with st.sidebar:    
    # Add a text input field for the OpenAI API key
    openai_api_key = st.text_input(
        "OpenAI API Key", key="chatbot_api_key", type="password")
    st.write(
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")

    # radio button for selecting the model
    model_choice = st.radio(
        "Select a model",
        ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4", "gpt-4o"],
        index=0
    )
st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

# Check if the "messages" key exists in the session state
if "messages" not in st.session_state:
    # If not, initialize it with a default message from the assistant
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}]

# Iterate over each message in the session state
for msg in st.session_state.messages:
    # Display the message in the chat interface
    st.chat_message(msg["role"]).write(msg["content"])

# Check if the user has entered a prompt in the chat input field
if prompt := st.chat_input():
    # Check if the OpenAI API key is provided
    if not openai_api_key:
        # Display an info message if the API key is missing
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Create an instance of the OpenAI client with the API key
    client = OpenAI(api_key=openai_api_key)

    # Append the user's prompt to the session state messages
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display the user's prompt in the chat interface
    st.chat_message("user").write(prompt)

    # Generate a response from the OpenAI model using the messages in the session state
    response = client.chat.completions.create(
        model=model_choice, messages=st.session_state.messages,
        stream=True)

    # Get the content of the first choice in the response
    msg = response.choices[0].message.content
    

    # Append the assistant's response to the session state messages
    st.session_state.messages.append({"role": "assistant", "content": msg})

    # Display the assistant's response in the chat interface
    st.chat_message("assistant").write(msg)
