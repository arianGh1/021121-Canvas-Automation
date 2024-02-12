import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import pickle
import numpy as np
import pandas as pd
import pickle
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
from random import randint
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from openai import OpenAI
import shutil
def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

######### Input or change your desired values here ##########
fields = ["Computer Science", "Drugs", "History"]
project_link = 'https://www.canva.com/design/DAF8ZAbX2QA/iWN4RirO5r1jRpKUX8Untw/edit'
gpt_apikey = "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"
######### Input or change your desired values here ##########

options = Options()

options.add_argument('--user-data-dir=/Users/Arian_Gh/AppData/Local/Google/Chrome/User Data/') 
options.add_argument('--profile-directory=Profile 11')

options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--start-maximized")

options.add_argument('disable-infobars')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--remote-debugging-port=9222")

prefs = {
    "download.default_directory":os.path.join( os.getcwd(),'Downs'),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)


# Loop through each field name to create the main folder and subfolders
for fld in fields:
    # Create the main folder path
    main_folder_path = os.path.join(os.getcwd(), fld)
    
    # Check if the main folder exists, if not, create it and the subfolders
    if not os.path.exists(main_folder_path):
        os.makedirs(main_folder_path)  # Create the main folder
        
        # Define subfolders
        subfolders = ["tables", "videos"]
        
        # Loop through and create each subfolder
        for subfolder in subfolders:
            subfolder_path = os.path.join(main_folder_path, subfolder)
            os.makedirs(subfolder_path)  # Create the subfolder


now = datetime.now()
date_time_str = now.strftime("%Y%m%d-%H%M%S")

#Calling GPT
for field in fields:
    print(f'Calling GPT for table generation , field = {field}')
    client = OpenAI(
        api_key=gpt_apikey,
    )
    
    project_name = field+'$'+ date_time_str
    
    resp = chat_gpt(f'Set 10 questions in a tabular format with 2 incorrect answers & 1 correct one. You must mix the answers to be at A, B, or C also the answer meanings should be close and not easy to choose.Column 1: Nos:- 1 to 10\n\nColumn 2: Question:- A random question specified in subject: {field} and no more subjects.\nColumn 3is A: First answer option\n\nColumn 4 is B: Second answer option\n\nColumn 5 is C: Third answer option\n\nColumn 6is ANS: The correct answer(which should be the word which is correct not that letters A,B,C and it should be the value withing that one of choices).\n(Make the answer options one word only). also please dont provide stupid questions\n\x0c')
    table_lines = resp.strip().split("\n")[2:]  
    table_data   = []
    
    for line in table_lines:
        
        cells = [cell.strip() for cell in line.split('|')[1:-1]]  
        table_data.append(cells)
    
    # Convert list of lists to DataFrame
    df = pd.DataFrame(table_data, columns=['Nos', 'Question', 'A', 'B', 'C','ANS'])
    df.to_csv(f'{field}/tables/{project_name}.csv',index=False)

driver = webdriver.Chrome(options=options)
driver.maximize_window()

#Canvas Crowling
for field in fields:
    print(f'Generating the corresponding video in Canva for field = {field}')
    time.sleep(2)
    driver.get(project_link)
    project_name = field +'$'+ date_time_str
    time.sleep(3)
    time.sleep(randint(1,5))
    bulk_btns = driver.find_elements(By.CLASS_NAME, "Ve4yyQ")
    bulk_btns[-1].click()
    
    time.sleep(5)
    file_input = driver.find_element(By.CSS_SELECTOR,"input[type='file']")
    
    # Now send the file path directly to this input element
    file_path = f'/{field}/tables/{project_name}.csv' 
    time.sleep(randint(1,4))
    file_input.send_keys(os.getcwd(),file_path)
    
    time.sleep(4)
    continue_btn = driver.find_element(By.CLASS_NAME,"iVUNpg")
    time.sleep(randint(1,3))
    continue_btn.click()
    
    time.sleep(4)
    generate_btn = driver.find_element(By.CLASS_NAME,"iVUNpg")
    time.sleep(randint(1,3))
    generate_btn.click()
    
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])
    
    
    time.sleep(3)
    input_element = driver.find_element(By.CLASS_NAME, "EWbX5g")
    
    input_element.clear()
    time.sleep(3)
    
    input_element.send_keys(project_name)
    
    time.sleep(3)
    share_btn = driver.find_element(By.CLASS_NAME,"fTSnxg")
    time.sleep(randint(1,3))
    share_btn.click()
    
    time.sleep(2)
    time.sleep(randint(1,3))
    download_btn = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Download']")
    download_btn.click()
    
    time.sleep(3)
    download_btn2 = driver.find_element(By.CSS_SELECTOR,"button[type='submit']")
    time.sleep(randint(1,3))
    download_btn2.click()
    
    status = driver.find_element(By.CLASS_NAME,"wuAAeg")
    while "Completed" not in status.text:
        status = driver.find_element(By.CLASS_NAME,"wuAAeg")
    
    time.sleep(randint(1,4))
    
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
time.sleep(10)
driver.close()

#Move downloaded videos to their corresponding path
downs_folder_path = os.path.join(os.getcwd(), "Downs")

print(f'Moving downloaded videos to their homeland...')
if os.path.exists(downs_folder_path):
    
    video_files = [file for file in os.listdir(downs_folder_path) if file.endswith(".mp4")]
    
    # Loop through each video file
    for video_file in video_files:

        field_name = video_file.split("$")[0]  
        
        # Define the destination path in the corresponding field's 'videos' subfolder
        destination_path = os.path.join(os.getcwd(), field_name, "videos", video_file)
        
        # Check if the destination field folder exists
        if os.path.exists(os.path.dirname(destination_path)):
            # Move (cut and paste) the video file to the destination
            shutil.move(os.path.join(downs_folder_path, video_file), destination_path)
            
print(f'Done!')

