from openai import OpenAI
import streamlit as st
from icecream import ic
from utils import *

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# for model in client.models.list():
#     print(model.id)

    
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris."},
    ],
    stream=True,
)

ic(response.__dict__)
ic(response.response.__dict__)

# ic(response.usage.total_tokens)


# input_price, output_price = get_model_cost("gpt-3.5-turbo")
# total_cost = calc_total_cost(response.usage.prompt_tokens, 
#                             response.usage.completion_tokens, 
#                             input_price, 
#                             output_price)

# ic(total_cost)

