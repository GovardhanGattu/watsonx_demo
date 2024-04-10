from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from data_ingestion import initiate_data_ingestion

instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")

#get the data from data ingestion file



#This class is used to create the embeddings for the input data and stores it in chroma vector database

def initiate_data_embedding(persist_directory):
    data = initiate_data_ingestion()
    chromadb= Chroma.from_documents(documents=data,embedding=instructor_embeddings,persist_directory=persist_directory)
    #save the model in the directory chromadb
    chromadb.persist()
        

if __name__=="__main__":
    persist_directory = "Procurement_chromadb"
    initiate_data_embedding(persist_directory)
