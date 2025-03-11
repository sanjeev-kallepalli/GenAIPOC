from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from llama_index.core import SimpleDirectoryReader
from langchain_core.runnables import chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.document_compressors import LLMChainFilter
from langchain.retrievers import ContextualCompressionRetriever
from langchain_openai import ChatOpenAI
import faiss
import pdb
import os
from dotenv import load_dotenv
import getpass


load_dotenv()


local_embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=500,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)
index = faiss.IndexFlatL2(len(local_embeddings.embed_query("hello world")))
index_store = './vector_store'
vector_store = FAISS(
    embedding_function = local_embeddings,
    index = index,
    docstore = InMemoryDocstore(),
    index_to_docstore_id = {},
)

def save_to_local(file):
    loader = PyMuPDFLoader(file)
    pages = loader.load()
    for page in pages:
        split_docs = splitter.create_documents([page.page_content])
        print(f"split_docs: {split_docs}")
        faiss_db = FAISS.from_documents(split_docs, local_embeddings)
        if os.path.exists(index_store):
            local_db = FAISS.load_local(index_store, local_embeddings, allow_dangerous_deserialization=True)
            local_db.merge_from(faiss_db)
            print("merge completed")
            local_db.save_local(index_store)
            print("updated index saved")
        else:
            faiss_db.save_local(folder_path=index_store)
            print("new store created ...")
    return {'message':'file uploaded and updated index'}


@chain
def custom_retriever(query:str, topk=10, threshold_score=-0.001):
    query = query["input"]
    print(f"Query is :{query}")
    vectorstore = FAISS.load_local(index_store, local_embeddings, allow_dangerous_deserialization=True)
    cosine_sim = vectorstore._select_relevance_score_fn()
    docs, scores = zip(*vectorstore.similarity_search_with_score(query, k=topk))
    final_docs=[]
    for doc, score in zip(docs, scores):
        print(f"Original score: {score}")
        score = cosine_sim(score)
        print(f"Cosine similarity score: {score}")
        doc.metadata["score"] = round(score, 3)
        if score>threshold_score:
            final_docs.append(doc)
    return final_docs

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def process_message(user_message):
    prompt = """You are an intelligent bot assistant for question-answering tasks.
    The questions will be around given context. If you don't find relavant answer in provided context, feel free to ask for 
    more information. When asked about describe or explain the document, please limit yourself to max of 5 sentences.
    When asked about precise information from document, provide the answer if available. Don't halucinate.

    Question:
    {question}

    Context:
    {context}

"""
    prompt_template = ChatPromptTemplate.from_template(prompt)
    llm = ChatOpenAI(model='gpt-4o-mini', api_key=os.getenv("OPENAI_API_KEY"))
    llmfunction=llm.bind()
    compressor = LLMChainFilter.from_llm(llm=llmfunction)
    compressor_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=custom_retriever
    )

    qa_rag_chain = (
        {
            "context": (
                compressor_retriever
                |
                format_docs),
            "question": RunnablePassthrough()
        }
          |
        prompt_template
          |
        llm
    )

    response = qa_rag_chain.invoke({"input": user_message })
    print(f"Response is :{response.content}")
    return response.content
