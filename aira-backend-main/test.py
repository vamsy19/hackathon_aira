import os

os.environ["OPENAI_API_VERSION"] = "2024-05-13"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://iris.openai.azure.com/"
os.environ["AZURE_OPENAI_API_KEY"] = "d00308b7327547ff9caa2c64892468d5"


# Import Azure OpenAI
from langchain_openai import AzureOpenAI

llm = AzureOpenAI(
    deployment_name="iris",
)

# Run the LLM
llm.invoke("Tell me a joke")
