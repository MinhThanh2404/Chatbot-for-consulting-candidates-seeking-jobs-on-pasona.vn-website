import pymysql
from flask_sqlalchemy import SQLAlchemy

# Import models
# from models.search_model import SearchModel

db = SQLAlchemy()

def init_db(app):
    db_user = app.config.get("DB_USER")
    db_pass = app.config.get("DB_PASS")
    db_name = app.config.get("DB_NAME")
    db_host = app.config.get("DB_HOST")
    db_port = app.config.get("DB_PORT")
    
    # Connect to database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
