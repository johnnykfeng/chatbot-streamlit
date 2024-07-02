from openai import OpenAI
import streamlit as st
import toml
from utils import api_key_check

with open('.streamlit/secrets.toml') as f:
    secrets = toml.load(f)

# if "key_input_disabled" not in st.session_state:
#     st.session_state["key_input_disabled"] = False

# if "password_input_disabled" not in st.session_state:
#     st.session_state["password_input_disabled"] = False

if "valid_key" not in st.session_state:
    st.session_state["valid_key"] = False

# Create a sidebar in the Streamlit app
with st.sidebar:
    st.subheader("Please enter either the OpenAI API key or the password.")

    # Add a text input field for the OpenAI API key
    openai_api_key = st.text_input(
        "OpenAI API Key", key="chatbot_api_key", type="password",
        value=None)

    if openai_api_key is not None:
        if api_key_check(openai_api_key):
            st.success("API key is valid")
            st.session_state["valid_key"] = True
        else:
            st.session_state["valid_key"] = False
            st.error("API key is invalid")

    st.write(
    "[How to get an OpenAI API key](https://platform.openai.com/account/api-keys)")

    password = st.text_input("Password", value = None,
                             type="password")
    if password is not None and password == secrets['PASSWORD']:
        openai_api_key = secrets['OPENAI_API_KEY']
        st.session_state["valid_key"] = True
        st.success("Correct password")
    elif password is not None and password != secrets['PASSWORD']:
        st.session_state["valid_key"] = False
        st.error("Incorrect password")

    # radio button for selecting the model
    model_choice = st.radio(
        "Select a model",
        ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4", "gpt-4o"],
        index=0
    )
    
    stream_choice = st.checkbox("Stream Response", value=True)
    
st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

# Check if the "messages" key exists in the session state
if "messages" not in st.session_state:
    # If not, initialize it with a default message from the assistant
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}]

if not openai_api_key and not st.session_state["valid_key"]:
    # Display an info message if the API key is missing
    st.info("Please add your OpenAI API key to continue.")
    st.stop()
else:
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
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        output = client.chat.completions.create(
            model=model_choice,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=stream_choice,
        )
        if stream_choice:
            msg = st.write_stream(output)
        else:
            msg = output.choices[0].message.content
            st.markdown(msg)
            # st.chat_message("assistant").write(msg)
        
    st.session_state.messages.append({"role": "assistant", "content": msg})
