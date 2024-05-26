from dataclasses import dataclass 
from typing import Dict, Any, Optional
from marshmallow import fields, EXCLUDE
from desert import field, schema_class
from src.schemas.api_models_cms import (
    ListReturnDataSchema,
    ListReturnData)


meta = {"unknown": EXCLUDE}

@dataclass(slots=True)
class HeaderData:
    """
    Handles API header data payload
    """
    api_secret_key: str = field(fields.String(data_key="X-API-SECRET-KEY"), default="123")
    app_id: str = field(fields.String(data_key="X-APP-ID"), default="10101010")
    user: str = field(fields.String(), default="test_user")
    
@dataclass(slots=True)
class ReturnData:
    """
    Handles API response data payload.
    """
    status: int
    message: str
    data: Optional[str] = None
    
# Schemas
HeaderDataSchema = schema_class(HeaderData, meta=meta)
ReturnDataSchema = schema_class(ReturnData, meta=meta)