from utils.db import db
from sqlalchemy.sql import func

class cust_info(db.Model):
    """
    - store customer contact information and their rating on overall experience with chatbot
    - params:
        + customer_id (int): auto generated
        + email (str): unique
        + name (str)
        + phone_no (str): unique
        + rating (text): def = 0 (not rating); format: {rating scale | time;...}; scale 1-5 (1: very disappointed, 5: very satisfied)
        + updated_at (dt): auto generated
    """
    customer_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), unique=True, nullable=True)
    name = db.Column(db.String(200), unique=False, nullable=True)
    phone_no = db.Column(db.String(20), unique=True, nullable=True)
    rating = db.Column(db.Text, unique=False, nullable=True, default = 0)
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=True)