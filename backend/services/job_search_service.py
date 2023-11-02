from model.job_search_model import job_search
from utils.db import db
from model.job_model import jobs
from utils.db import db
from sqlalchemy import select, text

class SearchService:
    @staticmethod
    def create_search(customer_id, keyword, industry, language, location, salary):
        new_search = job_search(cust_id=customer_id, keyword=keyword, industry=industry,
                                 language=language, location=location, salary=salary)
        db.session.add(new_search)
        db.session.commit()
        return new_search
    
#     def get_job(keyword, industry, language, location, salary):
#         area = text(f'SELECT DISTINCT job_area_name FROM jobs')
#         area_query = db.session.execute(area)
#         area_list = [row.job_area_name for row in area_query]
#         if location in area_list:
#             sql = text(f'SELECT * FROM jobs WHERE job_posititon LIKE "%{keyword}%" AND  job_industry_name LIKE "%{industry}%" AND job_other_language LIKE "%{language}%" AND job_area_name LIKE "%{location}%" AND job_minsalary >= {salary} AND job_phase LIKE "%open%" ORDER BY job_update, CASE WHEN job_rank = "S" THEN 1 WHEN job_rank = "A" THEN 2 WHEN job_rank = "B" THEN 3 ELSE 4 END LIMIT 10;')
#         else:
#             sql = text(f'SELECT * FROM jobs WHERE job_posititon LIKE "%{keyword}%" AND  job_industry_name LIKE "%{industry}%" AND job_other_language LIKE "%{language}%" AND job_area_summary LIKE "%{location}%" AND (job_area_summary LIKE "%OTHER%" OR job_area_summary LIKE "%FOREIGN%") AND job_minsalary >= {salary} AND job_phase LIKE "%open%" ORDER BY job_update, CASE WHEN job_rank = "S" THEN 1 WHEN job_rank = "A" THEN 2 WHEN job_rank = "B" THEN 3 ELSE 4 END LIMIT 10;')

#         #call API
#         result = db.session.execute(sql) #execute the query
#         data = [{'id': row.id, 'title': row.job_posititon} for row in result] #convert the result to list

#         return data
