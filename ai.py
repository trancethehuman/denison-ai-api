import os
import json
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


def get_openai_chat_response(knowledge, user_reply: str, set_the_tone: str):

    # Trying to put beginning prompt into querying vectorstore but couldn't
    context_prompt = PromptTemplate(
        template=set_the_tone, input_variables=[])
    chain_type_kwargs = {"prompt": context_prompt}

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200, chunk_overlap=300)

    texts = text_splitter.split_text(json.dumps(knowledge))

    embeddings = OpenAIEmbeddings(max_retries=2)
    vectorstore = FAISS.from_texts(texts, embeddings)
    retriever = vectorstore.as_retriever()

    qa = RetrievalQA.from_llm(
        llm=llm, retriever=retriever)

    return qa.run(set_the_tone + user_reply)


def get_openai_article_recommendation(knowledge, user_profile: str, set_the_tone: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1600, chunk_overlap=800)

    texts = text_splitter.split_text(json.dumps(knowledge))

    embeddings = OpenAIEmbeddings(max_retries=3)
    vectorstore = FAISS.from_texts(texts, embeddings)
    retriever = vectorstore.as_retriever()

    qa = RetrievalQA.from_llm(
        llm=llm, retriever=retriever)

    return qa.run(set_the_tone + "relevant to " + user_profile)
