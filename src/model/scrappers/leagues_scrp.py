from datetime import datetime 
from pathlib import Path
import sys
from typing import List

import requests
# ADD THE SRC FOLDER TO THE SYS PATH
APP_FOLDER = str(Path(Path(Path(Path(__file__).parent.absolute()).parent.absolute()).parent.absolute()).parent.absolute())
sys.path.insert(0, APP_FOLDER) 



import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.model.db.database import session
from src.model.db.tables.Leagues import Leagues

from src.model.scrappers.Scrappers import DirettaScrapper


class LeagueScrapper():
    '''
    Scraps league from MarketTransfer and saves them to DB
    '''
    def __init__(self) -> None:
        
        self.path = 'https://www.transfermarkt.co.uk/spieler-statistik/wertvollstespieler/marktwertetop?land_id=0&ausrichtung=alle&spielerposition_id=alle&altersklasse=alle&jahrgang=0&kontinent_id=0'
        
        self.ID_DECODER = ''
        self.SPORTS_DATA_BASE_URL = ''
        with open( APP_FOLDER + '/private/private.json','r') as jf:
            _data = json.load(jf)  
            self.DRIVER_LOCATION = _data['DRIVER_LOCATION']
        ## 
        self.leagues = [
            #['premier-league','GB1'],
            ['serie-a','IT1'],
            #['serie-b','IT2'],
            #['primera-division','ES1'],
            #['1-bundesliga','L1'],
            #['ligue-1','FR1'],
            #['ligua-portugal','PO1'],
            #['eredivisie','NL1'],
            
            ]
        
        self.current_league = {}
        self.current_team = {}

        self.driver : WebDriver = self._driver()
        self.driver.get('https://www.transfermarkt.co.uk')
        self._accept_cookies()

        
    # # # # # # # # # # # #  BASE UTILS  # # # # # # # # # # # # 
    # CREATE DRIVER
    def _driver(self) -> webdriver:
         # initialise the driver
        s = Service(self.DRIVER_LOCATION)
        driver = webdriver.Chrome(service=s)

        # Set window size and position. Avoids sovrappositions for threading
        #driver.set_window_size(900, 1000)
        #driver.set_window_position(x, y, windowHandle='current')
        return driver

    # # # # # # # # # # # #  WEBSITE UTILS  # # # # # # # # # # # # 
    # ACCEPT COOKIES
    def _accept_cookies(self):
        try: 
            self.driver.switch_to.frame(self.driver.find_element(By.ID, 'sp_message_iframe_575846'))
            
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div[3]/div[2]'))).click()
            self.driver.switch_to.default_content()
            
        except Exception as e:
            print('[ERROR] - : Unable to accept cookies.')    
            print(e)    

    
    ####################################################


    def collect_league_info(self):
        for league in self.leagues:
            self._collect_league_info(f'https://www.transfermarkt.co.uk/{league[0]}/startseite/wettbewerb/{league[1]}')
        

    def _collect_league_info(self, url):
        
        self.driver.get(url)
        
        
        box = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'box')))    

        LOGO =  box.find_element(By.CLASS_NAME,'headerfoto').find_element(By.TAG_NAME,'img')

        LEAGUE_NAME =  LOGO.get_attribute('title')
        LOGO =  LOGO.get_attribute('src')

        print('LEAGUE NAME: ' , LEAGUE_NAME)
        print('LOGO: ' , LOGO)

        
        
        

        info_box =  box.find_elements(By.CLASS_NAME,'profilheader')[0]
        
        for i,row in enumerate(info_box.find_elements(By.TAG_NAME,'tr')):
            header = row.find_element(By.TAG_NAME,'th').text
            cell = row.find_element(By.TAG_NAME,'td').text
            print(header, cell)
            if i == 0:
                LEAGUE_LEVEL = cell.split('Tier')[0].replace('First','1').replace('Second','2')
                NATION = row.find_element(By.TAG_NAME,'img').get_attribute('title')
                print( 'correction: ',header, cell, NATION)

            if 'teams' in header:
                TEAMS = cell.split(' ')[0]

        TRANSFERMARKT_ID = url.split('/')[-4] + '@' + url.split('/')[-1] 
        response = self.insert_league_to_db(transfermarkt_id=TRANSFERMARKT_ID, name=LEAGUE_NAME, nation=NATION,league_level=LEAGUE_LEVEL,teams=TEAMS,logo=LOGO)
        


 

    def insert_league_to_db(self,name, nation, league_level, teams, logo, transfermarkt_id):
 

   
        league = Leagues(name=name, 
            nation=nation, 
            league_level=league_level,
            squad_size=teams,
            logo=logo,
            transfermarkt_id=transfermarkt_id
            )
        
        
        found_league : Leagues = session.query(Leagues).filter(Leagues.transfermarkt_id == transfermarkt_id).one()
        if found_league:
            
            found_league.name=name
            found_league.nation=nation
            found_league.league_level=league_level
            found_league.squad_size=teams
            found_league.logo= found_league.get_logo(logo)
            found_league.transfermarkt_id=transfermarkt_id
            found_league.last_update = datetime.now()
        else:
            session.add(league)
        
        
        session.commit()



 
   
