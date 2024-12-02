# Instagram Block Automation
# Version 1.9

# Code Improvised by Saad BENBOUZID
# Github : https://github.com/Macadoshis

'''
For #Blockout2024
A Script crafted to automate blocking users on instagram
This script uses brave browser with chromium version 126
If you are a Palestine supporter and a developer, feel free to fork the code and make it better
This script is still experimental and can cause errors while running,
If the script throws errors, look at the error in the log-file in log directory.
'''

'''
Instructions
1. Either make changes according to your browser or install brave browser for easier use
2. Install the required modules using pip in command prompt
3. Run the code
'''


# Modules
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

from random import choice, randint

from os import listdir

from stdiomask import getpass

from datetime import datetime

from json import loads

# Vars
with open('res/config.json', 'r') as File_Obj:
    Config_Json = File_Obj.read()

Config = loads(Config_Json)

Buffer = Config['Buffer']
Standard_Wait = Config['Standard_Wait']
Increased_Wait = Config['Increased_Wait']
Buffer_Wait_Lower = Config["Buffer_Wait_Lower"]
Buffer_Wait_Upper = Config["Buffer_Wait_Upper"]

DRIVER = "./Driver/chromedriver.exe"
LINK = "http://www.instagram.com"
PROFILE = "https://www.instagram.com/{0}"

# Vars
with open('res/login.json', 'r') as File_Obj:
    login_json = File_Obj.read()
    
login = loads(login_json)

USERNAME = login["ID"]
PASSWORD = login["PASSWORD"]

Random_Wait_Times = [x/1000 for x in range(2000, 6001)]

Blocked_List_Exists = False
Blocked = []

if f'{USERNAME}.txt' in listdir('log'):
    Blocked_List_Exists = True

with open('res/Accounts_To_Block.txt', 'r') as File_Obj:
    To_Block = [user.strip('\n') for user in File_Obj.readlines()]

Counter = 0
WaitTime = randint(Buffer_Wait_Lower, Buffer_Wait_Upper)

# XPATH Vars
with open('./res/xpath.json', 'r') as File_Obj:
    XPATHS_Json = File_Obj.read()

XPATHS = loads(XPATHS_Json)

Search_Button_XPATH = XPATHS["Search_Button_XPATH"]
Follow_Button_XPATH = XPATHS["Follow_Button_XPATH"]


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")

# Initialisation
#service = Service(executable_path=DRIVER)
Browser = webdriver.Chrome(options=chrome_options)

# Functions
def New_Blocked_List(List):
    with open(f'./log/{USERNAME}.txt', 'w') as File_Obj:
        [File_Obj.write(element + '\n') for element in List]

def Retrive_Blocked_List():
    with open(f'./log/{USERNAME}.txt', 'r') as File_Obj:
        Data = [element.strip('\n') for element in File_Obj.readlines()]
    return Data

def log_error(ERROR):
    Mode = 'a' if f'Error_Log_{USERNAME}.txt' in listdir('./log') else 'w'
    with open(f'./log/Error_Log_{USERNAME}.txt', Mode) as File_Obj:
        time = datetime.now()
        record_time = f"[{time.day}/{time.month}/{time.year} | {time.time().hour}:{time.time().minute}:{time.time().second}]"
        File_Obj.write(f"{record_time}\n---[Error Start Block]---\n{ERROR}\n---[Error End Block]---\n")

def New_List():
    New = []
    for element in To_Block:
        if element not in Blocked:
            New.append(element)
    return New

def RandWait():
    Wait_Time = choice(Random_Wait_Times)
    sleep(Wait_Time)

def Block(USER_LINK):
    Browser.get(USER_LINK)
    
    try:
        
        # 1. 특정 좌표 (100, 50) 클릭
        actions = ActionChains(Browser)
        actions.move_by_offset(100, 50).click().perform()  # (0, 0) 클릭
        sleep(1)  # 지연 시간 추가 (필요시)   
        # 2. 탭(Tab) 키 6번 보내기
        for _ in range(6):
            actions.send_keys(Keys.TAB).perform()
            sleep(0.2)  # 지연 시간 추가 (필요시)

        # 3. 엔터(Enter) 키 보내기
        sleep(1)  # 지연 시간 추가 (필요시)   
        actions.send_keys(Keys.ENTER).perform()  
        
        sleep(1)  # 지연 시간 추가 (필요시)   
        actions.send_keys(Keys.ENTER).perform()  
        
        
    except Exception as Error:
        print(Error)
        return "404"
    
       
    return True

# Vars
if Blocked_List_Exists:
    Blocked = Retrive_Blocked_List()
    To_Block = New_List()
    
# Automation Process
Browser.get(LINK)

WebDriverWait(Browser, Standard_Wait).until(EC.presence_of_element_located((By.NAME, "password")))
RandWait()

Username_Input_Element = Browser.find_element(By.NAME, "username")
Username_Input_Element.send_keys(USERNAME)

Password_Input_Element = Browser.find_element(By.NAME, "password")
Password_Input_Element.send_keys(PASSWORD)
RandWait()

Password_Input_Element.send_keys(Keys.ENTER)

RandWait()
RandWait()

Browser.get(LINK)
RandWait()

print("Press 'Ctrl + c' to stop")

for User in To_Block:
    try:
        Val = Block(PROFILE.format(User))
        if Val == None:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {User} Already Blocked")
            Blocked.append(User)
            Counter += 1

        elif Val == True:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {User} blocked")
            Blocked.append(User)
            Counter += 1
            
        elif Val == "404":
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {User} | Account not found (unable to locate button elements)")
            Blocked.append(User)
            Counter += 1
        
        if Counter == Buffer:
            Counter = 0
            sleep(WaitTime)
    
    except KeyboardInterrupt:
        print("[Ctrl + c] received.. stopping now!!")
        New_Blocked_List(Blocked)
        Browser.quit()
        quit()
    
    except Exception as Error:
        print(Error)
        log_error(Error)
        try:
            Browser.get(LINK)
            WebDriverWait(Browser, Standard_Wait).until(EC.presence_of_element_located((By.XPATH, Search_Button_XPATH)))
            RandWait()
        except Exception as Error_2:
            print(Error_2)
            log_error(Error_2)
            New_Blocked_List(Blocked)
            quit()

#Quit
sleep(Standard_Wait * 1.5)
Browser.quit()
New_Blocked_List(Blocked)
