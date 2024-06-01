import json
import os
import base64
import tempfile
from dateutil import tz
from flask import jsonify, request
from flask_smorest import Blueprint
from flask.views import MethodView
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from src.config.app_config_values import get_config_values
from src.blob_manager import BlobManager
from src.index_manager import IndexManager
from src.utils import ContentManagerUtilities
from src.auth import validate_secret_key
from src.config.fetch_app_config import fetch_app_config
from langchain_community.document_loaders import PyPDFLoader

from src.schemas.api_models_generic import (
    HeaderDataSchema, 
    HeaderData, 
    ReturnData, 
    ReturnDataSchema)

from src.schemas.api_models_cms import (
    ListItemSchema,
    ListReturnData,
    ListItem,
    ListReturnDataSchema,
    UploadBodyData,
    UploadBodyDataSchema)

content_manager_bp = Blueprint("Content Manager", __name__, url_prefix="/v1", description="Content Management System API")

@content_manager_bp.route("/test")
class ContentManager(MethodView):
    
    @content_manager_bp.arguments(HeaderDataSchema, location="headers")
    @content_manager_bp.response(200, ReturnDataSchema)
    @validate_secret_key.validate_secret_key
    def get(self, header_data: HeaderData):
        
        response = ReturnData(
            status=200,
            message="Content Manager API is working",
            data=header_data.user
        )
        return response
    
@content_manager_bp.route("/process/<file>")
class ProcessView(MethodView):
    @content_manager_bp.arguments(HeaderDataSchema, location="headers")
    @content_manager_bp.arguments(UploadBodyDataSchema, location="json")
    @content_manager_bp.response(200, ReturnDataSchema)
    @content_manager_bp.response(500, ReturnDataSchema)
    @validate_secret_key.validate_secret_key
    def post(self, header_data: HeaderData, upload_body_data: UploadBodyData, file:str):
            
        filename = file
        applicability = upload_body_data.applicability
        function = upload_body_data.function
        data = upload_body_data.data
        
        pdf_bytes = base64.b64decode(data)

        # Write the bytes to a PDF file
        with open("output.pdf", "wb") as pdf_file:
            pdf_file.write(pdf_bytes)
        
        app_id = request.headers.get("X-APP-ID")
        app_config = fetch_app_config(app_id)
        config_values = get_config_values(app_config)
        blob_name = {
            "ccu": config_values.get("blob_name_ccu"),
            "aspen": config_values.get("blob_name_aspen"),
            "rrhi": config_values.get("blob_name_rrhi"),
            "rlc": config_values.get("blob_name_rlc"),
            "jgsoc": config_values.get("blob_name_jgsoc")
        }
        
        
        blob = BlobManager(config_values.get("blob_connection_string"))
        index = IndexManager(config_values.get("aisearch_service_endpoint"), config_values.get("aisearch_index"), config_values.get("aisearch_key"), config_values.get("openai_api_key"), config_values.get("openai_api_version"), config_values.get("openai_endpoint"), config_values.get("blob_connection_string"), config_values.get("blob_name_preprocessing"))

        if applicability.lower() == "generic":
            for bu in blob_name.keys():
                        blob.set_blob_service_client(blob_name[bu])
                        res = blob.upload_azure_blob_item(data, function.lower()+'/generic/')
        else:
            blob.set_blob_service_client(blob_name[applicability.lower()])
            res = blob.upload_azure_blob_item(pdf_bytes, filename, function.lower()+'/specific/')
        
        if res:
            res = index.upload_update_item_azure_index(pdf_bytes, filename, function)
            if res:
                response = ReturnData(
                    status=200,
                    message="Content uploaded successfully"
                )
            else:
                response = ReturnData(
                    status=500,
                    message="Error uploading to the index"
                )
        else:
            print("already exists in the container. Use the update button instead.")
            response = ReturnData(
                status=500,
                message="Error uploading to the blob"
            )

        return jsonify(response)
    
    @content_manager_bp.arguments(HeaderDataSchema, location="headers")
    @content_manager_bp.response(200, ReturnDataSchema)
    @content_manager_bp.response(404, ReturnDataSchema)
    @validate_secret_key.validate_secret_key
    def delete(self, header_data: HeaderData, file:str):
        
        app_id = request.headers.get("X-APP-ID")
        app_config = fetch_app_config(app_id)
        config_values = get_config_values(app_config)
        blob_name = {
            "ccu": config_values.get("blob_name_ccu"),
            "aspen": config_values.get("blob_name_aspen"),
            "rrhi": config_values.get("blob_name_rrhi"),
            "rlc": config_values.get("blob_name_rlc"),
            "jgsoc": config_values.get("blob_name_jgsoc")
        }
        
        print("Blob Name", blob_name)

        aisearch_credentials = AzureKeyCredential(config_values.get("aisearch_key"))

        index = IndexManager(config_values.get("aisearch_service_endpoint"), config_values.get("aisearch_index"), config_values.get("aisearch_key"), config_values.get("openai_api_key"), config_values.get("openai_api_version"), config_values.get("openai_endpoint"), config_values.get("blob_connection_string"), config_values.get("blob_name_preprocessing"))
        blob = BlobManager(config_values.get("blob_connection_string"))
        
        index_list = index.list_index_documents(f"document_title eq '{file}'")
        search_client = SearchClient(endpoint=config_values.get("aisearch_service_endpoint"), index_name=config_values.get("aisearch_index"), credential=aisearch_credentials)
        
        doc_url = None
        
        # Delete the document from the index
        for item in index_list:
            document_key = item.get('id')
            doc_url = item.get('download_url')
            
            search_client.delete_documents([{"@search.action": "delete", "id": document_key}])
        print(doc_url)
        if doc_url:
            response = ReturnData(
                status=200,
                message="Content deleted successfully",
                data=header_data.user
            )
            
            # Delete the document from the blob storage
            if "generic" in doc_url:
                function = doc_url.split("/")[4]
                
                for bu in blob_name.keys():
                    print(blob_name[bu.lower()])
                    blob.set_blob_service_client(blob_name[bu.lower()])
                    res = blob.delete_azure_blob_item(file, f"{function}/generic/")
                    print(res)
            else:
                bu = doc_url.split("/")[3]
                function = doc_url.split("/")[4]
                blob.set_blob_service_client(bu)
                blob.delete_azure_blob_item(file, f"{function}/specific/")
                
            # Delete the document from the preprocessing blob storage
            blob.set_blob_service_client(config_values.get("blob_name_preprocessing"))
            utils = ContentManagerUtilities()
            sanitized_file = utils.sanitize_filename(file)
            blob.delete_azure_blob_item(sanitized_file + ".json", "")
            blob.delete_azure_blob_item(sanitized_file + "-embedding.json", "")
        else:
            response = ReturnData(
                status=404,
                message="Content not found",
                data=header_data.user
            )
            
        return response
        
