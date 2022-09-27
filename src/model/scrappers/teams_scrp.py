from datetime import datetime 
from pathlib import Path
import sys
from typing import List

import requests

# ADD THE SRC FOLDER TO THE SYS PATH
APP_FOLDER = str(Path(Path(Path(Path(__file__).parent.absolute()).parent.absolute()).parent.absolute()).parent.absolute())
sys.path.insert(0, APP_FOLDER) 

from sqlalchemy import func

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
from src.model.db.tables.Teams import Teams

from src.model.scrappers.Scrappers import DirettaScrapper


 

class TeamScrapper():

    def __init__(self) -> None:
        
        self.path = 'https://www.transfermarkt.co.uk/spieler-statistik/wertvollstespieler/marktwertetop?land_id=0&ausrichtung=alle&spielerposition_id=alle&altersklasse=alle&jahrgang=0&kontinent_id=0'
        
        self.ID_DECODER = '' 
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
        driver.set_window_size(900, 1000)
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
        #response = self._post_to_api_league(transfermarkt_id=TRANSFERMARKT_ID, name=LEAGUE_NAME, nation=NATION,league_level=LEAGUE_LEVEL,teams=TEAMS,logo=LOGO)
        

        
        found_league : Leagues = session.query(Leagues).filter(Leagues.transfermarkt_id == TRANSFERMARKT_ID).one()

        # SAVE INFO ABOUT LEAGUE FOR TEAM SCRAP
        if found_league:
            self.current_league['id'] = found_league.league_id
            self.current_league['nation'] = NATION
            self.current_league['transfermarkt_id'] = TRANSFERMARKT_ID

        for link in self._collect_teams_links():
            self.collect_team_info(link[1])
        

    def collect_teams_links(self):
        LINKS = []
        for league in self.leagues:
            self.driver.get(f'https://www.transfermarkt.co.uk/{league[0]}/startseite/wettbewerb/{league[1]}')
            LINKS += self._collect_teams_links()
        return LINKS



    def _collect_teams_links(self):
        '''** CALL ONLY WHEN DRIVER ON LEAGUE PAGE**'''
        LINKS = []
        try:
            table = self.driver.find_element(By.XPATH,'//*[@id="yw1"]/table/tbody')
            rows = table.find_elements(By.TAG_NAME,'tr')
            rows = [ 
                x.find_element(By.CLASS_NAME, 'hauptlink')
                .find_element(By.TAG_NAME,'a') 
                for x in rows
                ]
            for row in rows:
 
               LINKS.append([
                   row.get_attribute('title'), 
                   row.get_attribute('href').replace('startseite','leistungsdaten').replace('/saison_id/2021','')
                   ])
            
        except Exception as e:
            print('[ERROR SCRAPPING PLAYER] - :\n' , e)
        
        finally:
            print(LINKS)
            print(len(LINKS))
            
            return LINKS

     


    def collect_team_info(self,url):
        
        self.driver.get(url)
        
        
        box = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'dataHeader')))    

        LOGO =  box.find_element(By.CLASS_NAME,'dataBild').find_element(By.TAG_NAME,'img')

        TEAM_NAME =  LOGO.get_attribute('alt')
        LOGO =  LOGO.get_attribute('src')

        print('TEAM NAME: ' , TEAM_NAME)
        print('LOGO: ' , LOGO)
        SQUAD_SIZE = box.find_element(By.XPATH,'//*[@id="verein_head"]/div/div[1]/div[2]/div/div[1]/p[1]/span[2]').text
        STADIUM = box.find_element(By.XPATH,'//*[@id="verein_head"]/div/div[1]/div[2]/div/div[2]/p[2]/span[2]/a').text
        SEATS = box.find_element(By.XPATH,'//*[@id="verein_head"]/div/div[1]/div[2]/div/div[2]/p[2]/span[2]/span').text.split(' ')[0].replace('.','')
        
        print('STADIUM: ' , STADIUM)
        print('SEATS: ' , SEATS)

        TRANSFERMARKT_ID = url.split('/')[-6] + '@' + url.split('/')[-3] 
        print('TRANSFERMARKT_ID: ' , TRANSFERMARKT_ID)
        self.insert_team_to_db(name=TEAM_NAME, league_id=self.current_league['id'],nation=self.current_league['nation'],
        logo = LOGO, squad_size=SQUAD_SIZE, stadium=STADIUM, seats=SEATS,
        transfermarkt_id=TRANSFERMARKT_ID)
        
     
 
   


    def insert_team_to_db(self,name, league_id, nation, logo,
        squad_size, stadium, seats,
        transfermarkt_id):
     

   
        
        found_team : Teams = session.query(Teams).filter(Teams.transfermarkt_id == transfermarkt_id).first()
        if found_team:
            

            found_team.name=name 
            found_team.nation=nation 
            found_team.league_id=league_id
            found_team.squad_size=squad_size
            found_team.logo=found_team.get_logo(logo)
            found_team.stadium=stadium
            found_team.seats=seats
            found_team.transfermarkt_id=transfermarkt_id
            found_team.last_update = datetime.now()
        else:
            team = Teams(name=name, 
                nation=nation, 
                league_id=league_id,
                squad_size=squad_size,
                logo=logo,
                stadium=stadium,
                seats=seats,
                transfermarkt_id=transfermarkt_id
                ) 
            
            session.add(team)
        
        
        session.commit()
   



 
