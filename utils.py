from openai import OpenAI
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


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


def get_model_cost(model_choice, prices):
    """Returns the input and output cost of the model in cent/token."""
    row = prices[prices["Model"] == model_choice]
    input_cost = float(row["Input Tokens ($/1M)"].values[0])/1e4  # cent/token
    output_cost = float(row["Output Tokens ($/1M)"].values[0])/1e4  # cent/token
    return input_cost, output_cost


def calc_total_cost(input_tokens, output_tokens, input_cost, output_cost):
    """Output is in cents."""
    return (input_tokens*input_cost + output_tokens*output_cost)


def plot_model_costs(prices_df):
        # Create a bar chart comparing input and output token costs
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Extract data for plotting
    models = prices_df['Model']
    input_costs = prices_df['Input Tokens ($/1M)']
    output_costs = prices_df['Output Tokens ($/1M)']
    
    # Set width of bars and positions of the bars
    bar_width = 0.35
    x = range(len(models))
    
    # Create bars
    ax.bar([i - bar_width/2 for i in x], input_costs, bar_width, label='Input Cost ($/1M tokens)', color='skyblue')
    ax.bar([i + bar_width/2 for i in x], output_costs, bar_width, label='Output Cost ($/1M tokens)', color='lightgreen')
    
    # Customize the plot
    ax.set_ylabel('Cost ($/1M tokens)')
    ax.set_title('OpenAI Model Pricing Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=45, ha='right')
    ax.legend()
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    return fig


if __name__ == "__main__":
    print(get_model_cost("gpt-3.5-turbo"))
