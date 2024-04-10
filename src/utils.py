from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from langchain_ibm import WatsonxLLM
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import  create_retrieval_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

#This class will provide the completely configured WatsonLLM  

def provide_watson_llm(model_id):
    credentials = {
            "url": "https://us-south.ml.cloud.ibm.com",
            "apikey": os.environ["WATSONX_API_KEY"]
        }
    project_id = os.environ["PRODUCT_ID"]
    parameters = {
            GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
            GenParams.MAX_NEW_TOKENS: 300,
            GenParams.MIN_NEW_TOKENS: 1,
            GenParams.TEMPERATURE: 0.3,
            GenParams.TOP_K: 50,
            GenParams.TOP_P: 1
        }
    llm = WatsonxLLM(
            model_id=model_id,
            url=credentials.get("url"),
            apikey=credentials.get("apikey"),
            project_id=project_id,
            params=parameters
        )
    
    return llm



def initiate_retrieval_chain(llm,prompt_template,query,retriever):
    prompt = PromptTemplate.from_template(prompt_template)
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
    answer=retrieval_chain.invoke({"input":query})
    return answer



if __name__=="__main__":
    llm = provide_watson_llm()

