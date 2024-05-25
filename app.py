from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from src.blueprints.content_manager import content_manager_bp

app = Flask(__name__)
app.config['API_TITLE'] = 'Content Management System API' 
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

api.register_blueprint(content_manager_bp)

if __name__ == '__main__':
    app.run(debug=True)