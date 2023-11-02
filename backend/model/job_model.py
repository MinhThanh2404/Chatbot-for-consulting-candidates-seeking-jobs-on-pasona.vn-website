from utils.db import db
from sqlalchemy.sql import func

class jobs(db.Model):
    """
    - store information about jobs
    - params:
        + id (int): auto generated
        + job_id (str): generated by Porters
        + job_posititon (str): job title
        + job_minsalary, job_maxsalary (int): USD (monthly?)
        + job_area, job_industry, job_category, job_category, job_other_language (str): code from Porters
        + job_area_name (str): geo location name
        + job_industry_name (str): industry (field) name
        + job_memo, job_category_summary (str): job desc
        + job_benefits (str)
        + job_type (str): fulltime/part-time...
        + job_holidays (str): when the employee can have a dayoff
        + job_phase (str): open/close
        + job_rank (str): S > A > B > C
        + job_update (dt): last time a section is updated
        + job_phase_date (dt): time close/open the job
        + is_hide (boolean): 1 - old job deleted from Porters database; 0 - existed job
        + job_education (str)
        + job_woking_hours (str):
        + job_area_summary (str): detail about the office address/workplace
    """

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    job_id = db.Column(db.String(255), unique=True, nullable=True)
    job_posititon = db.Column(db.String(255), unique=False, nullable=True)
    job_minsalary = db.Column(db.BigInteger, unique=False, nullable=True)
    job_maxsalary = db.Column(db.BigInteger, unique=False, nullable=True)
    job_area = db.Column(db.String(255), unique=False, nullable=True)
    job_area_name = db.Column(db.String(255), unique=False, nullable=True)
    job_industry = db.Column(db.String(255), unique=False, nullable=True)
    job_industry_name = db.Column(db.String(255), unique=False, nullable=True)
    job_memo = db.Column(db.Text, unique=False, nullable=True)
    job_category = db.Column(db.Text, unique=False, nullable=True)
    job_category_summary = db.Column(db.Text, unique=False, nullable=True)
    job_benefits = db.Column(db.Text, unique=False, nullable=True)
    job_type = db.Column(db.String(255), unique=False, nullable=True)
    job_holidays = db.Column(db.String(255), unique=False, nullable=True)
    job_phase = db.Column(db.String(255), unique=False, nullable=True)
    job_rank = db.Column(db.String(255), unique=False, nullable=True)
    job_other_language = db.Column(db.String(255), unique=False, nullable=True)
    job_update = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=True)
    job_phase_date = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=True)
    is_hide = db.Column(db.Boolean, default=0 , nullable=True)
    job_education = db.Column(db.Text, unique=False, nullable=True)
    job_woking_hours = db.Column(db.Text, unique=False, nullable=True)
    job_area_summary = db.Column(db.Text, unique=False, nullable=True)