@content_manager_bp.route("/update")
class UpdateView(MethodView):
    @content_manager_bp.arguments(HeaderDataSchema, location="headers")
    @content_manager_bp.response(200, ReturnDataSchema)
    @validate_secret_key.validate_secret_key
    def put(self, header_data: HeaderData):
        
        response = ReturnData(
            status=200,
            message="Content Manager API is working",
            data=header_data.user
        )
        return response

@content_manager_bp.route("/list/<applicability>/<function>")
class ListView(MethodView):
    @content_manager_bp.arguments(HeaderDataSchema, location="headers")
    @content_manager_bp.response(200, ReturnDataSchema)
    @validate_secret_key.validate_secret_key
    def get(self, header_data: HeaderData, applicability:str, function:str):
        
        app_id = request.headers.get("X-APP-ID")
        app_config = fetch_app_config(app_id)
        config_values = get_config_values(app_config)
        
        blob_name = {
            "ccu": config_values.get("blob_name_ccu"),
            "aspen": config_values.get("blob_name_aspen"),
            "rrhi": config_values.get("blob_name_rrhi"),
            "rlc": config_values.get("blob_name_rlc"),
            "jgsoc": config_values.get("blob_name_jgsoc")
        }
        
        index = IndexManager(config_values.get("aisearch_service_endpoint"), config_values.get("aisearch_index"), config_values.get("aisearch_key"), config_values.get("openai_api_key"), config_values.get("openai_api_version"), config_values.get("openai_endpoint"), config_values.get("blob_connection_string"), config_values.get("blob_name_preprocessing"))
        blob = BlobManager(config_values.get("blob_connection_string"))
        
        print("Index", index)
        print("Blob", blob.blob_service_client)
        
        index_list = index.list_index_documents(f"category eq '{function}'")
        
        files = []
        item_schema = ListItemSchema()
        for item in index_list:
            
            if not any(d['document_title'] == item['document_title'] for d in files):
                del item["@search.score"]
                del item["@search.reranker_score"]
                del item["@search.highlights"]
                del item["@search.captions"]
                del item["contentVector"]
                del item["content"]
                del item["file_location"]
                
                if function != "HR":
                    files.append(item_schema.dump(item))
                else:
                
                    if "generic" in applicability:
                        if function.lower()+'/generic' in item['download_url']:
                            blob_client = blob.blob_service_client.get_blob_client(config_values.get("blob_name_ccu"), function.lower()+'/generic/'+item['document_title'])
                            blob_properties = blob_client.get_blob_properties()
                            item["file_size"] = f"{round(int(blob_properties.size)/1024/1024,2)}MB"
                            item["created_date"] = blob_properties.creation_time.astimezone(tz.tzlocal()).strftime("%m-%d-%Y %I:%M %p")
                            item["modified_date"] = blob_properties.last_modified.astimezone(tz.tzlocal()).strftime("%m-%d-%Y %I:%M %p")
                            files.append(item_schema.dump(item))
                    else:
                        if blob_name[applicability.lower()]+'/'+function.lower()+'/specific' in item['download_url']:
                            blob_client = blob.blob_service_client.get_blob_client(blob_name[applicability.lower()], function.lower()+'/specific/'+item['document_title'])
                            blob_properties = blob_client.get_blob_properties()
                            item["file_size"] = f"{round(int(blob_properties.size)/1024/1024,2)}MB"
                            item["created_date"] = blob_properties.creation_time.astimezone(tz.tzlocal()).strftime("%m-%d-%Y %I:%M %p")
                            item["modified_date"] = blob_properties.last_modified.astimezone(tz.tzlocal()).strftime("%m-%d-%Y %I:%M %p")
                            files.append(item_schema.dump(item))
                        
        response = ListReturnData(
            status=200,
            message="Successfuly retrieved list of files",
            data=files
        )

        return jsonify(response)
    
    
