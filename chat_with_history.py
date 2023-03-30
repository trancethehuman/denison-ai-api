import os
import json
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain import ConversationChain, OpenAI, VectorDBQA, PromptTemplate
from langchain.memory import ConversationBufferMemory


load_dotenv()  # Required to load .env


openai_api_key = os.getenv("OPENAI_API_KEY")


if openai_api_key is not None:
    os.environ["OPENAI_API_KEY"] = openai_api_key


def get_openai_chat_response(knowledge, user_reply, set_the_tone_for_prompt):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200, chunk_overlap=300)

    texts = text_splitter.split_text(json.dumps(knowledge))

    embeddings = OpenAIEmbeddings(max_retries=2)
    vectorstore = FAISS.from_texts(texts, embeddings)

    llm = ChatOpenAI(max_retries=3, temperature=0.1,
                     model_name="gpt-3.5-turbo")

    template = set_the_tone_for_prompt + \
        "\n\nCurrent conversation:\n{history}\nHuman: {input}\nAI:"

    prompt = PromptTemplate(input_variables=['history', 'input'], output_parser=None, partial_variables={
    }, template=template)

    conversation = ConversationChain(
        llm=llm,
        memory=ConversationBufferMemory(),
        prompt=prompt,
    )

    return conversation.predict(input=user_reply)
