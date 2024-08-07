from pydantic import BaseModel
import os

# TODO: move this to the config folder/directory
class AppConfigValues(BaseModel):
    config_values: dict
    
def get_config_values(app_config):
    config_values = {
        "openai_api_key": os.getenv(app_config.config_values["azure_openai_resource"]["openai_api_key"]),
        "openai_api_version": os.getenv(app_config.config_values["azure_openai_resource"]["openai_api_version"]),
        "openai_endpoint": os.getenv(app_config.config_values["azure_openai_resource"]["openai_endpoint"]),
        "embedding_model_name": os.getenv(app_config.config_values["azure_openai_resource"]["embedding_model_name"]),
        
        "cosmosdb_url": os.getenv(app_config.config_values["cosmosdb_config"]["cosmosdb_url"]),
        "cosmosdb_key": os.getenv(app_config.config_values["cosmosdb_config"]["cosmosdb_key"]),
        "cosmosdb_database_name": os.getenv(app_config.config_values["cosmosdb_config"]["cosmosdb_database_name"]),
        "cosmosdb_container_name": os.getenv(app_config.config_values["cosmosdb_config"]["cosmosdb_container_name"]),

        "aisearch_service_endpoint": os.getenv(app_config.config_values["ai_search_config"]["aisearch_service_endpoint"]),
        "aisearch_key": os.getenv(app_config.config_values["ai_search_config"]["aisearch_key"]),
        "index_ccu": os.getenv(app_config.config_values["ai_search_config"]["index_ccu"]),
        "index_aspen": os.getenv(app_config.config_values["ai_search_config"]["index_aspen"]),
        "index_rlc": os.getenv(app_config.config_values["ai_search_config"]["index_rlc"]),
        "index_jgsoc": os.getenv(app_config.config_values["ai_search_config"]["index_jgsoc"]),
        "index_rrhi": os.getenv(app_config.config_values["ai_search_config"]["index_rrhi"]),
        "index_urc": os.getenv(app_config.config_values["ai_search_config"]["index_urc"]),

        "blob_connection_string": os.getenv(app_config.config_values["blob_storage_config"]["blob_connection_string"]),
        "blob_preprocessing": os.getenv(app_config.config_values["blob_storage_config"]["blob_name_preprocessing"]),
        "blob_ccu": os.getenv(app_config.config_values["blob_storage_config"]["blob_name_ccu"]),
        "blob_aspen": os.getenv(app_config.config_values["blob_storage_config"]["blob_name_aspen"]),
        "blob_rlc": os.getenv(app_config.config_values["blob_storage_config"]["blob_name_rlc"]),
        "blob_jgsoc": os.getenv(app_config.config_values["blob_storage_config"]["blob_name_jgsoc"]),
        "blob_rrhi": os.getenv(app_config.config_values["blob_storage_config"]["blob_name_rrhi"]),
        "blob_urc": os.getenv(app_config.config_values["blob_storage_config"]["blob_name_urc"]),
        "blob_link": os.getenv(app_config.config_values["blob_storage_config"]["blob_link"]),
        "blob_sas_token": os.getenv(app_config.config_values["blob_storage_config"]["blob_sas_token"]),
    }
    return config_values
