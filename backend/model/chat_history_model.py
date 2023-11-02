from utils.db import db
from sqlalchemy.sql import func

class chat_history(db.Model):
    """
    - store chat history of customers/users interacting with chatbot
    - params:
        + chat_id(int): auto generated
        + customer_id (int)
        + question (str): content of the message sent from customers
        + topic (str): main topic of the message (amount, salary, trivia)
        + response (str): query result
        + rating (int): def = 0 - not rating; 1: satisfied; 2: dissatified
        + created_at (dt): auto generated
    """
    chat_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.String(20), unique=False, nullable=True)
    question = db.Column(db.Text, unique=False, nullable=True)
    topic = db.Column(db.String(100), unique=False, nullable=True)
    keywords = db.Column(db.String(100), unique=False, nullable=True)
    response = db.Column(db.String(200), unique=False, nullable=True)
    rating = db.Column(db.SmallInteger, unique=False, nullable=True, default = 0)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
