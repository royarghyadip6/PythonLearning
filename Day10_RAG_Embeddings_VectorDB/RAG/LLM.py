from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding_model = AzureOpenAIEmbeddings(
    model="text-embedding-ada-002"

)