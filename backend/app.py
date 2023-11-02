from flask import Flask
from flask_cors import CORS
from routes.chat import chat_bp
from routes.dashboard import dashboard_bp
from utils.db import init_db
from dotenv import load_dotenv
import os

load_dotenv('.env')

app = Flask(__name__)
CORS(app)

# Initialize database
app.config['DB_USER'] = os.getenv("DB_USER")
app.config['DB_PASS'] = os.getenv("DB_PASS")
app.config['DB_NAME'] = os.getenv("DB_NAME")
app.config['DB_HOST'] = os.getenv("DB_HOST")
app.config['DB_PORT'] = os.getenv("DB_PORT")
init_db(app)


# Register blueprint
app.register_blueprint(chat_bp)
app.register_blueprint(dashboard_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
