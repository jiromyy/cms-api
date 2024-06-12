from src.utils import ContentManagerUtilities
from src.blob_manager import BlobManager
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
import uuid
from dotenv import load_dotenv

load_dotenv()

class IndexManager(ContentManagerUtilities, BlobManager):
    """
    This class contains methods for managing the Azure Cognitive Search index.
    
    The methods in this class are used to:
    - Upload or update an item in the Azure Cognitive Search index
    - Delete an item from the Azure Cognitive Search index
    - Download a blob from Azure Blob Storage to a JSON file
    - List documents in the Azure Cognitive Search index
    - Split text into chunks
    - Serialize chunks
    - Clean data
    - Store vector
    - Embed content
    
    The methods in this class are used by the KnowledgeBaseApp class.
    
    Parameters:
    - aisearch_service_endpoint: the Azure Cognitive Search service endpoint
    - aisearch_index_name: the Azure Cognitive Search index name
    - aisearch_key: the Azure Cognitive Search key
    - openai_api_key: the OpenAI API key
    - openai_api_version: the OpenAI API version
    - openai_endpoint: the OpenAI endpoint
    - connection_string: the connection string for the Azure Blob Storage account
    
    Note: The KnowledgeBaseApp class inherits from the ContentManagerUtilities and BlobManager classes.
    """
    def __init__(self, aisearch_service_endpoint, aisearch_index_name, aisearch_key, openai_api_key, openai_api_version, openai_endpoint, connection_string, blob_name_preprocessing):
        super().__init__(connection_string)
        self.aisearch_service_endpoint = aisearch_service_endpoint
        self.aisearch_index_name = aisearch_index_name
        self.aisearch_key = aisearch_key
        self.openai_api_key = openai_api_key
        self.openai_api_version = openai_api_version
        self.openai_endpoint = openai_endpoint
        self.aisearch_credentials = AzureKeyCredential(self.aisearch_key)
        self.ai_search_service_client = SearchClient(endpoint=self.aisearch_service_endpoint, index_name=self.aisearch_index_name, credential=self.aisearch_credentials)
        self.openai_client = AzureOpenAI(api_key = self.openai_api_key, api_version = self.openai_api_version, azure_endpoint = self.openai_endpoint)
        self.blob_name_preprocessing = blob_name_preprocessing
        
    def upload_update_item_azure_index(self, file, filename, category):
        """
        Upload or update an item in the Azure Cognitive Search index.
        
        Parameters:
        - file: the file to upload or update
        - category: the category of the file
        
        Returns:
        - True if the item was uploaded or updated successfully, False otherwise
        """
        #get the file name without the extension to use as the filename in the json blob
        self.file_name = self.sanitize_filename(filename)

        # Create a temporary file
        self.tmp_path = self._copy_temp(file, filename)
        self.loader = PyPDFLoader(self.tmp_path)
        self.pages = self.loader.load()
        self.chunks = self._split_text(self.pages)
        self.kb_dict = self._serialize_chunks(self.chunks)
        self.kb_dict = self._clean_data(self.kb_dict, category)
        print("BLOB", self.blob_name_preprocessing)
        self.set_blob_service_client(self.blob_name_preprocessing)
        self.upload_dict_to_azure_blob(self.kb_dict, self.file_name + '.json', self.blob_name_preprocessing)
        self.input_data = self.embed(self.kb_dict)
        self.upload_dict_to_azure_blob(self.input_data, self.file_name + '-embedding.json', self.blob_name_preprocessing)
        self._store_vector(self.input_data)
        
        # Delete the temporary file
        self._delete_temp(self.tmp_path)

        return True
    
    def delete_item_azure_index(self, file):
        """
        Delete an item from the Azure Cognitive Search index.
        
        Parameters:
        - file: the file to delete
        
        Returns:
        - True if the item was deleted successfully, False otherwise
        """
        search_client = SearchClient(endpoint=self.aisearch_service_endpoint, index_name=self.aisearch_index_name, credential=self.aisearch_credentials)

        filename = self.sanitize_filename(file) + '.json'
        print(filename)

        data_dict = self.download_azure_blob_to_json(filename, self.blob_name_preprocessing)

        try:
            for item in data_dict:
                document_key = item['id']
                result = search_client.delete_documents([{"@search.action": "delete", "id": document_key}])
            return True
        except Exception as e:
            return False
    
    def download_azure_blob_to_json(self, file, container_name):
        """
        Download a blob from Azure Blob Storage to a JSON file.
        
        Parameters:
        - file: the file to download
        - container_name: the name of the container
        
        Returns:
        - a dictionary containing the data from the JSON file
        """
        self.set_blob_service_client(container_name)
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(file)

        # Download the blob data
        blob_data = blob_client.download_blob().readall()

        # Convert blob data to string
        str_blob_data = blob_data.decode('utf-8')

        # Load string data into a dictionary
        data_dict = json.loads(str_blob_data)

        return data_dict
    
    def list_index_documents(self, filters):
        """
        List documents in the Azure Cognitive Search index.
        
        Returns:
        - a list of documents
        
        Note: The list of documents includes the total count of documents.
        """
        # Perform a search query to list all documents
        #print("Filters", filters)
        results = self.ai_search_service_client.search(search_text="*", include_total_count=True, filter=filters)

        return results

    def _store_vector(self, input_data):
        """
        Store the vector in the Azure Cognitive Search index.
        
        Parameters:
        - input_data: the input data
        
        Returns:
        - None
        """
        self.ai_search_service_client.upload_documents(input_data)
        
    def embed(self, input_data):
        """
        Embed the content.
        
        Parameters:
        - input_data: the input data
        
        Returns:
        - the input data with the content embedded
        """
        model = "text-embedding-ada-002"

        # create embedding function
        from tenacity import retry, wait_random_exponential, stop_after_attempt

        @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
        def generate_embeddings(text, item_id, model=model):
            try:
                return self.openai_client.embeddings.create(input=[text], model=model).data[0].embedding
            except Exception as e:
                print(f"Error generating embeddings for item ID {item_id}: {e}")
                return None
            
        # Generate embeddings for content field
        for item in input_data:
            content = item['content']
            content_embeddings = generate_embeddings(content, item['id'])
            item['contentVector'] = content_embeddings
            
        print("Embedding complete")
        
        return input_data
    
    def _split_text(self, docs):
        """
        Split the text into chunks.
        
        Parameters:
        - docs: the documents
        
        Returns:
        - the chunks
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=3500, 
            chunk_overlap=400, 
            length_function=len
        )
        
        self.chunks = self.text_splitter.split_documents(docs)
        return self.chunks

    def _serialize_chunks(self, chunks):
        """
        Serialize the chunks.
        
        Parameters:
        - chunks: the chunks
        
        Returns:
        - the serialized object
        """
        # serialize to json string
        self.serialized_obj = json.dumps(chunks, default=lambda x: x.__dict__)

        # deserialize from json string into a python dict
        self.kb_dict = json.loads(self.serialized_obj)
        
        return self.kb_dict

    def _clean_data(self, kb_dict, category):
        """
        Clean the data.
        
        Parameters:
        - kb_dict: the knowledge base dictionary
        - category: the category of the document
        
        Returns:
        - the cleaned data
        """
        # delete type : Document kv pair
        for dictionary in kb_dict:
            if 'type' in dictionary:
                del dictionary['type']

        # rename keys: 'page_content' to 'content' and 'source' to 'file_location'
        for dictionary in kb_dict:
            if 'page_content' in dictionary:
                dictionary['content'] = dictionary.pop('page_content')
            if 'metadata' in dictionary and 'source' in dictionary['metadata']:
                dictionary['metadata']['file_location'] = dictionary['metadata'].pop('source')

        # add key: 'document_title' to 'metadata' dict.
        for dictionary in kb_dict:
            if 'metadata' in dictionary and 'file_location' in dictionary['metadata']:
                file_location = dictionary['metadata']['file_location']
                # split into substing using '/' as separator and get last element - the file name
                document_title = file_location.split('/')[-1]
                dictionary['metadata']['document_title'] = document_title

        container = self.blob_link
        path = self.blob_path
        blob_sas_token = self.blob_sas

        # add key: 'download_url' as top level key with value as container + document_title + blob_sas_token

        for dictionary in kb_dict:
            if 'metadata' in dictionary and 'document_title' in dictionary['metadata']:
                document_title = dictionary['metadata']['document_title']
                # Update the download_url with container, document_title, and blob_sas_token
                dictionary['download_url'] = f'{container}{path}{document_title}?{blob_sas_token}'

        # add keys 'file_location' and 'document_title' as top level keys and delete 'metadata' key
        for dictionary in kb_dict:
            if 'metadata' in dictionary:
                dictionary['file_location'] = dictionary['metadata']['file_location']
                dictionary['document_title'] = dictionary['metadata']['document_title']
                del dictionary['metadata']
                
        # add key: 'category'
        for dictionary in kb_dict:
            dictionary['category'] = category
                
        # Add a new UUID as 'id'
        for dictionary in kb_dict:
            dictionary['id'] = str(uuid.uuid4())

        # print random item
        return kb_dict