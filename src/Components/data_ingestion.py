from langchain_community.document_loaders.csv_loader import CSVLoader

def initiate_data_ingestion():
    loader = CSVLoader(file_path='data/goods_data.csv')
    data = loader.load()
    return data



if __name__=="__main__":
    initiate_data_ingestion()
   