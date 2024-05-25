class AppConfigManager:
    APP_CONFIG = {
        "10101010": {
                "project_name": "bcfg-sana-all",     
                "routing_system_message": "BCFG_ROUTING_SYSTEM_MESSAGE",
                "synthesis_system_message": "BCFG_SYNTHESIS_SYSTEM_MESSAGE",                
                "secret_key": "BCFG_FRONTEND_REQUESTS_API_KEY", 
                "azure_openai_resource": {
                    "api_endpoint": "BCFG_AZURE_OPENAI_ENDPOINT",
                    "api_key": "BCFG_AZURE_OPENAI_API_KEY",
                    "api_version": "BCFG_AZURE_OPENAI_API_VERSION",
                    "embedding_model_name": "BCFG_AZURE_OPENAI_EMBEDDING_MODEL_NAME"
                    }
                },
                "vector_db_config": {                                        
                    "vector_db_endpoint": "BCFG_AZURE_AI_SEARCH_ENDPOINT",
                    "vector_db_api_key": "BCFG_AZURE_AI_SEARCH_API_KEY",
                    "vector_db_index_name": "BCFG_AZURE_AI_SEARCH_INDEX_NAME",                    
                },
                "cosmosdb_config": {
                    "cosmosdb_url": "BCFG_COSMOSDB_URL",
                    "cosmosdb_key": "BCFG_COSMOSDB_ACCOUNT_KEY",
                    "cosmosdb_database_name": "BCFG_COSMOSDB_DATABASE",
                    "cosmosdb_container_name": "BCFG_COSMOSDB_CONVERSATIONS_CONTAINER"
                }
    }