class DIRETTA_LeagueScrapper(DirettaScrapper):

    ''' 
    SCRAPS DIRETT.IT LEAGUE ID
    '''
    
       
    def __init__(self) -> None:
        ''' 
        
        '''
        super().__init__()
        
        self.driver : WebDriver = self._driver()
        
        self.current_league = {}
        self.current_team = {}
        self.tot_players = 0
        # Open chrome to the page
        self.driver.get('https://www.diretta.it/')
        self._accept_cookies()
        self.is_logged = self._login()
        self.driver.get('https://www.diretta.it/')
        time.sleep(5)
        self.legue_links = self._get_my_league_links()

        for link in self.legue_links:
            if 'serie-a' in link:
                self.scrap_league(link)

        print('\n\n',self.tot_players, '\n\n')





    def _get_my_league_links(self) -> List[str]:
        LINKS = []
        
        league_list = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'my-leagues-list')))
        league_list = league_list.find_elements(By.CLASS_NAME,'leftMenu__item')
        for league in league_list:
            print(league.get_attribute('title'))
            try:
                link = league.find_element(By.TAG_NAME,'a').get_attribute('href')
                print(link)
                LINKS.append(link)
            except Exception as e:
                print(e)
                pass
        return LINKS


    ########################################################################
    #                                                                      #
    #                          L E A G U E S                               #
    #                                                                      #
    ########################################################################

    def scrap_league(self, link):
        print('\n\n' + link.split('/')[-2].replace('-', ' ').upper() + '\n\n')
        self.driver.get(link)
        
        # Collect data
        self.nation = self.get_nation()
        self.league = self.get_league_name()
        diretta_id = link.replace('https://www.diretta.it/','')
        print(self.nation)
        print(self.league)
        print(diretta_id)
        
        self.update_league_to_db(nation=self.nation,league_name=self.league,diretta_id=diretta_id)
  
    # LEAGUE NATION
    def get_nation(self) -> str:
        translation = {
            'Inghilterra':'England',
            'Italia':'Italy',
            'Spagna':'Spain',
            'Olanda':'Netherlands',
            'Germania':'Germany',
            'Francia':'France',
            'Portogallo':'Portugal',
        } 
        return translation[self.driver.find_element(By.XPATH,'//*[@id="mc"]/div[4]/div[1]/h2/a[2]').text.lower().capitalize()]
 
    # LEAGUE NAME
    def get_league_name(self) -> str:
        return self.driver.find_element(By.XPATH,'//*[@id="mc"]/div[4]/div[1]/div[2]/div[1]/div[1]').text
    
    # SEASON
    def get_season(self) -> str:
        return self.driver.find_element(By.XPATH,'//*[@id="mc"]/div[4]/div[1]/div[2]/div[3]').text

    
    def update_league_to_db(self,nation, league_name,  diretta_id):
        data = {
           # 'key': self.SECRET_KEY,
            'type': 'NEW LEAGUE',
            'sender': 'ScrapTransfermarkt',
            'source': 'TRANSFERMARKT',
            'load': {
                
                "nation" : nation,
                "league_name" : league_name,
                "diretta_id" : diretta_id
                
                }
                 
            }  

        print('\n\n',data)  

        input()
         
        
        
        found_league : Leagues = session.query(Leagues).filter(Leagues.name == league_name).one()
        if found_league:
            found_league.diretta_id=diretta_id
            found_league.last_update = datetime.now()
            session.commit()
         
     
 
 
 


 
if __name__ == '__main__': 
    #sc = LeagueScrapper().collect_league_info()
    sc = DIRETTA_LeagueScrapper()
    
    found_league : Leagues = session.query(Leagues).filter(Leagues.name == 'Serie A').one()
    #found_league.fbref_id = '11'
    #session.commit()
    print(found_league.get_fbref_url())
