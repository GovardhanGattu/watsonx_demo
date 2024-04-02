from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import  RetrievalQA ,create_retrieval_chain
from langchain.prompts import PromptTemplate
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from ibm_watsonx_ai.foundation_models import ModelInference
from langchain_ibm import WatsonxLLM
from dotenv import load_dotenv
import os

load_dotenv()

credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "apikey": os.environ["WATSONX_API_KEY"]
}
project_id = os.environ["PRODUCT_ID"]
model_id = "meta-llama/llama-2-70b-chat"

parameters = {
    GenParams.DECODING_METHOD: DecodingMethods.SAMPLE,
    GenParams.MAX_NEW_TOKENS: 300,
    GenParams.MIN_NEW_TOKENS: 1,
    GenParams.TEMPERATURE: 0.3,
    GenParams.TOP_K: 50,
    GenParams.TOP_P: 1
}


instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")

persist_directory = "chromadb"


# cloader = CSVLoader(file_path='incidents_data.csv',source_column='Description')
# data = cloader.load()

# def createChromaDB():
    
#     vchromadb= Chroma.from_documents(documents=data,embedding=instructor_embeddings,persist_directory=persist_directory)
#     vchromadb.persist()

def retriever(query):
    vectordb =Chroma(persist_directory=persist_directory,embedding_function=instructor_embeddings)
    retriever = vectordb.as_retriever()
    rdocs=retriever.get_relevant_documents(query)
    return rdocs

def getQAChain(query):
    vectordb =Chroma(persist_directory=persist_directory,embedding_function=instructor_embeddings)
    retriever = vectordb.as_retriever()
    # rdocs = retriever.get_relevant_documents(query)
    # print("FROM the Retrieval document :::: ",rdocs)

    template = """
    Provide me the answer along with incident numbers from Number column and 
    knowledge base article from the Description column.Don't provide output: in the answer.
    context: {context}
    input: {input}
    """

    llm = WatsonxLLM(
    model_id=model_id,
    url=credentials.get("url"),
    apikey=credentials.get("apikey"),
    project_id=project_id,
    params=parameters
)

    prompt = PromptTemplate.from_template(template)
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
    answer=retrieval_chain.invoke({"input":query})
    return answer

if __name__=="__main__":
    chain=getQAChain("Order stuck in scheduled status")
    