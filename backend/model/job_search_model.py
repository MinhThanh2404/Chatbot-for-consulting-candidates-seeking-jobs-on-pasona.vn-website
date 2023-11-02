from utils.db import db
from sqlalchemy.sql import func

class job_search(db.Model):
    """
    - store job search history both from the chatbot and on Job Search page
    - params:
        + id (int): auto generated
        + cust_id (str) : unique identifier of a user who has searched for jobs in the chatbot, if from the Job Search page --> null
        + keyword (str): related to industry, typed
        + industry (str): multiple choice
        + language (str): main language used in job
        + location (str): multiple choice
        + salary (str): multiple
        + search_time (dt): auto generated
    """

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    cust_id = db.Column(db.BigInteger, unique=False, nullable=True)
    keyword = db.Column(db.String(200), unique=False, nullable=True)
    industry = db.Column(db.String(200), unique=False, nullable=True)
    language = db.Column(db.String(255), unique=False, nullable=True)
    location = db.Column(db.String(255), unique=False, nullable=True)
    salary = db.Column(db.String(255), unique=False, nullable=True)
    search_time = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=True)
    #is_jobpage = db.Column(db.Boolean, default=1, unique=False, nullable=True)


