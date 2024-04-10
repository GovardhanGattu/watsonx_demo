from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from src.utils import provide_watson_llm,initiate_retrieval_chain
from src.Components.prompt_templates import data_analytics_prompt

#specify the model id to get configure the Watson LLM
model_id = "meta-llama/llama-2-70b-chat"

#get the llm from the WatsonMML Provider by passing model id
llm = provide_watson_llm(model_id)

#Load the embeddings model to convert the user prompt into vecot embeddings
instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")

#Mention the path of the vectorDB to use
persist_directory = "Procurement_chromadb"



def procurement_retriever(query):
    vectordb =Chroma(persist_directory=persist_directory,embedding_function=instructor_embeddings)
    retriever = vectordb.as_retriever()
    rdocs=retriever.get_relevant_documents(query)
    return rdocs

def procurement_chain(query):
    vectordb =Chroma(persist_directory=persist_directory,embedding_function=instructor_embeddings)
    retriever = vectordb.as_retriever()
    prompt_template = data_analytics_prompt()
    reponse = initiate_retrieval_chain(llm=llm,prompt_template=prompt_template,query=query,retriever=retriever)
    return reponse

if __name__=="__main__":
    chain=procurement_chain("Order stuck in scheduled status")
    