class ScrapTeam(DirettaScrapper):

    
       
    def __init__(self, league_name) -> None:
        ''' 
        
        '''
        super().__init__()
        
        self.driver : WebDriver = self._driver()
        
        
        # Open chrome to the page
        self.found_league : Leagues = session.query(Leagues).filter(Leagues.name == league_name).first()
        if not self.found_league : return

        
        self.driver.get(self.found_league.get_direttait_url())
        self._accept_cookies()
        
        print(self.found_league.nation)
        print(self.found_league.name)
        print(self.found_league.league_id)
        
        
        self.scrap_league(self.found_league.get_direttait_url())
        
         



 


    ########################################################################
    #                                                                      #
    #                          L E A G U E S                               #
    #                                                                      #
    ########################################################################

    def scrap_league(self, link): 
        self.links = self.team_links()
 
 
        for link in self.links:
            diretta_ID = link[1].split('/')[-3] +'/' + link[1].split('/')[-2] 
            
            if 'Milan' == link[0]:
                link[0] = 'AC Milan'

            found_team : Teams =  session.query(Teams).filter(func.lower(Teams.name).contains(link[0].replace('-',' '))).first()   
            if found_team:
               
                found_team.diretta_id = diretta_ID
                session.commit()

 

    ########################################################################
    #                                                                      #
    #                         T E A M S                                    #
    #                                                                      #
    ########################################################################

 

    # TEAM LINKS
    def team_links(self) -> List[List[str]]:
        links = []
        self.driver.get(self.driver.current_url + 'classifiche')
        classifica_table = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="tournament-table-tabs-and-content"]/div[3]/div[1]/div/div/div[2]')))
        
        rows = classifica_table.find_elements(By.CLASS_NAME,'ui-table__row')

        for row in rows:
            cell = row.find_element(By.CLASS_NAME,'tableCellParticipant__name')
            links.append([cell.text,cell.get_attribute('href')])
        
        return links
 
 
def teamFBREF_ID():
    # initialise the driver
    driver_path = '/Users/karis/Drivers/chromedriver'
    s = Service(driver_path)
    driver = webdriver.Chrome(service=s)

    # Set window size and position. Avoids sovrappositions for threading
    driver.set_window_size(900, 1000)
    #driver.set_window_position(x, y, windowHandle='current')

    # Open chrome to the page
    BASE_URL = 'https://fbref.com/en/comps/11/Serie-A-Stats' 
    driver.get(BASE_URL)

    # PART 1 :  Download the excel
    try:
            
        # Agree to cookies
        # Agree to cookies
        agree_cookies_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[3]')))
        agree_cookies_btn.click()
        print(f'- Reached website - ')


        teams_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="div_results2022-2023111_overall"]')))
        teams_table = teams_container.find_element(By.TAG_NAME, 'table')
        body = teams_table.find_element(By.TAG_NAME, 'tbody')
        rows = body.find_elements(By.TAG_NAME, 'tr')
        squad_columns = [row.find_elements(By.TAG_NAME, 'td')[0] for row in rows ]
        row_body = [squad.find_element(By.TAG_NAME, 'a') for squad in squad_columns ]
        links = [elem.get_attribute('href') for elem in row_body]
        print(links)
        


        for link in links:
            team = link.split('/')[-1].replace('-Stats','').replace('nazionale','')
            print(team)
            fbref_id = link.split('/')[-2]
            
            if 'Milan' == team:
                team = 'AC Milan'

            found_team : Teams =  session.query(Teams).filter(func.lower(Teams.name).contains(team.replace('-',' '))).first()   
            if found_team:
                found_team.fbref_id = fbref_id
                session.commit()
               

        driver.quit()

    except Exception as e:
        print(e)




 
if __name__ == '__main__':
    ###
    # sc = TeamScrapper().collect_league_info()

    ###
    sc = ScrapTeam('Serie A')

    ##
    # teamFBREF_ID()
    