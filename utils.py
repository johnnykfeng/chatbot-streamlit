from openai import OpenAI
import streamlit as st
import pandas as pd


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


# prices = pd.read_csv(
#     r"assets\openai_models.csv")

def get_model_cost(model_choice, prices):
    """Returns the input and output cost of the model in cent/token."""
    row = prices[prices["Model"] == model_choice]
    input_cost = float(row["Input/1k Tokens"].values[0])/10  # cent/token
    output_cost = float(row["Output/1k Tokens"].values[0])/10  # cent/token
    return input_cost, output_cost


def calc_total_cost(input_tokens, output_tokens, input_cost, output_cost):
    """Output is in cents."""
    return (input_tokens*input_cost + output_tokens*output_cost)


if __name__ == "__main__":
    print(get_model_cost("gpt-3.5-turbo"))
