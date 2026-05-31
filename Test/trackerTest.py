from trackerClass import job_tracker

        ###################### HELPER FUNCTION ######################

# HELPER FUNCTION TO ADD APPLICAITONS
def add_application_helper(t):
    t.add_Application(
        "OpenAI",
        "Software Engineer",
        "2026/03/18",
        "https://example.com/openai",
        "Applied",
        "2026/03/25",
        "Wait for recruiter")

# HELPER FUNCTION TO ADD MULTIPLE JOB APPLICAITONS
def add_mult_app_helper(t):
    t.add_Application(
        "OPENAI",
        "SOFTWARE ENGINEER",
        "2026/03/18",
        "https://example.com/openai",
        "Applied",
        "2026/03/25",
        "Wait for recruiter")
    t.add_Application(
        "GOOGLE",
        "SOFTWARE ENGINEER",
        "2026/03/26",
        "https://example.com/google",
        "Round 2 interview",
        "",
        "Wait for recruiter")
    t.add_Application(
        "META",
        "SOFTWARE ENGINEER",
        "2026/05/15",
        "https://example.com/meta",
        "Round 1 interview",
        "",
        "Wait for recruiter")
    t.add_Application(
        "GOOGLE",
        "SOFTWARE ENGINEER II",
        "2026/05/15",
        "https://example.com/meta",
        "Round 1 interview",
        "",
        "Wait for recruiter")
    
# HELPER FUNCTION TO ADD CREDENTIALS
def add_credential_helper(t):
    t.add_Credential(
        "OpenAI",
        "benxiang3215@gmail.com",
        "Testing1111",
        "https://example.com/openai"
    )

def add_mult_cred_helper(t):
    t.add_Credential(
        "OpenAI",
        "benxiang3215@gmail.com",
        "Testing1111",
        "https://example.com/openai"
    )
    t.add_Credential(
        "Google",
        "benxiang3215@gmail.com",
        "Googletest3215",
        "https://example.com/google"
    )
    t.add_Credential(
        "Lockheed Martin",
        "benxiang3215@gmail.com",
        "Googletest3215",
        "https://example.com/google"
    )
    
# HELPER FUNCTION TO CREATE TEMPORARY MEMORY TO DATABASE
def make_Tracker():
    t = job_tracker(":memory:", ":memory:")
    t.create_Application_DB()
    t.create_Authenticator_DB()
    return t

            ###################### TESTING APPLICATION DATABASE ######################

def test_add_and_search_application():
    t = make_Tracker()
    add_application_helper(t)
    
    result = t.search_Application("OpenAI", "Software Engineer")
    assert len(result) == 1
    assert result[0][1] == "OpenAI"
    assert result[0][2] == "Software Engineer"
    assert result[0][3] == "2026/03/18"
    assert result[0][5] == "Applied"
    
    t.close_Database()

def test_update_status():
    t = make_Tracker()
    add_application_helper(t)
    
    t.update_Application_Status("OpenAI",  "Software Engineer", "Interviewing")
    
    result = t.search_Application("OpenAI", "Software Engineer")
    
    assert len(result) == 1
    assert result[0][5] == "Interviewing"
    
    t.close_Database()

def test_update_interview_date():
    t = make_Tracker()
    add_mult_app_helper(t)
    
    company_name = "GOOGLE"
    job_title = "SOFTWARE ENGINEER"
    interview_date = "05/10/2026"
    
    t.update_interview_date(company_name, job_title, interview_date)
    
    result = t.search_Application(company_name, job_title)
    
    assert result[0][6] == interview_date 
    
    t.close_Database()

def test_list_app_by_status():
    t = make_Tracker()
    add_mult_app_helper(t)
    
    status = "Round"
    
    result = t.list_Applications_By_Status(status)
    
    print(*result, sep='\n')

def test_display_all_jobs():
    t = make_Tracker()
    add_mult_app_helper(t)
    
    result = t.display_All_Jobs()
    
    print(*result, sep='\n')
    

def test_remove_applications():
    t = make_Tracker()
    add_mult_app_helper(t)
    
    applications: list[dict] = []
    company_name = None
    job_title = None
    
    while True:
        company_name = input("Enter Company name (or 'exit' to stop): ")
        company_name = company_name.upper()
        if company_name == "EXIT":
            break
        
        job_title = input("Enter Job Title: ")
        job_title =job_title.upper()
        
        if not t.search_Application(company_name, job_title):
            print(f"\033[31m❌ Company: {company_name} and Job title: {job_title} was not found!\033[0m")        
        else: 
            print(f"\033[32m✅ Removing Company: {company_name} and Job title: {job_title} from Database!\033[0m")        
            applications.append({
                "company_name" : company_name,
                "job_title": job_title
            })
    
    t.remove_Applications(applications)
    result = t.display_All_Jobs()
    
    print(*result, sep='\n')
    print(f"{len(applications)} application(s) removed. {len(result)} remaining.")

    t.close_Database()

def test_display_up_Coming_Interviews():
    t = make_Tracker()
    add_mult_app_helper(t)
    
    result = t.display_up_Coming_Interviews()
    
    
    print(result, sep='\n')
    
    assert len(result) == 0

def test_search_application_by_company():
    t = make_Tracker()
    add_mult_app_helper(t)
    
    company_name = input ("Company Name: ").upper()
    
    result = t.search_Application_by_company(company_name)
    
    if not result:
        print (f"{company_name} NOT FOUND")
        return 
    
    print (*result, sep='\n')
    

            ###################### TESTING AUTHENTICATION DATABASE ######################

def test_add_and_search_credentials():
    t = make_Tracker()
    add_credential_helper(t)
    
    result = t.search_Credential("OpenAI")
    assert len(result) == 1
    assert result[0][1] == "OpenAI"
    assert result[0][2] == "benxiang3215@gmail.com"
    assert result[0][3] == "Testing1111"
    assert result[0][4] == "https://example.com/openai"
    
    t.close_Database()
    
def test_update_Credentials():
    t = make_Tracker()
    add_credential_helper(t)
    
    company_name= "OpenAI"
    user_name = "benxiang3215@gmail.com"
    new_password = "Testing3215@"
    
    t.update_Credentials(user_name, new_password, company_name)
    
    result = t.search_Credential("OpenAI")
    
    assert result [0][1] == "OpenAI"
    assert result [0][2] == "benxiang3215@gmail.com"
    assert result [0][3] == "Testing3215@"
    
    t.close_Database()

def test_remove_credential():
    t = make_Tracker()
    add_credential_helper(t)
    
    company_name = "OpenAI"
    user_name = "benxiang3215@gmail.com"
    
    t.remove_Credential(company_name, user_name)
    
    result = t.search_Credential(company_name)
    
    assert len(result) == 0
    
    t.close_Database()

def test_display_credentials():
    t = make_Tracker()
    add_mult_cred_helper(t)
    
    result = t.display_credentials()
    
    print(*result, sep='\n')
    
    t.close_Database()