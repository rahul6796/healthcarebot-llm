import streamlit as st
from streamlit_chat import message
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# load the pdf:
loader = DirectoryLoader("data/",
                         glob='*.pdf',
                         loader_cls=PyPDFLoader)

documents = loader.load()

# split into the chunks:
text_spliter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    )
text_chunks = text_spliter.split_documents(documents=documents)

# create embedding:
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}
)

# vectorstore:

vector_store = FAISS.from_documents(
    text_chunks, embedding=embedding
)

# create llm:
llm = CTransformers(
    model = "patliu1001/llama-2-7b-chat.ggmlv3.q8_0.bin",
    model_type = "llama",
    config = {'max_new_tokens': 128, "temperature": 0.5},
)

memory = ConversationBufferMemory(memory_key="chat_history",
                                  return_messages=True)
chain  = ConversationalRetrievalChain.from_llm(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store(search_kwargs={"k:2"}),
    memory=memory

)


# create app:
st.title("HealthCare  ChatBot")

