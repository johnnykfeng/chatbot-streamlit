import streamlit as st
import anthropic

st.title("Anthropic 🤖")
st.caption("🚀 A Streamlit chatbot powered by Anthropic")

if "valid_key" not in st.session_state:
    st.session_state["valid_key"] = False

if "msg_history" not in st.session_state:
    st.session_state["msg_history"] = []

with st.sidebar:
    password = st.text_input("Password", value=None, type="password")
    if password is not None and password == st.secrets["PASSWORD"]:
        anthropic_api_key = st.secrets["ANTHROPIC_API_KEY"]
        st.session_state["valid_key"] = True
        st.success("Correct password")
    elif password is not None and password != st.secrets["PASSWORD"]:
        st.session_state["valid_key"] = False
        st.error("Incorrect password")

    model_choice = st.radio("Select model: ", ["claude-3-5-sonnet-20240620",
                                               "claude-2.1"], index=0)
if not st.session_state["valid_key"]:
    st.info("Please add your Anthropic API key to continue.")
    st.stop()
else:
    for i, msg in enumerate(st.session_state.msg_history):
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not anthropic_api_key:
        st.info("Please add your Anthropic API key to continue.")
        st.stop()
    
    client = anthropic.Anthropic(api_key=anthropic_api_key)

    st.session_state.msg_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        
        # Remove the first assistant message if it exists, avoid error in the API
        if st.session_state.msg_history[0]["role"] == "assistant":
            st.session_state.msg_history.pop(0)
        
        response = client.messages.create(
            model=model_choice,
            max_tokens=1000,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.msg_history],
            stream=False)

        msg = response.content[0].text
        st.markdown(msg)

    st.session_state.msg_history.append({"role": "assistant", "content": msg})

with st.expander("Show message history"):
    st.write(st.session_state.msg_history)
