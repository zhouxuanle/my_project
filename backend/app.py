from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import logging
from config import Config
from utils import setup_proxy

# Setup proxy immediately to ensure all subsequent connections use it
setup_proxy()

from routes.auth import auth_bp
from routes.data import data_bp
from routes.jobs import jobs_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
JWTManager(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(data_bp)
app.register_blueprint(jobs_bp)

if __name__ == '__main__':
    app.run(debug=True)
