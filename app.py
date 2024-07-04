from openai import OpenAI
import streamlit as st
from utils import api_key_check, get_model_cost, calc_total_cost
import pandas as pd

with st.expander("Show cost table"):
    # file_path = r"https://github.com/johnnykfeng/chatbot-streamlit/blob/main/assets/openai_models.csv"
    file_path = r"./assets/openai_models.csv"
    prices = pd.read_csv(file_path)
    st.write(prices)

if "valid_key" not in st.session_state:
    st.session_state["valid_key"] = False

if "last_cost" not in st.session_state:
    st.session_state["last_cost"] = [0]

if "running_cost" not in st.session_state:
    st.session_state["running_cost"] = 0
    
if "prompt_tokens" not in st.session_state:
    st.session_state["prompt_tokens"] = [0]

if "completion_tokens" not in st.session_state:
    st.session_state["completion_tokens"] = [0]

# Create a sidebar in the Streamlit app
with st.sidebar:
    st.subheader("Please enter either the OpenAI API key or the password.")

    # Add a text input field for the OpenAI API key
    openai_api_key = st.text_input(
        "OpenAI API Key", key="chatbot_api_key", type="password", value=None
    )

    if openai_api_key is not None:
        if api_key_check(openai_api_key):
            st.success("API key is valid")
            st.session_state["valid_key"] = True
        else:
            st.session_state["valid_key"] = False
            st.error("API key is invalid")

    st.write(
        "[How to get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    )

    password = st.text_input("Password", value=None, type="password")
    if password is not None and password == st.secrets["PASSWORD"]:
        openai_api_key = st.secrets["OPENAI_API_KEY"]
        st.session_state["valid_key"] = True
        st.success("Correct password")
    elif password is not None and password != st.secrets["PASSWORD"]:
        st.session_state["valid_key"] = False
        st.error("Incorrect password")

    # radio button for selecting the model
    model_choice = st.radio(
        "Select a model", ["gpt-3.5-turbo", "gpt-4o", "gpt-4-turbo"], index=0
    )
    input_cost, output_cost = get_model_cost(model_choice, prices)
    st.write(f"**Input cost:** {input_cost:.5f} ¢/token")
    st.write(f"**Output cost:** {output_cost:.5f} ¢/token")

    stream_choice = st.checkbox("Stream Response", value=False)

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

# Check if the "messages" key exists in the session state
if "messages" not in st.session_state:
    # If not, initialize it with a default message from the assistant
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

if not openai_api_key and not st.session_state["valid_key"]:
    # Display an info message if the API key is missing
    st.info("Please add your OpenAI API key to continue.")
    st.stop()
else:
    # Iterate over each message in the session state
    for i, msg in enumerate(st.session_state.messages):
        # Display the message in the chat interface
        st.chat_message(msg["role"]).write(msg["content"])
        if msg["role"] == "assistant":
            j = int(i/2)
            st.caption(
                f" Prompt tokens: {st.session_state['prompt_tokens'][j]}" + 
                f" | Completion tokens: {st.session_state['completion_tokens'][j]}" + 
                f" | Answer cost: {st.session_state['last_cost'][j]:.4f} ¢"
            )

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
        response = client.chat.completions.create(
            model=model_choice,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=stream_choice,
        )

        if stream_choice:
            msg = st.write_stream(response)
        else:
            msg = response.choices[0].message.content
            st.markdown(msg)
            
            st.session_state["prompt_tokens"].append(response.usage.prompt_tokens)
            st.session_state["completion_tokens"].append(response.usage.completion_tokens)
            st.session_state["last_cost"].append(calc_total_cost(
                response.usage.prompt_tokens,
                response.usage.completion_tokens,
                input_cost,
                output_cost))

            st.caption(
                f"Prompt tokens: {st.session_state['prompt_tokens'][-1]}" + 
                f" | Completion tokens: {st.session_state['completion_tokens'][-1]}" +
                f" | Answer cost: {st.session_state['last_cost'][-1]:.4f} ¢" )
            st.session_state["running_cost"] += st.session_state["last_cost"][-1]
            st.caption(
                f"Running Cost: {st.session_state['running_cost']:.4f} ¢")

    st.session_state.messages.append({"role": "assistant", "content": msg})
