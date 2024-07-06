import boto3
from langchain_community.vectorstores.faiss import FAISS

from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.prompts import PromptTemplate

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.text import TextLoader

from langchain_community.llms.bedrock import Bedrock

from langchain_community.embeddings.bedrock import BedrockEmbeddings
from decouple import config


ACCESS_KEY_ID = config("ACCESS_KEY_ID")
SECRET_KEY = config("SECRET_KEY")
AWS_REGION = config("REGION_NAME")

LLM_MODEL_ID = config("LLM_MODEL_ID")
EMBEDDING_MODEL = config("EMBEDDING_MODEL")

bedrock = boto3.client("bedrock-runtime",
                       aws_access_key_id=ACCESS_KEY_ID,
                       aws_secret_access_key=SECRET_KEY,
                       region_name="ca-central-1")


def get_embedding():
    titan_embeddings = BedrockEmbeddings(model_id=EMBEDDING_MODEL,
                                         client=bedrock)
    return titan_embeddings


def data_ingestion():
    loader = TextLoader("/Users/hasnat/Desktop/codemium/data/data.txt")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                   chunk_overlap=250)
    docs = text_splitter.split_documents(documents)
    return docs


def setup_vector_store(documents):
    vector_store = FAISS.from_documents(
        documents,
        get_embedding(),
    )
    vector_store.save_local("faiss_index")


def load_llm():
    llm = Bedrock(model_id=LLM_MODEL_ID, client=bedrock, model_kwargs={"max_tokens": 512})
    return llm


prompt_template = """Human: 
    You are a conversational assistant designed to help answer questions from an developer. 
    You should reply to the human's question using the information provided below. Include all relevant information but keep your answers detailed. Only answer the question. Do not say things like "according to the training or handbook or according to the information provided...".
    <Information>
    {context}
    </Information>
    {question}

    Assistant:"""

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])


def get_response(llm, vector_store, query):
    retrieval_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": 3}
        ),
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True,
    )
    response = retrieval_qa.invoke(query)
    return response['result']
