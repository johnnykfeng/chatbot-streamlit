from openai import OpenAI
import streamlit as st

def api_key_check(openai_api_key):
    client = OpenAI(api_key=openai_api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "say hello"}],
        )
        if response.choices[0].message.content:
            return True
    except Exception as e:
        return False
    
    