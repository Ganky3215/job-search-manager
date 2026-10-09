import time

class ExitPrompt(Exception):
    pass


def ask(prompt, transform=None):
    value = input(prompt).strip()
    
    if value.lower() in ("exit", "cancel", "q"):
        raise ExitPrompt

    if transform:
        return transform(value)

    return value

def show_exit_hint():
    print("\033[32mYOU CAN TYPE 'exit' ANYTIME TO STOP!\033[0m")
    time.sleep(0.8)


####################################### APPLICATION MENUE #######################################


def add_application_menu(tracker):
    show_exit_hint()
    try:
        company_name  = ask ("Company Name: ", str.upper)
        job_title = ask ("Job Title: ", str.upper)
        date_applied = ask ("Date Applied (YYYY/MM): ")
        job_url = ask("Job URL: ")
        status = ask("Status: ", str.upper)
        interview_date = ask('Interview Date: ')
        next_action = ask("Next Action: ", str.upper)

        result = tracker.search_Application(company_name, job_title)

        if result:
            print (f"You have already applied to {company_name} for {job_title}")
            return 
        
        tracker.add_Application(
            company_name,
            job_title,
            date_applied,
            job_url,
            status,
            interview_date,
            next_action
        )
        
        print (f"{company_name} added successfully!")
    except ExitPrompt:
        print("\033[33mEXITING APPLICATION INSERTION.\033[0m")

def search_application_menu(tracker):
    show_exit_hint()
    
    try:
        
        company_name = ask ("Company Name: ", str.upper)
        job_title = ask ("Job Title: ", str.upper)
        
        result = tracker.search_Application(company_name, job_title)
        
        if not result: 
            print(f"{company_name} : {job_title} NOT FOUND!")
            return
        
        print (*result, sep='\n')
    
    except ExitPrompt:
        print("\033[33mEXITING APPLICATION SEARCHING.\033[0m")

def update_application_status_menu(tracker):
    show_exit_hint()
    try:
        company_name = ask ("Company Name: ", str.upper)
        job_title = ask("Job Title: ", str.upper)
        status = ask ("New Status: ")

        result = tracker.search_Application(company_name, job_title)

        if not result:
            print(f"{company_name} : {job_title} NOT FOUND.")
            return
        
        tracker.update_Application_Status(company_name, job_title, status)
        
        print(f"{company_name} : {job_title} STATUS UPDATED SUCCESSFULLY")
    
    except ExitPrompt:
        print("\033[33mEXITING APPLICATION UPDATE.\033[0m")
    
def update_next_step_menu(tracker):
    show_exit_hint()
    
    try:
        company_name = ask("Company Name: ", str.upper)
        job_title = ask ("Job Title: ", str.upper)
        next_action = ask("Next application stage (Interview, Under Review, Applied, etc.): ")

        
        if  not tracker.search_Application(company_name, job_title):
            print (f"{company_name} : {job_title} not found!")
            return 

        tracker.update_Next_Step(company_name, job_title, next_action)
        print (f"{company_name} : {job_title} application next step updated successfully!")
        
    except ExitPrompt:
        print("\033[33mEXITING NEXT-STEP UPDATE.\033[0m")    
        
        
def update_interview_date_menu(tracker):
    show_exit_hint()
    
    try:
        company_name = ask ("Company Name: ", str.upper)
        job_title = ask("Job Title: ", str.upper)
        interview_date = ask("Enter Interview date (mm/dd/yyyy): ")
        
        if  not tracker.search_Application(company_name, job_title):
            print (f"{company_name} : {job_title} not found!")
            return 
        
        tracker.update_interview_date(company_name, job_title, interview_date)
        print (f"{company_name} : {job_title} Interview has been scheduled for {interview_date}.")
    
    except ExitPrompt:
        print("\033[33mEXITING INTERVIEW-DATE UPDATE.\033[0m")
        
def list_application_by_status_menu(tracker):
    show_exit_hint()
    try:
        status = ask("Job Status: ", str.upper)
        
        result = tracker.list_Applications_By_Status(status)
        
        if not result:
            print(f"COULD NOT FIND ANYTHING WITH THE STATUS: {status}")
            return 
        
        print(*result, sep='\n')
    except ExitPrompt:
        print("\033[33mEXITING APPLICATION LISTING BY STATUS.\033[0m")
        
def search_application_by_company_menu(tracker):
    show_exit_hint()
    
    try:
        company_name = ask("Company Name: ", str.upper)
        
        result = tracker.search_Application_by_company(company_name)
        
        if not result:
            print(f"{company_name} NOT FOUND")
            return
        
        print(*result, sep='\n')
        
    except ExitPrompt:
        print("\033[33mEXITING APPLICATION SEARCHING BY COMPANY.\033[0m")
          
def display_upcoming_Interview_menu(tracker):
    result = tracker.display_upcoming_Interviews()
    
    print(*result, sep='\n')
    
def display_all_Jobs_menu(tracker):
    result = tracker.display_all_Jobs()
    
    print(*result, sep='\n')

