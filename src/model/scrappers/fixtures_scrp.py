import datetime
from pathlib import Path
import sys

# ADD THE SRC FOLDER TO THE SYS PATH
# ADD THE SRC FOLDER TO THE SYS PATH
APP_FOLDER = str(Path(Path(Path(Path(__file__).parent.absolute()).parent.absolute()).parent.absolute()).parent.absolute())
sys.path.insert(0, APP_FOLDER) 


from typing import List
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.model.db.tables.Fixtures import Fixtures
from src.model.db.tables.Leagues import Leagues
from src.model.db.database import session
from src.model.scrappers.Scrappers import DirettaScrapper
from src.model.db.tables.Teams import Teams
class ScrapFixtures(DirettaScrapper):

    def __init__(self) -> None:
        ''' 
        
        '''
        super().__init__()
        
        self.driver : WebDriver = self._driver()
        

        self.current_league = {
            'id':'serie-a/'
        }
        

        # Open chrome to the page
        self.driver.get('https://www.diretta.it/serie-a/')
        self._accept_cookies()
      
        self.is_logged = self._login()
         
        self.legue_links = ['https://www.diretta.it/serie-a/']
    
    
    def scrap_past_fixtures(self):
        for link in self.legue_links:
            self._scrap_past_fixtures(link)
            
            

    def scrap_future_fixtures(self):
        for link in self.legue_links:
           

            self._scrap_future_fixtures(link)
 

    # TEAM INFO
 
    # MATCHES LINKS
    def match_links_and_matchday(self) :
       
        
        OUTPUT = {}
        calendar_table = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="live-table"]/div[1]/div/div')))
        
        rows = calendar_table.find_elements(By.XPATH,'./*')[1:]

        matchday = ''
        for row in rows:
            if 'event__round' in row.get_attribute('class'):
                matchday = row.text
                OUTPUT[matchday] = {'ids':[], 'links':[]}
            else:
                id = row.get_attribute('id').split('_')[-1]
                OUTPUT[matchday]['ids'].append(id)
                OUTPUT[matchday]['links'].append(f"https://www.diretta.it/partita/{id}/#/informazioni-partita")
        
        return OUTPUT


    # SEASON
    def get_season(self) -> str:
        return self.driver.find_element(By.XPATH,'//*[@id="mc"]/div[4]/div[1]/div[2]/div[2]').text

  

    def _get_my_league_links(self) -> List[str]:
        LINKS = []
        self.driver.get("https://www.diretta.it/")
        league_list = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="my-leagues-list"]')))
        league_list = league_list.find_elements(By.CLASS_NAME,'leftMenu__item')
        for league in league_list:
            print(league.get_attribute('title'))
            link = league.find_element(By.TAG_NAME,'a').get_attribute('href')
            print(link)
            LINKS.append(link)
        return LINKS




    ###### S C R A P   P A S T   F I X T U R E ####
    def _scrap_future_fixtures(self, link):
        print('\n\n' + link.split('/')[-2].replace('-', ' ').upper() + '\n\n')
        
        self.driver.get(link)
        
        # Collect data
        season = self.get_season()
        
        self.driver.get(self.driver.current_url + 'calendario')
        

                # Load all matches till first day
        while True:
            matchday = self.driver.find_elements(By.CLASS_NAME,'event__round')[-1].text.split(' ')[-1]
            print(matchday)

            if matchday == '38' : break

            more_button = self.driver.find_element(By.CLASS_NAME,'event__more')
            self.driver.execute_script('''arguments[0].scrollIntoView({
            behavior: 'auto',
            block: 'center',
            inline: 'center'
            });''', more_button)
            
            more_button.click()
            time.sleep(2)

        MATCHDAY_INFO = self.match_links_and_matchday()

        for matchday, values in MATCHDAY_INFO.items():
            diretta_ids = values['ids']
            links = values['links']
            print(int(matchday.split(' ')[-1]))
            if int(matchday.split(' ')[-1]) == 18: 

                print(links , '\n\n')
                for diretta_id,link in zip(diretta_ids,links):

                    date, home, home_diretta_id,home_score,away_score, away, away_diretta_id, referee ,home_score_1T , away_score_1T , home_score_2T , away_score_2T = scrap_match_info(self.driver, link)
                    ##
                    referee = None
                    ##

                    self.insert_fixture_to_db( diretta_id, season, matchday, date,
                    home, home_diretta_id,home_score,away_score, away, away_diretta_id,
                    home_score_1T , away_score_1T , home_score_2T , away_score_2T,
                    referee, link)



    ###### S C R A P   F U T U R E   F I X T U R E ####
    def _scrap_past_fixtures(self, link):
        print('\n\n' + link.split('/')[-2].replace('-', ' ').upper() + '\n\n')
        
        self.driver.get(link)
        
        # Collect data
        season = self.get_season()
        self.driver.get(self.driver.current_url + 'risultati')
        
        # Load all matches till first day
        while True:
            matchday = self.driver.find_elements(By.CLASS_NAME,'event__round')[-1].text.split(' ')[-1]
            print(matchday)

            if matchday == '1' : break

            more_button = self.driver.find_element(By.CLASS_NAME,'event__more')
            self.driver.execute_script('''arguments[0].scrollIntoView({
            behavior: 'auto',
            block: 'center',
            inline: 'center'
            });''', more_button)
            
            more_button.click()
            time.sleep(2)
            
            

        
      
        MATCHDAY_INFO = self.match_links_and_matchday()

        for matchday, values in MATCHDAY_INFO.items():
            
            diretta_ids = values['ids']
            links = values['links']
            print(links , '\n\n')

            for diretta_id,link in zip(diretta_ids[::-1],links[::-1]):

                date, home, home_diretta_id,home_score,away_score, away, away_diretta_id, referee , home_score_1T , away_score_1T , home_score_2T , away_score_2T = scrap_match_info(self.driver, link)
            
                print( diretta_id, season, matchday, date,
                    home, home_diretta_id,home_score,away_score, away, away_diretta_id,
                    referee, link, home_score_1T , away_score_1T , home_score_2T , away_score_2T)
                self.insert_fixture_to_db( diretta_id, season, matchday, date,
                    home, home_diretta_id,home_score,away_score, away, away_diretta_id,
                    home_score_1T , away_score_1T , home_score_2T , away_score_2T,
                    referee, link)
                
                # match_id = response['fixture_id']
                # home_id = response['home_id']
                # away_id = response['away_id']
                # home = response['home']
                # away = response['away']
                
           
             
             


    def fetch_league(self,url):
        diretta_id = url.replace('https://www.diretta.it/','')
        response = requests.get(self.SPORTS_DATA_BASE_URL + 'data/leagues/diretta_id:' + diretta_id.replace('/','@'))
        if response.status_code == 200:
            print(response.json())
            return response.json()
        else:
            print(response.content) 


    def insert_fixture_to_db(self, diretta_id,  season, matchday, date,
            home, home_diretta_id,home_score,away_score, away, away_diretta_id,
            home_score_1T , away_score_1T , home_score_2T , away_score_2T,
            referee,  link):
        
        league : Leagues = session.query(Leagues).filter(Leagues.diretta_id == self.current_league['id']).first()
        home_team : Teams = session.query(Teams).filter(Teams.diretta_id == home_diretta_id).first()
        away_team : Teams = session.query(Teams).filter(Teams.diretta_id == away_diretta_id).first()
 
        data = { 
                'diretta_id' : diretta_id, 
                'nation' : league.nation, 
                'league' : league.name,
                'league_id' :league.league_id,
                'season' : season, 
                'matchday' : matchday.split(' ')[-1], 
                'date' : date,
                        
                'home_diretta_id' : home_diretta_id,
                'home_score' : home_score,
                'away_score' : away_score, 
                'away_diretta_id' : away_diretta_id,
                'referee' : referee, 
                'diretta_link' : link
             
            }    
        print(data)
   

        fixture = Fixtures(
            season = season,
            nation = league.nation,
            league = league.name,
            league_id = league.league_id, 
            matchday = matchday.split(' ')[-1], 
            date =  datetime.datetime.strptime(date, '%d.%m.%Y %H:%M'), 
            home = home, 
            away = away, 
            home_id = home_team.team_id, 
            away_id = away_team.team_id, 
            home_score = home_score, 
            away_score = away_score, 
            home_score_1T = home_score_1T,
            away_score_1T = away_score_1T,
            home_score_2T = home_score_2T,
            away_score_2T = away_score_2T,
            stadium = home_team.stadium, 
            referee = referee, 
            diretta_link = link, 
            diretta_id = diretta_id)
        
        
        found_fix : Fixtures = session.query(Fixtures).filter(Fixtures.fixture_id == fixture.fixture_id).first()
        if found_fix:
            
            found_fix.season = season
            found_fix.nation = league.nation
            found_fix.league = league.name
            found_fix.league_id = league.league_id 
            found_fix.matchday = matchday.split(' ')[-1] 
            found_fix.date = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M')
            found_fix.home = home 
            found_fix.away = away 
            found_fix.home_id = home_team.team_id 
            found_fix.away_id = away_team.team_id 
            found_fix.home_score = home_score 
            found_fix.away_score = away_score 
            found_fix.home_score_1T = home_score_1T
            found_fix.away_score_1T = away_score_1T
            found_fix.home_score_2T = home_score_2T
            found_fix.away_score_2T = away_score_2T
            found_fix.stadium = home_team.stadium 
            found_fix.referee = referee 
            found_fix.diretta_link = link 
            found_fix.diretta_id = diretta_id   
            found_fix.last_update = datetime.datetime.now()
        else:
            session.add(fixture)
        
        
        session.commit()

    


 
