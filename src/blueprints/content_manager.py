from flask_smorest import Blueprint
from flask.views import MethodView
from src.auth import validate_secret_key

from src.schemas.api_models_generic import (
    HeaderDataSchema, 
    HeaderData, 
    ReturnData, 
    ReturnDataSchema)

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
    
    
@content_manager_bp.route("/upload")
class UploadView(MethodView):
    
    @content_manager_bp.arguments(HeaderDataSchema, location="headers")
    @content_manager_bp.response(200, ReturnDataSchema)
    @validate_secret_key.validate_secret_key
    def post(self, header_data: HeaderData):
        
        response = ReturnData(
            status=200,
            message="Content Manager API is working",
            data=header_data.user
        )
        return response

@content_manager_bp.route("/delete")
class DeleteView(MethodView):
        @content_manager_bp.arguments(HeaderDataSchema, location="headers")
        @content_manager_bp.response(200, ReturnDataSchema)
        @validate_secret_key.validate_secret_key
        def delete(self, header_data: HeaderData):
            
            response = ReturnData(
                status=200,
                message="Content Manager API is working",
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

@content_manager_bp.route("/list")
class ListView(MethodView):
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