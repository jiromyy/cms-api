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
                    "aisearch_key": "CMS_AZURE_AI_SEARCH_API_KEY",
                    "index_ccu": "CMS_AI_SEARCH_INDEX_NAME_CCU",
                    "index_aspen": "CMS_AI_SEARCH_INDEX_NAME_ASPEN",
                    "index_rlc": "CMS_AI_SEARCH_INDEX_NAME_RLC",
                    "index_jgsoc": "CMS_AI_SEARCH_INDEX_NAME_JGSOC",
                    "index_rrhi": "CMS_AI_SEARCH_INDEX_NAME_RRHI",
                    "index_urc": "CMS_AI_SEARCH_INDEX_NAME_URC",
                },
                "blob_storage_config": {
                    "blob_connection_string": "CMS_AZURE_BLOB_CONNECTION_STRING",
                    "blob_name_preprocessing": "CMS_AZURE_BLOB_CONTAINER_NAME_PREPROCESS",
                    "blob_link":"CMS_AZURE_BLOB_LINK",
                    "blob_sas_token": "CCU_AZURE_BLOB_SAS_TOKEN",
                    "blob_name_ccu": "CMS_AZURE_BLOB_CONTAINER_NAME_CCU",
                    "blob_name_aspen": "CMS_AZURE_BLOB_CONTAINER_NAME_ASPEN",
                    "blob_name_rlc": "CMS_AZURE_BLOB_CONTAINER_NAME_RLC",
                    "blob_name_jgsoc": "CMS_AZURE_BLOB_CONTAINER_NAME_JGSOC",
                    "blob_name_rrhi": "CMS_AZURE_BLOB_CONTAINER_NAME_RRHI",
                    "blob_name_urc": "CMS_AZURE_BLOB_CONTAINER_NAME_URC",
                },
           },     
    }