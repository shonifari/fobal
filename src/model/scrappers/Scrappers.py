from pathlib import Path
import sys
# ADD THE SRC FOLDER TO THE SYS PATH
APP_FOLDER = str(Path(Path(Path(Path(__file__).parent.absolute()).parent.absolute()).parent.absolute()).parent.absolute())
sys.path.insert(0, APP_FOLDER) 


import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DirettaScrapper():

    def __init__(self) -> None:
        
        self.SECRET_KEY = ''
        self.ID_DECODER = ''
        self.SPORTS_DATA_BASE_URL = ''
        self.DIRETTA_USERNAME = ''
        self.DIRETTA_PSSWD = ''

        with open( APP_FOLDER + '/private/id_decoder.json','r') as jf:
            self.ID_DECODER = json.load(jf)
        with open( APP_FOLDER + '/private/private.json','r') as jf:
            _data = json.load(jf)
            self.SECRET_KEY = _data['SECRET_KEY']
            self.SPORTS_DATA_BASE_URL = _data['SPORTS_DATA_BASE_URL']
            self.DIRETTA_USERNAME = _data['DIRETTA_USERNAME']
            self.DIRETTA_PSSWD = _data['DIRETTA_PSSWD']
            self.DRIVER_LOCATION = _data['DRIVER_LOCATION']
        
        self.is_logged = False


        
    # # # # # # # # # # # #  BASE UTILS  # # # # # # # # # # # # 
    # CREATE DRIVER
    def _driver(self) -> webdriver:
         # initialise the driver
        s = Service(self.DRIVER_LOCATION)
        driver = webdriver.Chrome(service=s)

        # Set window size and position. Avoids sovrappositions for threading
        driver.set_window_size(900, 1000)
        #driver.set_window_position(x, y, windowHandle='current')
        return driver

    # # # # # # # # # # # #  WEBSITE UTILS  # # # # # # # # # # # # 
    # ACCEPT COOKIES
    def _accept_cookies(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))).click()
        except Exception as e:
            print('[ERROR] - : Unable to accept cookies.')    
            print(e)    

    # LOGIN
    def _login(self):

        #Check if already logged
        try:
            if WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="user-menu"]/span'))).text == self.DIRETTA_USERNAME:
                print('[USER IS LOGGED]')
                return True
            
        except Exception as e:
            print('[ERROR] - : Unable to login.')    
            print(e)   



        try:
            
            # Open login dial
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header__block--user-menu"]'))).click()
            # Insert cred
            self.driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(self.DIRETTA_USERNAME)
            self.driver.find_element(By.XPATH, '//*[@id="passwd"]').send_keys(self.DIRETTA_PSSWD)
            # Log
            self.driver.find_element(By.XPATH, '//*[@id="header__block--user-menu"]/div[2]/div/div/div/div[2]/section[2]/button').click()   
            

            # CHECK AGAIN IF USER IS LOGGED
            for i in range(0,10):
                if WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="user-menu"]/span'))).text == self.DIRETTA_USERNAME:
                    return True
                time.sleep(1)
            
        except Exception as e:
            print('[ERROR] - : Unable to login.')    
            print(e)    
 
   