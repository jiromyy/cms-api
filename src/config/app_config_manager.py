class AppConfigManager:
    APP_CONFIG = {
        "10101010": {
                "project_name": "content-management-system",                     
                "secret_key": "CMS_FRONTEND_REQUESTS_API_KEY", 
                "azure_openai_resource": {
                    "openai_endpoint": "CMS_AZURE_OPENAI_ENDPOINT",
                    "openai_api_key": "CMS_AZURE_OPENAI_API_KEY",
                    "openai_api_version": "CMS_AZURE_OPENAI_API_VERSION",
                    "embedding_model_name": "CMS_AZURE_OPENAI_EMBEDDING_MODEL_NAME"
                    },
                "cosmosdb_config": {
                    "cosmosdb_url": "CMS_COSMOSDB_URL",
                    "cosmosdb_key": "CMS_COSMOSDB_ACCOUNT_KEY",
                    "cosmosdb_database_name": "CMS_COSMOSDB_DATABASE",
                    "cosmosdb_container_name": "CMS_COSMOSDB_CONVERSATIONS_CONTAINER"
                },
                "ai_search_config": {
                    "aisearch_service_endpoint": "CMS_AZURE_AI_SEARCH_ENDPOINT",
                    "aisearch_index": "CMS_AZURE_AI_SEARCH_INDEX_NAME",
                    "aisearch_key": "CMS_AZURE_AI_SEARCH_API_KEY"
                },
                "blob_storage_config": {
                    "blob_connection_string": "CMS_AZURE_BLOB_CONNECTION_STRING",
                    "blob_name_preprocessing": "CMS_AZURE_BLOB_NAME_PREPROCESSING",
                    "blob_link":"CMS_AZURE_BLOB_LINK",
                    "blob_sas_token": "CMS_AZURE_BLOB_SAS_TOKEN",
                    "blob_name_ccu": "CMS_AZURE_BLOB_CCU_CONTAINER_NAME",
                    "blob_name_aspen": "CMS_AZURE_BLOB_ASPEN_CONTAINER_NAME",
                    "blob_name_rlc": "CMS_AZURE_BLOB_RLC_CONTAINER_NAME",
                    "blob_name_jgsoc": "CMS_AZURE_BLOB_JGSOC_CONTAINER_NAME",
                    "blob_name_rrhi": "CMS_AZURE_BLOB_RRHI_CONTAINER_NAME",
                },
           },     
    }


