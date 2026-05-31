import sqlite3
from datetime import datetime

# ----------------
# APPLICATIONS.db
# ----------------
# ID PRIMARY KEY,
# COMPANY_NAME TEXT NOT NULL,
# JOB_TITLE TEXT NOT NULL,
# DATE_APPLIED TEXT NOT NULL,
# JOB_URL TEXT,
# STATUS TEXT NOT NULL,
# INTERVIEW_DATE TEXT NOT NULL,
# NEXT_ACTION TEXT

# ----------------
# AUTHENTICATOR.db
# ----------------
# ID PRIMARY KEY,
# COMPANY_NAME TEXT NOT NULL,
# USERAME TEXT,
# PASSWORD_MANAGEMENT TEXT,
# JOB_URL TEXT

    
    # Function to get the current date in the format YYYY/MM/DD
def get_current_date():
        date = datetime.now()
        formatted_date = date.strftime("%Y/%m/%d")
        return formatted_date


class job_tracker:
    def __init__ (self, application:str = "applications.db", authenticator:str = "credential.db"):
        self.app_conn = sqlite3.connect(application)
        self.auth_conn = sqlite3.connect(authenticator)

        self.app_cursor = self.app_conn.cursor()
        self.auth_cursor = self.auth_conn.cursor()

                ###################### APPLICATION DATABASE ######################

    # CREATE APPLICATION DB
    def create_Application_DB(self):
        createApplicationDB = """
            CREATE TABLE IF NOT EXISTS JOB_APP (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                COMPANY_NAME TEXT NOT NULL,
                JOB_TITLE TEXT NOT NULL,
                DATE_APPLIED TEXT NOT NULL,
                JOB_URL TEXT,
                STATUS TEXT NOT NULL,
                INTERVIEW_DATE TEXT,
                NEXT_ACTION TEXT)
        """

        self.app_cursor.execute(createApplicationDB)
        self.app_conn.commit()
    
    # ADD JOB APPLICATIONS
    def add_Application(self, company_name:str, job_title:str, date_applied:str, job_url:str, status:str, interview_date:str, next_action:str):
        insertApplication = """
            INSERT INTO JOB_APP (COMPANY_NAME, JOB_TITLE, DATE_APPLIED, JOB_URL, STATUS, INTERVIEW_DATE, NEXT_ACTION)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        interview_date  = interview_date if len(interview_date) > 0 else None
        next_action = next_action if len(next_action) > 0 else None
        self.app_cursor.execute(insertApplication, (company_name, job_title, date_applied, job_url, status, interview_date, next_action))
        self.app_conn.commit()
    
    # FIND JOB APPLICATIONS
    def search_Application(self, company_name:str, job_title:str):
        searchApplication = """
            SELECT * FROM JOB_APP WHERE COMPANY_NAME = ? AND JOB_TITLE = ?
        """

        self.app_cursor.execute(searchApplication, (company_name, job_title))
        result = self.app_cursor.fetchall()
        return result
    
    # FIND JOB APPLICATION BY COMPANY
    def search_Application_by_company(self, company_name:str):
        searchApplicationByCompany = """
            SELECT * FROM JOB_APP WHERE COMPANY_NAME = ?
        """
    
        self.app_cursor.execute(searchApplicationByCompany, (company_name,))
        result = self.app_cursor.fetchall()
        return result

    
    # REMOVE JOB APPLICATIONS
    def remove_Applications (self, applications: list[dict]):
        removeApplication = """
            DELETE FROM JOB_APP WHERE COMPANY_NAME = ? AND JOB_TITLE = ?
        """

        values = [(app["company_name"], app["job_title"])
                    for app in applications]
        
        self.app_cursor.executemany(removeApplication, values)
        self.app_conn.commit()
        
    # UPDATE APPLICATION STATUS
    def update_Application_Status(self, company_name:str, job_title:str, new_status:str):
        updateStatus = """
            UPDATE JOB_APP SET STATUS = ? WHERE COMPANY_NAME = ? AND JOB_TITLE = ?
        """

        self.app_cursor.execute(updateStatus, (new_status, company_name, job_title))
        self.app_conn.commit()
    
    # List all job applications with a specific status
    def list_Applications_By_Status (self, status:str):
        listByStatus = """
            SELECT * FROM JOB_APP WHERE STATUS LIKE ?
        """

        self.app_cursor.execute(listByStatus, (f"%{status}%",))
        result = self.app_cursor.fetchall()
        return result

    # Find all up coming interview
    def display_up_Coming_Interviews(self):
        upcoming_interviews = """
            SELECT * FROM JOB_APP WHERE INTERVIEW_DATE IS NOT NULL
                    AND INTERVIEW_DATE >= ? 
                ORDER BY INTERVIEW_DATE ASC
        """

        current_date = get_current_date()
        self.app_cursor.execute(upcoming_interviews, (current_date,))
        result = self.app_cursor.fetchall()
        return result

    # Updates the next step for a job
    def update_Next_Step(self, company_name:str, job_title:str, next_action:str):
        Next_Step = """
            UPDATE JOB_APP
                SET NEXT_ACTION = ?
            WHERE COMPANY_NAME = ?
                AND JOB_TITLE = ?
        """
        self.app_cursor.execute(Next_Step, (next_action, company_name, job_title))
        self.app_conn.commit()

    # Updates the interview_date
    def update_interview_date(self, company_name:str, job_title:str, new_interview_date:str):
        interview_date = """
            UPDATE JOB_APP
                SET INTERVIEW_DATE = ?
            WHERE COMPANY_NAME = ?
                AND JOB_TITLE = ? 
        """
        self.app_cursor.execute(interview_date, (new_interview_date, company_name, job_title))
        self.app_conn.commit()
        
    
    # Display all Jobs 
    def display_All_Jobs(self):
        display_Jobs = """
            Select * from JOB_APP
        """
        self.app_cursor.execute(display_Jobs)
        results = self.app_cursor.fetchall()
        return results

                ###################### AUTHENTICATION DATABASE ######################

    # CREATE CREDENTIALS DB
    def create_Authenticator_DB(self):
        createAuthenticatorDB = """
            CREATE TABLE IF NOT EXISTS CREDENTIALS (
                ID INTEGER  PRIMARY KEY AUTOINCREMENT,
                COMPANY_NAME TEXT NOT NULL,
                USERNAME TEXT,
                PASSWORD_MANAGEMENT TEXT,
                JOB_URL TEXT)
        """

        self.auth_cursor.execute(createAuthenticatorDB)
        self.auth_conn.commit()
    

    # ADD CREDENTIALS
    def add_Credential(self, company_name:str, username:str, password_management:str, job_url:str):
        insertCredential = """
            INSERT INTO CREDENTIALS (COMPANY_NAME, USERNAME, PASSWORD_MANAGEMENT, JOB_URL)
            VALUES (?, ?, ?, ?)
        """

        self.auth_cursor.execute(insertCredential, (company_name, username, password_management, job_url))
        self.auth_conn.commit()
    
    # FIND CREDENTIALS
    def search_Credential(self, company_name:str):
        findCredential = """
            SELECT * FROM CREDENTIALS WHERE COMPANY_NAME = ?
        """

        self.auth_cursor.execute(findCredential, (company_name,))
        result = self.auth_cursor.fetchall()
        return result
    
    # REMOVE CREDENTIALS
    def remove_Credential (self, company_name: str, username: str):
        removeCredential = """
            DELETE FROM CREDENTIALS WHERE COMPANY_NAME = ? AND USERNAME = ?
        """

        self.auth_cursor.execute(removeCredential, (company_name, username))
        self.auth_conn.commit()


    # Updates user login credentials 
    def update_Credentials (self, new_username:str, new_password:str, company_name:str):
        updateCredentials = """
            UPDATE CREDENTIALS 
                SET USERNAME = ?,
                PASSWORD_MANAGEMENT = ?
            WHERE COMPANY_NAME = ?
        """
        
        self.auth_cursor.execute(updateCredentials, (new_username, new_password, company_name))
        self.auth_conn.commit()

    # Display all credtials
    def display_credentials(self):
        display_cred = """
            SELECT * FROM CREDENTIALS
        """
        self.auth_cursor.execute(display_cred)
        results = self.auth_cursor.fetchall()
        return results

    # USED to close the database
    def close_Database(self):
        self.app_conn.close()
        self.auth_conn.close()