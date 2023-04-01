import os
import json
from typing import Any, Dict
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain import ConversationChain, OpenAI, VectorDBQA
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate


load_dotenv()  # Required to load .env


openai_api_key = os.getenv("OPENAI_API_KEY")


if openai_api_key is not None:
    os.environ["OPENAI_API_KEY"] = openai_api_key

llm = ChatOpenAI(max_retries=3, temperature=0,
                 model_name="gpt-3.5-turbo")

vectorstore_retrievers: Dict[str, Any] = {
    "admission": None,
    "denison_edu": None,
    "denisonian": None,
}


def get_vectorstore_retriever(input: str, vectorstore_name: str):
    if (vectorstore_retrievers[vectorstore_name] is None):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=3000, chunk_overlap=200)

        texts = text_splitter.split_text(json.dumps(input))

        embeddings = OpenAIEmbeddings(max_retries=2)
        vectorstore = FAISS.from_texts(texts, embeddings)

        vectorstore_retrievers[vectorstore_name] = vectorstore.as_retriever()
    return


def get_openai_chat_response(text_context: str, user_reply: str, set_the_tone: str, vectorstore_category):
    get_vectorstore_retriever(text_context, vectorstore_category)

    qa = RetrievalQA.from_llm(
        llm=llm, retriever=vectorstore_retrievers[vectorstore_category])

    return qa.run(set_the_tone + user_reply)


def get_openai_article_recommendation(text_context, user_profile: str, set_the_tone: str, vectorstore_category):
    get_vectorstore_retriever(text_context, vectorstore_category)

    qa = RetrievalQA.from_llm(
        llm=llm, retriever=vectorstore_retrievers[vectorstore_category])

    return qa.run(set_the_tone + "relevant to " + user_profile)