def remove_applications_menu(tracker):
    show_exit_hint()
    applications: list[dict] = []
    
    while True:
        try:
            company_name = ask("Enter Company Name (or 'exit' to stop): ", str.upper)
            job_title = ask("Enter Job Title (or 'exit' to stop: )", str.upper)
            
            if not tracker.search_Application(company_name, job_title):
                print(f"\033[31m❌ Company: {company_name} and Job title: {job_title} was not found!\033[0m")
            else:
                print(f"\033[32m✅ Queued Company: {company_name} and Job title: {job_title} for removal!\033[0m")        
                applications.append({
                    "company_name" : company_name,
                    "job_title": job_title
                })
        except ExitPrompt:
            print("\033[33mEXITING APPLICATION REMOVAL.\033[0m")
            break
    
    if not applications:
        print("\033[33mNo applications selected for removal.\033[0m")
        return
    
    confirm = input("\nAre you sure you want to remove these? (y/n): ").strip().lower()
    
    if confirm != "y":
        print("\033[33mRemoval cancelled.\033[0m")
        return
    
    time.sleep(0.8)
    tracker.remove_Applications(applications)
    time.sleep(0.8)
    print ("\033[32m✅ PROCESS COMPLETE\033[0m")
    
    
####################################### CREDENTIALS MENUE #######################################

def add_credentials_menu(tracker, key):
    show_exit_hint()
    try:
        company_name = ask ("Enter Company Name: ", str.upper)
        user_name = ask("Enter username: ")
        password = ask("Enter password used:")
        job_url = ask("Enter Job application URL")
        
        
        tracker.add_credential(company_name, user_name, password, job_url,key)
        
    except ExitPrompt:
        print("\033[33mEXITING CREDENTIAL INSERTION.\033[0m")

def search_Credential_menue(tracker):
    show_exit_hint()
    
    try:
        company_name = ask("Enter Company Name: ", str.upper)
        user_name = ask("Enter User Name: ")
        result = tracker.search_Credential(company_name, user_name)

        if not result:
            print(f"No credentials found for {company_name}.")
            return 

        print(*result, sep='\n')

    except ExitPrompt:
        print("\033[33mEXITING CREDENTIAL SEARCH.\033[0m")
    
def update_Credentials_menue(tracker, key):
    show_exit_hint()
    
    try:
        old_username = ask("Enter old username: ")
        new_username = ask("Enter NEW username: ")
        new_password = ask("Enter NEW password: ")
        company_name = ask ("Enter Company name to change Credentials for: ", str.upper)

        tracker.update_Credentials(new_username, new_password, old_username, company_name, key)
    except ExitPrompt:
        print("\033[33mEXITING CREDENTIALS UPDATE.\033[0m")

def remove_credentials_menue(tracker):
    show_exit_hint()
    
    credentials: list[dict] = []
    
    while True:
        try:
            company_name = ask("Enter Company Name: ", str.upper)
            user_name = ask("Enter username used: ")
            
            if not tracker.search_Credential(company_name, user_name):
                 print(f"\033[31m❌ Company: {company_name} with {user_name} was not found!\033[0m")
            else:
                print(f"\033[32m✅ Queued Credentials for Company: {company_name} for removal!\033[0m")    
                credentials.append({
                    "company_name" : company_name,
                    "username": user_name
                })    
        except ExitPrompt:
            print("\033[33mEXITING CREDENTIAL REMOVAL.\033[0m")
            break
    
    if not credentials:
        print("\033[33mNo credentials were selected for removal.\033[0m")
        return
    
    confirm = input("\nAre you sure you want to remove these? (y/n): ").strip().lower()
    
    if confirm != "y":
        print("\033[33mRemoval cancelled.\033[0m")
        return
    
    time.sleep(0.8)
    tracker.remove_Credential(credentials)
    time.sleep(0.8)
    print ("\033[32m✅ PROCESS COMPLETE\033[0m")

def display_credentials_menue(tracker):
    result = tracker.display_credentials()
    
    print(*result, sep='\n')
    
def build_menu_options(tracker, key):
    return  {
        "1": ("Add Job Application", lambda: add_application_menu(tracker)),
        "2": ("Find Job Application", lambda: search_application_menu(tracker)),
        "3": ("Update Application Status", lambda: update_application_status_menu(tracker)),
        "4": ("Update Application Next Step", lambda: update_next_step_menu(tracker)),
        "5": ("Update Interview Date", lambda: update_interview_date_menu(tracker)),
        "6": ("Display All Application by status", lambda: list_application_by_status_menu(tracker)),
        "7": ("Find Application by Company", lambda: search_application_by_company_menu(tracker)),
        "8": ("Show up coming interviews", lambda: display_upcoming_Interview_menu(tracker)),
        "9": ("Show ALL Job Applications", lambda: display_all_Jobs_menu(tracker)),
        "10": ("Remove Job Application", lambda: remove_applications_menu(tracker)),
        "11": ("Add Login Info", lambda: add_credentials_menu(tracker, key)),
        "12": ("Find Login Info", lambda: search_Credential_menue(tracker)),
        "13": ("Update Login Info", lambda: update_Credentials_menue(tracker, key)),
        "14": ("Remove Login Info", lambda: remove_credentials_menue(tracker)),
        "15": ("Show ALL Login Credentials", lambda: display_credentials_menue(tracker))
        
    }
    
def menu(MENU_OPTIONS):
    print("####### MENU #######")
    time.sleep(0.08)
    
    for number, option in MENU_OPTIONS.items():
        label = option[0]
        print (f"{number}: {label}")
        time.sleep(0.08)