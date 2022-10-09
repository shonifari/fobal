
import json
from pathlib import Path
import sys


# ADD THE SRC FOLDER TO THE SYS PATH
APP_FOLDER = str(Path(Path(Path(Path(__file__).parent.absolute()).parent.absolute()).parent.absolute()).parent.absolute())
sys.path.insert(0, APP_FOLDER) 


from typing import List

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.model.db.database import session
from src.model.db.tables.Fixtures import Fixtures
from src.model.db.tables.Teams import Teams
 
from src.model.scrappers.Scrappers import DirettaScrapper
 


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
    def scrap_events(self):

            
        for link in self.legue_links:
                
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
                print(int(matchday.split(' ')[-1]))
                

                print(links , '\n\n')
                for diretta_id,link in zip(diretta_ids,links):

                    EVENTS_DATA = scrap_match_events(self.driver, link)
                    
                    for d in EVENTS_DATA:
                        print(d)
                    input()


  



def _scrap_lineups(driver, link,matchday, ):
    
    LINEUPS_JSON_PATH = '/Users/karis/dev/Python/fobal/res/lineups/2223--serie-a.json'

    _link = link.split('/')[:-1]
    _link.append('formazioni')
    _link = '/'.join(_link)
    driver.get(_link)
    # Select the 'partita' section
    lineup_section_button = driver.find_element(By.XPATH,'//*[@id="detail"]/div[7]/div/a[3]')
    lineup_section_button.click()
    
    formations = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'lf__field'))).find_elements(By.CLASS_NAME, 'lf__formation')

    lineups = {}
    
        
    for i, lineup in enumerate(formations):
        sections = {}
        field_sections = lineup.find_elements(By.CLASS_NAME,'lf__line')
         
        for ii, sect in enumerate(field_sections):
            players = sect.find_elements(By.CLASS_NAME ,'lf__player')
            players_links = [f.find_element(By.CLASS_NAME,'lf__playerName').get_attribute('href') for f in players]
            player_names = ['/'.join(f.split('/')[-3:]) for f in players_links]
            
            print(player_names)
            
            
            #players_names = [f.find_element(By.CLASS_NAME,'lf__playerNameInner').text for f in players]
            
            sections[ii] = player_names
        
        lineups[i] = sections

    
    print(lineups)




    fixture : Fixtures = session.query(Fixtures).filter(Fixtures.diretta_link == link).first()
    print(fixture.home)
    print(fixture.away)

    try:
        with open(LINEUPS_JSON_PATH, 'r', encoding='utf-8') as f:
            LINEUPS = json.load(f)
    
    except Exception as e:
        print(e)
        LINEUPS = {
            "lineups":{
                "1": {
                    "FIX_ID":{
                        "fixture_id":"",
                        "home":"",
                        "away":"",
                        "home_id":"",
                        "away_id":"",
                        "home_lineup":{},
                        "away_lineup":{}
                    }
                }
            }
        }

    
    
    if not str(matchday) in LINEUPS['lineups'].keys():
        LINEUPS['lineups'][str(matchday)] = {}
    
    LINEUPS['lineups'][str(matchday)][fixture.fixture_id] = {
        "fixture_id":fixture.fixture_id,
        "home":fixture.home,
        "away":fixture.away,
        "home_id":fixture.home_id,
        "away_id":fixture.away_id,
        "home_lineup":lineups[0],
        "away_lineup":lineups[1]
        
        
        }
    
        

        
    with open(LINEUPS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(LINEUPS, f, ensure_ascii=False, indent=4)


def scrap_match_events(driver : WebDriver, match_link):
    
    match_link = 'https://www.diretta.it/partita/8ANy6MTO/#/informazioni-partita'
    driver.get(match_link)
    
    fixture : Fixtures = session.query(Fixtures).filter(Fixtures.diretta_link == match_link).first()
    home : Teams = session.query(Teams).filter(Teams.team_id == fixture.home_id).first()
    away : Teams = session.query(Teams).filter(Teams.team_id == fixture.away_id).first()
    
    events_section = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'smv__verticalSections')))
    events = events_section.find_elements(By.XPATH,'./*')
    
    
    OUTPUT = []
    

  
    home_score = 0
    away_score = 0
    status = 'First Half'

    # get events    
    for event in events[1:]:

        DATA = {}
        DATA['home_score'] = home_score
        DATA['away_score'] = away_score
    
        if 'smv__incidentsHeader' in event.get_attribute('class'):
            status = 'Second Half'
            continue

        DATA['status'] = status


        team_event_id = home.diretta_id if 'home' in event.get_attribute('class').split(' ')[-1] else away.diretta_id
        DATA['team_event_id'] = team_event_id
        try:
            is_var = event.find_elements(By.CLASS_NAME,'var-ico')
        except:
            is_var = []

         
        if len(is_var) == 0:
            event_section = event.find_element(By.CLASS_NAME, 'smv__incident')
            try:
                event_icon = event_section.find_element(By.CLASS_NAME, 'smv__incidentIcon') 
                DATA['player_id'] = '/'.join(event.find_element(By.CLASS_NAME, 'smv__playerName').get_attribute('href').split('/')[-3:])
            except: 
                try:
                    event_icon = event_section.find_element(By.CLASS_NAME, 'smv__incidentIconSub') 
                    DATA['player_id'] = '/'.join(event.find_element(By.CLASS_NAME, 'smv__playerName').get_attribute('href').split('/')[-3:])
                    
                except: 
                    event_icon = event_section.find_element(By.CLASS_NAME, 'smv__incidentIcon') 
                    DATA['player_id'] = '/'.join(event.find_element(By.CLASS_NAME, 'smv__assist').find_element(By.TAG_NAME,'a').get_attribute('href').split('/')[-3:])
                    
            #player = get_player_name(player, team_event)

            DATA['minutes'] = event.find_element(By.CLASS_NAME, 'smv__timeBox').text[:-1]
            DATA['match_event'] = ''
            DATA['second_player_id'] = ''
            if len(event_icon.find_elements(By.CLASS_NAME, 'yellowCard-ico')) == 1:
                DATA['match_event'] = 'Yellow Card'

            elif len(event_icon.find_elements(By.CLASS_NAME, 'redCard-ico')) == 1:
                DATA['match_event'] = 'Red Card'
        
            elif len(event_icon.find_elements(By.CLASS_NAME, 'card-ico')) == 1:
                DATA['match_event'] = 'Second Yellow Card'

            elif len(event_icon.find_elements(By.CLASS_NAME, 'soccer')) == 1:
                DATA['match_event'] = 'Goal'
                if len(event.find_elements(By.CLASS_NAME,'smv__subIncident')) == 1 :
                    DATA['second_player_id'] = event.find_element(By.CLASS_NAME,'smv__subIncident').text
                elif len(event.find_elements(By.CLASS_NAME,'smv__assist')) == 1 :
                    DATA['second_player_id'] = '/'.join(event.find_element(By.CLASS_NAME, 'smv__assist').find_element(By.TAG_NAME,'a').get_attribute('href').split('/')[-3:])
                    

                home_score += 1 if team_event_id == home.diretta_id else 0
                away_score += 1 if team_event_id == away.diretta_id else 0

            elif len(event_icon.find_elements(By.CLASS_NAME, 'footballOwnGoal-ico')) == 1:
                DATA['match_event'] = 'Own Goal'
                away_score += 1 if team_event_id == home.diretta_id else 0
                home_score += 1 if team_event_id == away.diretta_id else 0
            
            elif len(event_icon.find_elements(By.CLASS_NAME, 'warning')) == 1:
                DATA['match_event'] = 'Missed Pen'
            
            elif len(event_icon.find_elements(By.CLASS_NAME, 'var')) == 1:
                DATA['match_event'] = 'VAR No Goal'
            
            elif len(event_icon.find_elements(By.CLASS_NAME, 'substitution')) == 1:
                DATA['match_event'] = 'Subs'
                DATA['second_player_id'] = '/'.join(event.find_element(By.CLASS_NAME, 'smv__subDown').get_attribute('href').split('/')[-3:])
                
             
            OUTPUT.append(DATA)
    return OUTPUT






def main():
    sc = ScrapFixtures()
    sc.scrap_events() 

if __name__ == '__main__':
    main() 





