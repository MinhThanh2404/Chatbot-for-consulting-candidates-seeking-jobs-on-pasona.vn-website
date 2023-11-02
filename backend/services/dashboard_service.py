from model.chat_history_model import chat_history
from model.cust_info_model import cust_info
from utils.db import db
from sqlalchemy import select, text
import pandas as pd
from datetime import datetime
import json
import traceback

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(self, o)


class DashboardService:
    @staticmethod
    
    def get_data(time_type, visual_name):
        """
        - interact with the database via the query text to collect the data for the visualization
        - params: time_type (str), visual_name (str)
        - return: data (list)
        """
        def convert_timetype(time_type):
            match time_type.lower():
                case 'today':
                    return {'date': 'DATE', 'year': False}
                case 'month' | 'week' | 'quarter':
                    return {'date':time_type.upper(), 'year': True}
                case 'year':
                    return {'date': time_type.upper(), 'year': False}
                case 'all':
                    return {'date': "", 'year': False}
        
        query = ""
        year_col = ""
        time_ = convert_timetype(time_type)['date']
        match visual_name:
            case 'total_users' | 'total mes' | 'topic_dist' | 'topic_realtime' | 'wordcloud_chat' | 'chat_data':
                year_col = 'created_at'
                year = f'AND YEAR({year_col}) = YEAR(CURDATE())' if convert_timetype(time_type)['year'] else ""
                query = f'SELECT * FROM chat_history WHERE {time_}({year_col}) = {time_}(CURDATE()) {year}' if time_type !='all' \
                    else f'SELECT * FROM chat_history'

            case 'total_search' | 'search_option' | 'topic_realtime' | 'search_KPI' | 'where_search' | 'search_keyword' | 'search_location' | 'salary' | 'language' | 'industry' | 'jobsearch_data':
                year_col = 'search_time'
                year = f'AND YEAR({year_col}) = YEAR(CURDATE())' if convert_timetype(time_type)['year'] else ""
                query = f'SELECT * FROM job_search WHERE {time_}({year_col}) = {time_}(CURDATE()) {year}' if time_type !='all' \
                    else f'SELECT * FROM job_search'
            
            case 'new_customers':
                year_col = 'chat_history.created_at'
                year = f'AND YEAR({year_col}) = YEAR(CURDATE())' if convert_timetype(time_type)['year'] else ""
                query = f'SELECT DISTINCT cust_info.* \
                    FROM cust_info LEFT JOIN chat_history ON cust_info.customer_id = chat_history.customer_id LEFT JOIN job_search ON chat_history.customer_id = job_search.cust_id \
                        WHERE ( {time_}(cust_info.updated_at) = {time_}(CURDATE()) ) \
                            AND ( ( {time_}({year_col}) = {time_}(CURDATE()) ) OR ( {time_}(job_search.search_time) = {time_}(CURDATE()) ) ) {year}'

            case 'rentation':
                year_col = 'chat_history.created_at'
                year = f'AND YEAR({year_col}) = YEAR(CURDATE())' if convert_timetype(time_type)['year'] else ""
                query = f'SELECT DISTINCT cust_info.* \
                    FROM cust_info LEFT JOIN chat_history ON cust_info.customer_id = chat_history.customer_id LEFT JOIN job_search ON chat_history.customer_id = job_search.cust_id \
                        WHERE ( {time_}(cust_info.updated_at) < {time_}(CURDATE()) ) \
                            AND (({time_}({year_col}) = {time_}(CURDATE())) OR ({time_}(job_search.search_time) = {time_}(CURDATE()) ) ) {year}'
                                
            case 'rating' | 'satisfaction' | 'cust_info':
                year_col = 'rating_table.timestamp_'
                year = f'AND YEAR({year_col}) = YEAR(CURDATE())' if convert_timetype(time_type)['year'] else ""
                query = f"SELECT * \
                    FROM\
                        (\
                            SELECT cust_info.customer_id, cust_info.email, cust_info.phone_no, cust_info.name, \
                                REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(cust_info.rating,',',num.n),'|',1),'(','') as rating,\
                                REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(cust_info.rating, ',', num.n), '|', -1),')','') as timestamp_,\
                                cust_info.updated_at \
                            FROM (SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5) num \
                                INNER JOIN cust_info ON CHAR_LENGTH(cust_info.rating) - CHAR_LENGTH(REPLACE(cust_info.rating,',','')) >= num.n -1 \
                                    ORDER BY cust_info.customer_id) rating_table \
                    WHERE {time_}({year_col}) = {time_}(CURDATE()) {year}" if time_type !='all' \
                    else f"SELECT * \
                    FROM\
                        (\
                            SELECT cust_info.customer_id, cust_info.email, cust_info.phone_no, cust_info.name, \
                                REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(cust_info.rating,',',num.n),'|',1),'(','') as rating,\
                                REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(cust_info.rating, ',', num.n), '|', -1),')','') as timestamp_,\
                                cust_info.updated_at \
                            FROM (SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5) num \
                                INNER JOIN cust_info ON CHAR_LENGTH(cust_info.rating) - CHAR_LENGTH(REPLACE(cust_info.rating,',','')) >= num.n -1 \
                                    ORDER BY cust_info.customer_id) rating_table"
                # SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5: the n is the total of ratings a single customer can have in your dataset.
        result = db.session.execute(text(query)) #execute the query
        result = result.mappings().all()
        print(result)
        # Convert data to JSON using the custom encoder
        df = pd.DataFrame.from_dict(result). astype(str) #convert to dataframe, convert data type of columns to string
        json_data = df.to_json(orient='records', date_format='iso')

        print(time_type,':',json_data)
        return json_data
    