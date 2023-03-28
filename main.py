import os
import json
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI, VectorDBQA

load_dotenv()  # Required to load .env

openai_api_key = os.getenv("OPENAI_API_KEY")
print(openai_api_key)
if openai_api_key is not None:
    os.environ["OPENAI_API_KEY"] = openai_api_key

with open('./test-data/news-denison-edu.json', 'r', encoding="utf8") as f:
    data = json.load(f)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800, chunk_overlap=300)
texts = text_splitter.split_text(json.dumps(data))

embeddings = OpenAIEmbeddings(max_retries=2)
vectorstore = FAISS.from_texts(texts, embeddings)

# qa = RetrievalQA.from_llm(llm=ChatOpenAI(
#     model_name="gpt-3.5-turbo"))

qa = VectorDBQA.from_chain_type(llm=ChatOpenAI(max_retries=2, temperature=0.1,
                                               model_name="gpt-3.5-turbo"), chain_type="stuff", vectorstore=vectorstore)

query = input("What would you like to know? ")
print(qa.run(query))
