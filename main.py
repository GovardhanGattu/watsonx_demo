from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores.chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate


load_dotenv()
google_api_key =os.environ["GOOGLE_API_KEY"]
llm = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=google_api_key,convert_system_message_to_human=True)

faiss_file = "faiss_index"
persist_directory = "chromadb"

instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
loader = CSVLoader(file_path='incidents_data.csv',source_column="Description")
data = loader.load()

def createChromaDB():
    vchromadb=Chroma.from_documents(documents=data,embedding=instructor_embeddings,persist_directory=persist_directory)
    vchromadb.persist()
    vchromadb=None


def getQAChain(query):
    vectordb = Chroma(persist_directory=persist_directory,embedding_function=instructor_embeddings)
    retriever = vectordb.as_retriever()

    template = """
    Your are an helpful AI assistant
    Answer based on the context provided.In the answer try to provide the text from the number column 
    and Description only.In the answer provide me all the relavant data.Please convert the answer 
    to plain text seperated by |
    context: {context}
    input: {input}
    answer : """

    prompt = PromptTemplate.from_template(template)
    combine_doc_chain= create_stuff_documents_chain(llm,prompt)
    retrieval_chain = create_retrieval_chain(retriever ,combine_doc_chain)
    response = retrieval_chain.invoke({"input":query})
    
    return response


if __name__=="__main__":
    chain = getQAChain("Order stuck in scheduled status")
    print(chain["answer"])


