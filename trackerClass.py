import sqlite3
from datetime import datetime
import os
import base64
import hashlib
import hmac
from cryptography.fernet import Fernet, InvalidToken

ITERATIONS = 600_000

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
# USERNAME TEXT,
# ENCRYPTED_PASSWORD TEXT,
# JOB_URL TEXT

# ----------------
# MASTER_AUTH.db
# ----------------
# ID INTEGER PRIMARY KEY CHECK (ID = 1),
# SALT BLOB NOT NULL,
# MASTER_VERIFIER TEXT NOT NULL

    
    # Function to get the current date in the format mm/dd/YYYY
def get_current_date():
        date = datetime.now()
        formatted_date = date.strftime("%m/%d/%Y")
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
    def display_upcoming_Interviews(self):
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
    def display_all_Jobs(self):
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
                ENCRYPTED_PASSWORD TEXT,
                JOB_URL TEXT)
        """

        self.auth_cursor.execute(createAuthenticatorDB)
        self.auth_conn.commit()
        
        #ENCRYPTION FUNCTION
    def derive_encryption_key(self, master_password:str, salt: bytes) -> bytes:
        key = hashlib.pbkdf2_hmac("sha256", (master_password + ":encryption").encode("utf-8"), salt, ITERATIONS)
        
        return base64.urlsafe_b64encode(key)

        #encrypts password
    def encrypt_data(self, data: str, key:bytes) -> bytes:
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data.encode("utf-8"))
        return encrypted_data

        #Decodes the encrypted password
    def decrypt_data(self, encrypted_data:bytes, key:bytes) -> str:
        fernet=Fernet(key)
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
            return decrypted_data.decode("utf-8")
        except InvalidToken:
            raise ValueError("Invalid decryption token.")
    
    # ADD CREDENTIALS
    def add_credential(self, company_name:str, username:str, password_management:str, job_url:str, key: bytes):
        
        encrypted_password = self.encrypt_data(password_management, key)

        insertCredential = """
            INSERT INTO CREDENTIALS (COMPANY_NAME, USERNAME, ENCRYPTED_PASSWORD, JOB_URL)
            VALUES (?, ?, ?, ?)
        """

        self.auth_cursor.execute(insertCredential, (company_name, username, encrypted_password, job_url))
        self.auth_conn.commit()
    
    # FIND CREDENTIALS
    def search_Credential(self, company_name:str, username:str):
        findCredential = """
            SELECT * FROM CREDENTIALS WHERE COMPANY_NAME = ? AND USERNAME = ?
        """

        self.auth_cursor.execute(findCredential, (company_name, username))
        result = self.auth_cursor.fetchall()
        return result
    
    # REMOVE CREDENTIALS
    def remove_Credential (self, credentials: list[dict]):
        removeCredential = """
            DELETE FROM CREDENTIALS WHERE COMPANY_NAME = ? AND USERNAME = ?
        """

        values = [(cred["company_name"], cred["username"]) for cred in credentials]
        self.auth_cursor.executemany(removeCredential, values)
        self.auth_conn.commit()


    # Updates user login credentials 
    def update_Credentials (self, new_username:str, new_password:str, old_username:str, company_name:str, key:bytes):
        
        encrypted_pass  = self.encrypt_data(new_password, key)
        
        updateCredentials = """
            UPDATE CREDENTIALS 
                SET USERNAME = ?,
                ENCRYPTED_PASSWORD = ?
            WHERE COMPANY_NAME = ?
        """
        
        self.auth_cursor.execute(updateCredentials, (new_username, encrypted_pass, company_name))
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

                ###################### MASTER AUTHENTICATION DATABASE ######################
    #CREATES THE MASTER AUTH
    def create_Master_auth_DB(self):
        createMasterAuth = """
            CREATE TABLE IF NOT EXISTS MASTER_AUTH (
                ID INTEGER PRIMARY KEY CHECK (ID = 1),
                SALT BLOB NOT NULL,
                MASTER_VERIFIER TEXT NOT NULL
            )
        """
        self.auth_cursor.execute(createMasterAuth)
        self.auth_conn.commit()
    
    #FUNCTION TO HASH_PASSWORD
    def hash_password(self, master_pass:str, salt:bytes) -> str:
        hashedpass = hashlib.pbkdf2_hmac("sha256", (master_pass + ":verification").encode("utf-8"), salt, ITERATIONS) 
        
        return hashedpass.hex()
    
    #SEARCH THE MASTER AUTH DATABASE
    def search_master_auth(self):
        self.auth_cursor.execute("SELECT COUNT(*) FROM MASTER_AUTH")
        
        count = self.auth_cursor.fetchone()[0]
        
        return count > 0

    #VERIFTIES THE INCOMING PASSWORD IN THE DATABASE
    def verify_master_password(self, master_password:str) -> bool:
        self.auth_cursor.execute("SELECT SALT, MASTER_VERIFIER FROM MASTER_AUTH WHERE ID = 1")
        
        result = self.auth_cursor.fetchone()
        
        if result is None:
            return False
        
        salt, stored_verifier = result
        attempted_verifier = self.hash_password(master_password, salt)
        
        return hmac.compare_digest(attempted_verifier, stored_verifier)

    # Retrieves the salt from the database for some of the functions
    def get_master_salt(self):
        self.auth_cursor.execute("SELECT SALT FROM MASTER_AUTH WHERE ID = 1")
        
        result = self.auth_cursor.fetchone()
        
        if result is None:
            return None

        return result[0]
    
    
    #INSERTS AUTH MASTER PASSWORD
    def add_master_auth(self, master_password):
        if self.search_master_auth():
            print ("\033[31m❌ ACCOUNT ALREADY EXIST")
            return
        
        salt = os.urandom(16)
        
        MASTER_VERIFIER = self.hash_password(master_password, salt)
        
        insertMasterAuth = """
            INSERT INTO MASTER_AUTH (ID, SALT, MASTER_VERIFIER)
            VALUES(1, ? , ?)
        """
        
        self.auth_cursor.execute(insertMasterAuth, (salt, MASTER_VERIFIER))
        
        print ("\033[32m✅ ACCOUNT CREATED SUCCESSFULLY")
        
        self.auth_conn.commit()
        