from utils.db import db
from sqlalchemy.sql import func, text


class Verify:
    def verify_db(check_dict, table, expect_column):
        """
        - verify if the information has existed in the database or not. if existing, return yes; otherwise, return no
        - params:
            + check (dict):
                * key: column to check
                * value: info needs checking
            + table (str): name of table to check on
            + expect_column: what column value to return
        - return: True/False
        """
        cond = ""
        columns = ', '.join(list(check_dict.keys()))
        
        for key, value in check_dict.items():
            cond += f"{key} = '{value}' OR "
        sql = text(f'SELECT {expect_column} FROM {table} WHERE {cond[:-4]}')
        result = db.session.execute(sql) #execute the query
        result = result.mappings().all()
        if result:
            return result[0][f'{expect_column}']
        else: 
            return "new"
                    