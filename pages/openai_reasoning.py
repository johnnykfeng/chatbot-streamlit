import streamlit as st
from openai import OpenAI

st.title("OpenAI Reasoning Models")
openai_api_key = st.secrets["OPENAI_API_KEY"]

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "What can I help you with?"}]
    
if "last_response" not in st.session_state:
    st.session_state["last_response"] = None

if "usage" not in st.session_state:
    st.session_state["usage"] = None

model_choice = st.radio("Select model:", ["o1-mini", "o1-preview", "o3-mini-2025-01-31"], index=0)
reasoning_effort = st.radio("Select reasoning effort:", ["low", "medium", "high"], index=1)
stream_choice = st.checkbox("Stream response", value=False)

client = OpenAI(api_key=openai_api_key)

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
if prompt := st.chat_input():
    # st.session_state.messages.append({"role": "user", "content": [{"type": "text", "text": prompt}]})
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if model_choice != "o3-mini-2025-01-31":
            response = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": "developer", "content": "You are a helpful assistant."},
                    *st.session_state.messages
                ],
                stream=stream_choice       
            )
        else:
            response = client.chat.completions.create(
                model=model_choice,
                reasoning_effort=reasoning_effort,
                messages=[
                    {"role": "developer", "content": "You are a helpful assistant."},
                    *st.session_state.messages
                ],
                stream=stream_choice       
            )
        
        if stream_choice:
            message = st.write_stream(response)
        else:
            message = response.choices[0].message.content
            st.markdown(message)
    
    st.session_state["last_response"] = response
    st.session_state["usage"] = response.usage
    st.session_state.messages.append({"role": "assistant", "content": message})

with st.sidebar:
    st.write("## Message History")
    st.write(st.session_state.messages)
    # st.write("## Last Response")
    # st.write(st.session_state["last_response"])
    st.write("## Usage")
    if st.session_state["usage"]:
        st.json({
            "prompt_tokens": st.session_state["usage"].prompt_tokens,
            "completion_tokens": st.session_state["usage"].completion_tokens,
            "total_tokens": st.session_state["usage"].total_tokens,
            "completion_tokens_details": st.session_state["usage"].completion_tokens_details
        })
    else:
        st.write("No usage data yet")


# Clear chat button
if st.button("Clear chat history"):
    st.session_state.messages = [
        {"role": "assistant", "content": "What can I help you with?"}
    ]
    st.rerun()

