

import requests
import ast
import sqlite3
from datetime import datetime


class JenkinsJobDB(object):
    
    def db_name(self):
        return 'jenkins'
        
    def get_db_connection(self):
        '''Connect to an existing sqlite database or create one, if it doesnt exist'''
        conn = sqlite3.connect('jenkins.db')
        self.create_db_table(conn)
        return conn
    
    def create_db_table(self, db_conn):
        '''Create jenkins_job table in database'''
        try:
            create_table_statement = '''CREATE TABLE jenkins_job (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name TEXT NOT NULL, status TEXT NOT NULL, checked_date DATETIME NOT NULL);''' 
            db_conn.execute(create_table_statement)
        except:
            pass
        
    def insert_job_values_in_db(self, db_conn, job_name, job_status, date):
        '''Insert job information in table jenkins_job'''
        db_conn.execute("INSERT INTO jenkins_job (name, status, checked_date) \
                         VALUES (?, ?, ?)", (job_name, job_status, date));
        
    
    def is_jobname_in_db(self, db_conn, job_name):
        '''Check if job exists in database to avoid duplicates'''        
        result = db_conn.execute("SELECT * from jenkins_job where name='" + job_name + "'")
        all_result = result.fetchall()
        return len(all_result) > 0
    
    def get_all_jobs(self):
        '''Get all jobs in table jenkins_job'''
        db_conn = self.get_db_connection()
        result = db_conn.cursor().execute("select * from jenkins_job")
        return result.fetchall()
        
        
class JenkinsJob(object):
    '''Jenkins Class for any given instance with url, username and password'''
    def __init__(self, jenkins_url, username, password):
        self.jenkins_url = jenkins_url
        self.username    = username
        self.password    = password
        self.db_conn     = JenkinsJobDB()
        
        
    def get_jobs(self):
        '''Get all jenkins jobs'''
        r = requests.get(jenkins_url, auth=(username, password), stream=True)
        job_list_json = ast.literal_eval(r.text)
        return job_list_json['jobs']
    
    def get_jobs_in_db(self):
        '''Get all saved jobs in database table jenkins_job'''
        return self.db_conn.get_all_jobs()
            
    
    def eval_job_status(self, color):
        '''
        Evaluate Job status:
        assume blue=successful; red=failure; None=unknown
        '''
        job_colors = {'blue': 'successful', 'red': 'failure', 'None': 'unknown'}
        return job_colors.get(color)
        
    
    def save_job_info(self):
        '''Save job information in database table jenkins_job'''
        db_conn = self.db_conn.get_db_connection()
        jobs   = self.get_jobs()
        for index,job in enumerate(jobs):
            job_name  = job.get('name')
            
            '''Check if job exists in db'''
            check_job = self.db_conn.is_jobname_in_db(db_conn, job_name)
            if not check_job:                
                job_color = str(job.get('color')) #covert to string for None values
                '''Evaluate jpb status using its color'''
                job_status = self.eval_job_status(job_color)
                date       = datetime.now()
                self.db_conn.insert_job_values_in_db(db_conn, job_name, job_status, date)
        
        '''Commit data and close database connection'''
        db_conn.commit()
        db_conn.close()
    

'''Test Account credentials for a Jenkins instance using Python API'''
jenkins_url = 'http://localhost:8080/api/python?pretty=true&tree=jobs[name, color]'
username    = 'ajirapsy'
password    = 'developer'

jenkins_job = JenkinsJob(jenkins_url, username, password)

jenkins_job.save_job_info()

'''Print jobs in database to verify'''
print jenkins_job.get_jobs_in_db()