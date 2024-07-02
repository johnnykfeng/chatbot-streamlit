import toml
from openai import OpenAI

with open('.streamlit/secrets.toml') as f:
    secrets = toml.load(f)

client = OpenAI(api_key=secrets['OPENAI_API_KEY'])

for model in client.models.list():
    print(model.id)
    