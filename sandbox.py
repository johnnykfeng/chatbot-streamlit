import toml
from openai import OpenAI

with open('.streamlit/secrets.toml') as f:
    secrets

client = OpenAI(api_key=secrets['OPENAI_API_KEY'])

# ic(client.models.list())
for model in client.models.list():
    print(model.id)