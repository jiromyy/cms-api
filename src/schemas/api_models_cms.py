from dataclasses import dataclass 
from typing import Any, Dict, Optional
from marshmallow import fields, EXCLUDE
from desert import field, schema_class

meta = {"unknown": EXCLUDE}

@dataclass(slots=True)
class ListItem:
    """
    Handles API response data payload.
    """
    id: str
    category: str
    document_title: str
    download_url: str
    edit_url: str
    created_date: str
    modified_date: str
    created_by: str
    file_size: str
    
@dataclass(slots=True)
class ListReturnData:
    """
    Handles API response data payload.
    """
    status: int
    message: str
    data: Optional[ListItem] = None
    
@dataclass(slots=True)
class UploadBodyData:
    """
    Handles API response data payload.
    """
    applicability: str
    function: str
    data: str
    

ListItemSchema = schema_class(ListItem, meta=meta)
ListReturnDataSchema = schema_class(ListReturnData, meta=meta)
UploadBodyDataSchema = schema_class(UploadBodyData, meta=meta)
    