def scrap_match_info(driver, match_link):
     
    driver.get(match_link)
    
    date = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="detail"]/div[5]/div[1]/div'))).text
    
    home = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[2]/div[3]/div[2]/a')
    home_diretta_id =  '/'.join(home.get_attribute('href').split('/')[-2:])
    home = home.text 
    
    away = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[4]/div[3]/div[1]/a')
    away_diretta_id =  '/'.join(away.get_attribute('href').split('/')[-2:])
    away = away.text
    
    try:
        score = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[3]/div/div[1]').find_elements(By.TAG_NAME, 'span')
        home_score = int(score[0].text)
        away_score = int(score[2].text)
    except:
        home_score = None
        away_score = None

    try:
        info_tab = driver.find_element(By.CLASS_NAME, 'mi__data').find_elements(By.CLASS_NAME, 'mi__item__val')
        referee = info_tab[0].text
        
    except:
        referee = None
   
    try:
        FH_score = driver.find_elements(By.CLASS_NAME, 'smv__incidentsHeader')[0]
        FH_score = FH_score.find_elements(By.TAG_NAME, 'div')[1].text
        print(FH_score)
        home_score_1T = int(FH_score.split(' - ')[0])
        away_score_1T = int(FH_score.split(' - ')[1])
        home_score_2T = home_score - home_score_1T
        away_score_2T = away_score - away_score_1T
    except:
        
        home_score_1T = None
        away_score_1T = None
        home_score_2T = None
        away_score_2T = None

    return  date, home, home_diretta_id,home_score,away_score, away, away_diretta_id, referee , home_score_1T , away_score_1T , home_score_2T , away_score_2T




def main():
    sc = ScrapFixtures()
    sc.scrap_future_fixtures()
    #sc.scrap_past_fixtures()
  
if __name__ == '__main__':
    main()
    #d = datetime.datetime.strptime('01.10.2022 14:00', '%d.%m.%Y %H:%M')