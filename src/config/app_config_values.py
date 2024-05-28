from pydantic import BaseModel
import os

# TODO: move this to the config folder/directory
class AppConfigValues(BaseModel):
    config_values: dict
    
def get_config_values(app_config):
    config_values = {
        "aisearch_service_endpoint": os.getenv(app_config.config_values["ai_search_config"]["aisearch_service_endpoint"]),
        "aisearch_index": os.getenv(app_config.config_values["ai_search_config"]["aisearch_index"]),
        "aisearch_key": os.getenv(app_config.config_values["ai_search_config"]["aisearch_key"]),
        "openai_api_key": os.getenv(app_config.config_values["azure_openai_resource"]["openai_api_key"]),
        "openai_api_version": os.getenv(app_config.config_values["azure_openai_resource"]["openai_api_version"]),
        "openai_endpoint": os.getenv(app_config.config_values["azure_openai_resource"]["openai_endpoint"]),
        "blob_connection_string": os.getenv(app_config.config_values["blob_storage_config"]["blob_connection_string"]),
        "blob_name_preprocessing": os.getenv(app_config.config_values["blob_storage_config"]["blob_name_preprocessing"]),
        "blob_name_ccu": os.getenv(app_config.config_values["blob_storage_config"]["blob_name_ccu"]),
        "blob_name_aspen": os.getenv(app_config.config_values["blob_storage_config"]["blob_name_aspen"]),
        "blob_name_rlc": os.getenv(app_config.config_values["blob_storage_config"]["blob_name_rlc"]),
        "blob_name_jgsoc": os.getenv(app_config.config_values["blob_storage_config"]["blob_name_jgsoc"]),
        "blob_name_rrhi": os.getenv(app_config.config_values["blob_storage_config"]["blob_name_rrhi"]),
    }
    return config_values
