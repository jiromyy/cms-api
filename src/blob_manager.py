from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions, ContentSettings
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv
import base64

load_dotenv(".env.development", override=True)

class BlobManager:
    """
    This class contains methods for managing Azure Blob Storage.
    
    The methods in this class are used to:
    - Set the Blob Service Client
    - Set the Blob Item URL
    - List Blobs
    - Upload an Azure Blob Item
    - Update an Azure Blob Item
    - Delete an Azure Blob Item
    - Upload a dictionary to an Azure Blob
    - Generate a SAS token
    
    The methods in this class are used by the IndexManager class.
    
    Parameters:
    - connection_string: the connection string for the Azure Blob Storage account
    """
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.blob_link = None
        self.blob_path = None
        self.blob_sas = None
        
        self.blob_name_preprocessing = None
        self.container_client = None
                
    def set_blob_service_client(self, container_name):
        """
        Set the Blob Service Client and Container Client.
        
        Parameters:
        - container_name: the name of the container
        
        Returns:
        - None
        """
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)
        
    def set_blob_item_url(self, blob_link, blob_path, blob_sas):
        """
        Set the Blob Item URL.
        
        Parameters:
        - blob_link: the link to the blob
        - blob_path: the path to the blob
        - blob_sas: the Shared Access Signature (SAS) token
        
        Returns:
        - None
        """
        self.blob_link = blob_link
        self.blob_path = blob_path
        self.blob_sas = blob_sas

    def list_blob(self, subfolder):
        """
        List the blobs in a subfolder.
        
        Parameters:
        - subfolder: the subfolder
        
        Returns:
        - a list of blobs
        """
        return self.container_client.list_blobs(name_starts_with=subfolder)

    def upload_azure_blob_item(self, file, filename, path):
        """
        Upload an Azure Blob Item.
        
        Parameters:
        - file: the file to upload
        - path: the path to the file
        
        Returns:
        - True if the file was uploaded successfully, False otherwise
        """
        self.blob_client = self.container_client.get_blob_client(f'{path}{filename}')
        try:
            # Specify the content type
            content_settings = ContentSettings(content_type='application/pdf')
            
            self.blob_client.upload_blob(file, content_settings=content_settings)
            return True
        except Exception as e:
            print(e)
            return False
        
    def update_azure_blob_item(self, file, filename, path):
        """
        Update an Azure Blob Item.
        
        Parameters:
        - file: the file to update
        - path: the path to the file
        
        Returns:
        - True if the file was updated successfully, False otherwise
        """
        self.blob_client = self.container_client.get_blob_client(f'{path}{filename}')
        try:
            
            # Specify the content type
            content_settings = ContentSettings(content_type='application/pdf')
            
            self.blob_client.upload_blob(file, overwrite=True, content_settings=content_settings)
            return True
        except Exception as e:
            return False
        
    def delete_azure_blob_item(self, file, path):
        """
        Delete an Azure Blob Item.
        
        Parameters:
        - file: the file to delete
        - path: the path to the file
        
        Returns:
        - True if the file was deleted successfully, False otherwise
        """
        print("delete", file, path)
        try:
            self.container_client.delete_blob(f'{path}{file}')
            return True
        except Exception as e:
            return False
        
    def upload_dict_to_azure_blob(self, data_dict, blob_name, container_name):
        """
        Upload a dictionary to an Azure Blob.
        
        Parameters:
        - data_dict: the dictionary to upload
        - blob_name: the name of the blob
        - container_name: the name of the container
        
        Returns:
        - None
        """
        # Convert the dictionary to a JSON string
        self.json_data = json.dumps(data_dict, indent=4)

        # Get a reference to the container
        container_client = self.blob_service_client.get_container_client(container_name)

        # Get a reference to the blob (file)
        self.blob_client = container_client.get_blob_client(blob_name)

        # Upload the JSON data
        self.blob_client.upload_blob(self.json_data, blob_type="BlockBlob", overwrite=True)
        
    def generate_sas_token(self, blob_name):
        """
        Generate a Shared Access Signature (SAS) token.
        
        Parameters:
        - blob_name: the name of the blob
        
        Returns:
        - the SAS token
        
        Note: The SAS token is valid for 1 hour.
        """
        sas_token = generate_blob_sas(
            account_name=self.blob_service_client.account_name,
            account_key=self.blob_service_client.credential.account_key,
            container_name=self.container_client.container_name,
            blob_name=blob_name,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
        )
        return sas_token
