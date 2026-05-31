import time

def add_application_menu(tracker):
    company_name  = input ("Company Name: ").upper()
    job_title = input ("Jon Title: ").upper()
    date_applied = input ("Date Applied: ")
    job_url = input("Job URL: ")
    status = input("Status: ").upper()
    interview_date = input('Interivew Date: ')
    next_action = input("Next Action: ").upper()
    
    tracker.add_Application(
        company_name,
        job_title,
        date_applied,
        job_url,
        status,
        interview_date,
        next_action
    )
    
    print (f"${company_name} added succesfully!")

def search_application_menu(tracker):
    company_name = input ("Company Name: ").upper()
    job_title = input ("Job Title: ").upper()
    
    result = tracker.search_Application(company_name, job_title)
    
    if not result: 
        print(f"{company_name} : {job_title} NOT FOUND!")
        return
    
    print (*result, sep='\n')

def update_application_status_menu(tracker):
    company_name = input ("Company Name: ").upper()
    job_title = input("Job Title: ").upper()
    status = input ("New Status: ")
    
    tracker.update_Application_Status(company_name, job_title, status)
    
    print(f"{company_name} : {job_title} STATUS UPDATED SUCCESSFULLY")
    
def update_next_step_menu(tracker):
    company_name = input("Company Name: ").upper()
    job_title = input ("Job Title: ").upper()
    next_action = input("Next application stage (Interview, Under Review, Applied, etc.): ")

    
    if  not tracker.search_Application(company_name, job_title):
        print (f"{company_name} : {job_title} not found!")
        return 

    tracker.update_Next_Step(company_name, job_title, next_action)
    print (f"{company_name} : {job_title} application next step updated successfully!")

def update_interview_date_menu(tracker):
    company_name = input ("Company Name: ").upper()
    job_title = input ("Job Title: ").upper()
    interview_date = input("Enter Interview date (mm/dd/yyyy): ")
    
    if  not tracker.search_Application(company_name, job_title):
        print (f"{company_name} : {job_title} not found!")
        return 
    
    tracker.update_interview_date(company_name, job_title, interview_date)
    print (f"{company_name} : {job_title} interivew has been scheduled for {interview_date}.")
        
def list_application_by_status_menu(tracker):
    status = input ("Job Status: ").upper()
    
    result = tracker.list_Applications_By_Status(status)
    
    if not result:
        print(f"COULD NOT FIND ANYTHING WITH THE STAUTS: {status}")
        return 
    
    print(*result, sep='\n')
        
def search_application_by_company_menu(tracker):
    company_name = input ("Company Name: ").upper()
    
    result = tracker.search_Application_by_company(company_name)
    
    if not result:
        print(f"{company_name} NOT FOUND")
        return
    
    print(*result, sep='\n')

def display_up_coming_interivew_menu(tracker):
    result = tracker.display_up_Coming_Interviews()
    
    print(*result, sep='\n')
    
def display_All_Jobs_menu(tracker):
    result = tracker.display_All_Jobs()
    
    print(*result, sep='\n')

def remove_applications_menu(tracker):
    company_name = ""
    job_title = ""
    applications: list[dict] = []
    while True:
        company_name = input("Enter Company Name (or 'exit' to stop): ").upper()
        job_title = input("Enter Job Title (or 'exit' to stop: )").upper()
        
        if company_name == "EXIT" or job_title == "EXIT": 
            break
        
        if not tracker.search_Application(company_name, job_title):
            print(f"\033[31m❌ Company: {company_name} and Job title: {job_title} was not found!\033[0m")
        else:
            print(f"\033[32m✅ Queued Company: {company_name} and Job title: {job_title} for removal!\033[0m")        
            applications.append({
                "company_name" : company_name,
                "job_title": job_title
            })
    
    if not applications:
        print("\033[33mNo applications selected for removal.\033[0m")
        return
    
    confirm = input("\nAre you sure you want to remove these? (y/n): ").lower()
    
    if confirm != "y":
        print("\033[33mRemoval cancelled.\033[0m")
        return
    
    time.sleep(0.8)
    tracker.remove_Applications(applications)
    time.sleep(0.8)
    print ("\033[32m✅ PROCESS COMPELTE\033[0m")
        
        
        
            


def build_menue_options(tracker):
    return  {
        "1": ("Add Job Application", lambda: add_application_menu(tracker)),
        "2": ("Find Job Application", lambda: search_application_menu(tracker)),
        "3": ("Update Application Status", lambda: update_application_status_menu(tracker)),
        "4": ("Update Application Next Step", lambda: update_next_step_menu(tracker)),
        "5": ("Update Interview Date", lambda: update_interview_date_menu(tracker)),
        "6": ("Display All Application by status", lambda: list_application_by_status_menu(tracker)),
        "7": ("Find Application by Company", lambda: search_application_by_company_menu(tracker)),
        "8": ("Show up coming interviews", lambda: display_up_coming_interivew_menu(tracker)),
        "9": ("Show ALL Job Applications", lambda: display_All_Jobs_menu(tracker)),
        "10": ("Remove Job Application", lambda: remove_applications_menu(tracker)),
        "11": ("Add Login Info", tracker.add_Credential),
        "12": ("Find Login Info", tracker.search_Credential),
        "13": ("Update Login Info", tracker.update_Credentials),
        "14": ("Remove Login Info", tracker.remove_Credential),
        "15": ("Show ALL Login Credentials", tracker.display_credentials)
        
    }
    
def menue(MEUNE_OPTIONS):
    print("####### MENUE #######")
    time.sleep(0.08)
    
    for number, option in MEUNE_OPTIONS.items():
        label = option[0]
        print (f"{number}: {label}")
        
        time.sleep(0.08)