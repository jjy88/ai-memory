import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configuration
from config import config

# Import legacy blueprints
from upload_routes import upload_bp
from pay_routes import pay_bp
from chat_routes import chat_bp
from view_routes import view_bp

# Import new API
from api import api_bp

# Create Flask app
app = Flask(__name__)

# Load configuration
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize extensions
jwt = JWTManager(app)
CORS(app)

# Initialize rate limiter (skip if testing or Redis not available)
limiter = None
if not app.config.get('TESTING', False):
    try:
        limiter = Limiter(
            app=app,
            key_func=get_remote_address,
            storage_uri=app.config.get('RATELIMIT_STORAGE_URL'),
            default_limits=["200 per day", "50 per hour"]
        )
    except Exception as e:
        app.logger.warning(f"Rate limiter not initialized: {e}")

# Initialize Celery (if needed)
try:
    from tasks import init_celery
    celery = init_celery(app)
except Exception:
    celery = None

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

# Register blueprints - New API first
app.register_blueprint(api_bp)

# Legacy blueprints (for backward compatibility)
app.register_blueprint(upload_bp)
app.register_blueprint(pay_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(view_bp)

@app.route("/")
def index():
    return """
    <h2>欢迎来到 Obsi喵 🐾</h2>
    <p>API文档: <a href='/api/v1/docs'>/api/v1/docs</a></p>
    <p>传统接口: <a href='/pay'>/pay</a></p>
    """

@app.route("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config['DEBUG'])
