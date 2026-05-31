from trackerClass import job_tracker
from menu import build_menue_options, menue
import time
import os

STARTING_BANNER = r"""
 ####  #######    ##    ######  ####### ### ##    ##  #####
##       ###     ####   ##   ##   ###   ### ###   ## ##
 ####    ###    ##  ##  ######    ###   ### ## ## ## ##  ###
    ##   ###    ######  ##  ##    ###   ### ##  #### ##   ##
 ####    ###    ##  ##  ##   ##   ###   ### ##   ###  #####
"""

JOB_TRACKER_BANNER = r"""
                    ##  #######  ######
                    ##  ##   ##  ##   ##
                    ##  ##   ##  ##   ##
                    ##  ##   ##  ######
                ##  ##  ##   ##  ##   ##
                ##  ##  ##   ##  ##   ##
                #####   #######  ######

#######  ######     ##     ######  ##  ##  #######  ######
   ##    ##   ##   ####   ##      ## ##   ##       ##   ##
   ##    ##   ##  ##  ##  ##      ####    ##       ##   ##
   ##    ######  ##    ## ##      ###     #####    ######
   ##    ##  ##  ######## ##      ####    ##       ##  ##
   ##    ##   ## ##    ## ##      ## ##   ##       ##   ##
   ##    ##   ## ##    ##  ###### ##  ##  #######  ##   ##
"""

EXITING_JOB_BANNER = r"""
####### ##   ## ### ####### ### ##    ##  #####
##       ## ##  ###   ###   ### ###   ## ##
#####     ###   ###   ###   ### ## ## ## ##  ###
##       ## ##  ###   ###   ### ##  #### ##   ##
####### ##   ## ###   ###   ### ##   ###  #####

       #######  #######  ######
          ##    ##   ##  ##   ##
          ##    ##   ##  ######
       ## ##    ##   ##  ##   ##
        ###     #######  ######
"""

def create_DB():
    return job_tracker()


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")
    
def print_banner(banner, delay = 0.8):
    for line in banner.splitlines():
        print(line)
        time.sleep(delay)


def banner_animation():
    clear_terminal()
    print_banner(STARTING_BANNER, delay=0.08)
    
    time.sleep(1.5)
    
    print_banner(JOB_TRACKER_BANNER, delay=0.05)
    
    time.sleep(1)
    
def banner_exiting():
    clear_terminal()
    print_banner(EXITING_JOB_BANNER, delay=0.08)
    
    time.sleep(1.5)
    

# TODO: Finish up the function
def run():
    user_input: None
    decision: None
    tracker = create_DB()
    MEUNE_OPTIONS = build_menue_options(tracker)
    
    banner_animation()
    time.sleep(1.5)
    clear_terminal()
    try:
        while True:
            menue(MEUNE_OPTIONS)
            user_input = input("Select an option or type exit to quit: ").strip().upper()
            if user_input == "EXIT":
                banner_exiting()
                time.sleep(1)
                clear_terminal()
                break
    except KeyboardInterrupt:
        banner_exiting()

if __name__ == '__main__':
    run()