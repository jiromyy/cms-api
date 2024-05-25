from flask import request
from flask_smorest import abort
from src.config.fetch_app_config import fetch_app_config
import os

def validate_secret_key(func):
    """
    Decorator to validate the API secret key provided in the request header.

    This decorator checks the 'X-API-SECRET-KEY' value in the request headers against
    a predefined key. If the key matches, the decorated function is executed. If not,
    it aborts the request with a 401 Unauthorized status.    
    """
    def validate_and_execute(*args, **kwargs):

        app_id = request.headers.get("X-APP-ID")
        app_config = fetch_app_config(app_id)
        
        secret_value = os.getenv(app_config.config_values["secret_key"])        
        if secret_value and secret_value == request.headers.get("X-API-SECRET-KEY"):                
            return func(*args, **kwargs)

        abort(401, message="Unauthorized: Invalid API Key")

    return validate_and_execute