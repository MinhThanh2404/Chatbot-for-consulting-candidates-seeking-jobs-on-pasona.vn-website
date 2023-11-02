from model.cust_info_model import cust_info
from utils.db import db
from sqlalchemy import update, text
from datetime import datetime as dt
import pdb


class CustService:
    @staticmethod
    def create_cust(cust_name, cust_email, cust_phone):
        """
        - Create a new customer record in the database
        - params:
            + cust_name (str)
            + cust_email (str)
            + cust_phone (str)
        """
        # print(name, email, phone)
        new_cust = cust_info(name=cust_name, email=cust_email, phone_no=cust_phone)
        db.session.add(new_cust)
        db.session.commit()
        return new_cust

    def update_existing_cust(cust_id, name, email, phone):
        """
        - update new customer contact info if it's changed
        - param:
            + cust_id (int): customer ID
            + name (str)
            + email (str)
            + phone (str)
        """
        update = cust_info.query.filter_by(customer_id=cust_id).first()
        update.name = name
        update.email = email
        update.phone_no = phone
        db.session.commit()
        return update

    def update_rating(cust_id, rating):
        """
        - update new customer contact info if it's changed
        - param:
            + cust_id (int): customer ID
            + rating (int)    
        """
        # update
        r = cust_info.query.filter_by(customer_id=cust_id).first()
        if r.rating == "0": #have never rated before
            r.rating = "(" + str(rating) + '|' + str(dt.now()) + ")"
        else: #have rated before
            r.rating += ', ('+str(rating) + '|' + str(dt.now()) + ")"
        db.session.commit()
        return r
