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
from src.model.db.tables.Players import Players

from src.model.scrappers.Scrappers import DirettaScrapper







class PlayersScrapper():

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
 


    def collect_team_info(self,team_id, league_id,url):
        
        self.driver.get(url)

        for link in self._collect_players_links():
            #if not link[1] in self.all_players_url:
                print('\n[NEW PLAYER TO ADD]: ', link[0],'\n')
                try:
                    self.collect_player_info(team_id, league_id,link[1])
                except Exception as e:
                    print('[UNABLE TO COLLECT PLAYER]:')
                    print(e)
                    pass
        




    def _collect_players_links(self):
        '''** CALL ONLY WHEN DRIVER ON TEAM PAGE **'''
        LINKS = []
        try:
            table = self.driver.find_element(By.XPATH,'//*[@id="yw1"]/table/tbody')
            rows = table.find_elements(By.CLASS_NAME,'odd') + table.find_elements(By.CLASS_NAME,'even')
            
            for i in range(0,len(rows)):
                xpath=f'//*[@id="yw1"]/table/tbody/tr[{i + 1}]/td[2]/table/tbody/tr[1]/td[2]/div[1]/span/a'
                player_box = self.driver.find_element(By.XPATH,xpath)
                
                print(i + 1,player_box.get_attribute('title'), player_box.get_attribute('href'))
                LINKS.append([player_box.get_attribute('title'), player_box.get_attribute('href')])
                 
            print(LINKS)


        except Exception as e:
            print('[ERROR SCRAPPING PLAYER] - :\n' , e)
        
        finally:
            return LINKS
        
            

    def collect_player_info(self, team_id, league_id, url):
        
        self.driver.get(url)
        
        
        box = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'data-header')))    
        NUMBER = ''
        try:
            NUMBER =  box.find_element(By.CLASS_NAME,'data-header__shirt-number').text
        except:
            pass
        


        LOGO = None
        PLAYER_NAME =  None
        try:
            
            LOGO = self.driver.find_element(By.CLASS_NAME,'data-header__profile-container').find_element(By.TAG_NAME,'img')
            PLAYER_NAME =  LOGO.get_attribute('title')
            LOGO =  LOGO.get_attribute('src')
        except:    
            pass        
 
        if not PLAYER_NAME : return

        print('PLAYER NAME : ' , PLAYER_NAME)
        print('NUMBER: ' , NUMBER)
        print('LOGO: ' , LOGO)

        
        DOB = ''
        NATION = ''
        HEIGHT = ''
        POSITION = ''
        
        

        info_box =  box.find_element(By.CLASS_NAME,'data-header__details').find_elements(By.TAG_NAME,'ul')[:2]
        info_list = [x.find_elements(By.TAG_NAME,'li') for x in info_box]
        info_list = info_list[0] + info_list[1]
        for i,row in enumerate(info_list):
            if i < 5:
                header = row.text.split(':')[0]
                cell = row.find_element(By.TAG_NAME, 'span').text
                
                if 'Date' in header:
                    DOB = str(cell).split('(')[0]
                elif 'Citizenship' in header:
                    NATION = cell
                elif 'Height' in header:
                    HEIGHT = cell
                elif 'Position' in header:
                    POSITION = cell
                
                
                
                print(header, cell)
                
        
        TRANSFERMARKT_ID = url.split('/')[-4] + '@' + url.split('/')[-1]

        self.insert_player_to_db(name=PLAYER_NAME, team_id=team_id, league_id=league_id, img=LOGO,
        nation=NATION, number = NUMBER, dob = DOB , height =HEIGHT , position=POSITION, transfermarkt_id=TRANSFERMARKT_ID)

 


    def insert_player_to_db(self,name,team_id, league_id, nation, img,
       number, dob, height,position,
        transfermarkt_id):
        data = { 
            'type': 'NEW PLAYER',
            'sender': 'ScrapTransfermarkt',
            'source': 'TRANSFERMARKT',
            'load': {
        'name' : name,
        'team_id' : team_id,
        'league_id' : league_id,
        'nation' : nation, 
        'number':number,
        'dob' : dob, 
        'height' : height,
        'position' : position,
        'transfermarkt_id' : transfermarkt_id
                }
                 
            }  

        print('\n\n',data)  

        found_player : Players = session.query(Players).filter(Players.transfermarkt_id == transfermarkt_id).first()
        if found_player:
            

            found_player.name=name 
            found_player.nation=nation 
            found_player.league_id=league_id
            found_player.nation=nation
            found_player.img=found_player.get_logo(img)
            found_player.number=number
            found_player.dob=dob
            found_player.height=height
            found_player.position=position
            found_player.transfermarkt_id=transfermarkt_id
            found_player.last_update = datetime.now()
        else:
            player = Players(
                name=name,
                team_id=team_id,
                league_id=league_id,
                nation=nation,
                img=img,
                number=number,
                dob=dob,
                height=height,
                position=position,
                transfermarkt_id=transfermarkt_id
            
            )
            
            session.add(player)
        
        
        session.commit()


  
class DirettaScrapPlayers(DirettaScrapper):
    '''
    Scraps player info from diretta.it
    '''
    
       
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
        
        self.current_team = None
        self.teams = session.query(Teams).filter(Teams.league_id == self.found_league.league_id).all()
        
        
        # done_teams = ['Inter Milan','AC Milan','Juventus FC','SSC Napoli','AS Roma',
        # 'Atalanta BC','SS Lazio', 'US Sassuolo','ACF Fiorentina',
        # 'Torino FC','AC Monza','Bologna FC 1909', 'Udinese Calcio',
        # 'Hellas Verona','US Salernitana 1919','FC Empoli','UC Sampdoria']
        for team in self.teams:
            # if not team.name in done_teams:
                self.current_team = team
                self.scrap_players(team)

        

    def scrap_players_info(self,team):
        self.driver.get(team.get_direttait_url() + '/rosa')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "overall-all"))).click()
        
        elemtns = [ x for x in self.driver.find_elements(By.CSS_SELECTOR, "a[class='lineup__cell lineup__cell--name']") if x.text != '']
        names =[ x.text for x in elemtns ]
        links =[ x.get_attribute('href') for x in elemtns ]
        ids =[ x.split('/')[-2] + x.split('/')[-1] for x in links ]

        for i,id in enumerate(ids[:-1]):
            name_el = names[i].split(' ')
            name = ' '.join([name_el[-1]] + name_el[:-1])
            name2 = ' '.join(name_el[-2:] + name_el[:-2])
            
            
            id = ids[i]
            link = links[i]

            found_players : Players = session.query(Players).filter(Players.team_id == self.current_team.team_id).all()
            
            player_names = {}

            for player in found_players:
                player_names[rename_player(player.name)] = player

            
 
             
            if name in list(player_names.keys()):
                player_names[name].diretta_id = '/'.join(link.split('/')[-3:])
                print(player_names[name].diretta_id)
                
            elif names[i] in list(player_names.keys()):
                name = names[i]
                player_names[name].diretta_id = '/'.join(link.split('/')[-3:])
                print(player_names[name].diretta_id)
                
            
            elif name2 in list(player_names.keys()):
                player_names[name2].diretta_id = '/'.join(link.split('/')[-3:])
                print(player_names[name2].diretta_id)
                

            else:    
                print('\n\n\n' + id, name,link)
            
            session.commit()
        
        return names[:-1], ids[:-1]    
 

        
    def scrap_players(self, team):  
        a,b = self.scrap_players_info(team)
        
def fix_specific_player_names(name) -> str:
    names = {
        
        'Ruslan Malinovskyi' : 'Ruslan Malinovsky' ,
        'Christian Kouamé' : 'Cristian Kouame' ,
        'Denso Kasius' : 'Dense Kasius' ,
        'Juan Cabal' : 'David Cabal Juan' ,
        'Jaime Báez' : 'Jaime Baez Stabile' ,
        'Mehdi Léris' : 'Marcel Leris Mehdi Pascal' ,
    }
    return names[name] if name in names.keys() else name
       

def rename_player(name) -> str:

        name = fix_specific_player_names(name)

        chr = set() 
        path = '/Users/karis/dev/Python/fb_analysis/rsrc/Teams/Serie A/Players Images/2122/'
        
        alph = 'a b c d e f g h i j k l m n o p q r s t u v w x y z - . \''.split(' ') + [' ']
        output = name

        do_it = False
        for ch in name.lower():
            if not ch in alph:
                do_it = True
                chr.add(ch)
        if do_it: 

            _A = 'ã ą ă á ä'
            _A = _A.split(' ') + _A.upper().split(' ') 
            _E = 'è ę é ë'
            _E = _E.split(' ') + _E.upper().split(' ') 
            _I = 'ì í ï ı'
            _I = _I.split(' ') + _I.upper().split(' ') 
            _O = 'ó ö ò ô'
            _O = _O.split(' ') + _O.upper().split(' ') 
            _U = 'ü ú'
            _U = _U.split(' ') + _U.upper().split(' ') 
            _L = 'ł'
            _L = _L.split(' ') + _L.upper().split(' ') 
            _Z = 'ż ž '
            _Z = _Z.split(' ') + _Z.upper().split(' ') 
            _S = 'š ș'
            _S = _S.split(' ') + _S.upper().split(' ') 
            _C = 'ć č ç '
            _C = _C.split(' ') + _C.upper().split(' ') 
            _N = 'ñ ń'
            _N = _N.split(' ') + _N.upper().split(' ') 
            _G = 'ğ '
            _G = _G.split(' ') + _G.upper().split(' ') 
            _T = 'ț'
            _T = _T.split(' ') + _T.upper().split(' ') 
            _D = 'đ ð'
            _D = _D.split(' ') + _D.upper().split(' ') 
            _DJ = 'đ'
            _DJ = _DJ.split(' ') + _DJ.upper().split(' ') 
            _AE = 'æ'
            _AE = _AE.split(' ') + _AE.upper().split(' ') 
            
            
        
        
            
            for ch in name:
                
                if ch in _A:
                    output = output.replace(ch,'a') 
                if ch in _E:
                    output = output.replace(ch,'e') 
                if ch in _I:
                    output = output.replace(ch,'i') 
                if ch in _O:
                    output = output.replace(ch,'o') 
                if ch in _U:
                    output = output.replace(ch,'u') 
                if ch in _L:
                    output = output.replace(ch,'l') 
                if ch in _Z:
                    output = output.replace(ch,'z') 
                if ch in _S:
                    output = output.replace(ch,'s') 
                if ch in _C:
                    output = output.replace(ch,'c') 
                if ch in _N:
                    output = output.replace(ch,'n') 
                if ch in _G:
                    output = output.replace(ch,'g') 
                if ch in _T:
                    output = output.replace(ch,'t') 
                if ch in _D:
                    output = output.replace(ch,'d') 
                if ch in _DJ:
                    output = output.replace(ch,'dj') 
                if ch in _AE:
                    output = output.replace(ch,'ae')
                    


                    
                        
            
                    
            words = output.split(' ')
            new_string = ''
            for word in words:
                new_string += word[:1].upper()
                new_string += word[1:]
                new_string += ' '
                
            output = new_string[:-1]    
            

        return output if do_it else name
 


 



def scrap_players_link(teams):
 
    
    # initialise the driver
    driver_path = '/Users/karis/Drivers/chromedriver'
    s = Service(driver_path)
    driver = webdriver.Chrome(service=s)

    # Set window size and position. Avoids sovrappositions for threading
    driver.set_window_size(900, 1000)
    #driver.set_window_position(x, y, windowHandle='current')

    for team in teams: 
        
        driver.get(team.get_fbref_url())

        try:        

            teams_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="div_stats_standard_11"]')))
            teams_table = teams_container.find_element(By.TAG_NAME, 'table')
            body = teams_table.find_element(By.TAG_NAME, 'tbody')
            rows = body.find_elements(By.TAG_NAME, 'tr')
            player_cols = [row.find_elements(By.TAG_NAME, 'th')[0] for row in rows ]
            
            row_body = []
            for player in player_cols:
                try:
                    a = player.find_element(By.TAG_NAME, 'a')
                    row_body.append(a)
                except:
                    pass

            data = {}
            for elem in row_body:
                data[rename_player(elem.text)] = elem.get_attribute('href')
            
            

            found_players : Players = session.query(Players).filter(Players.team_id == team.team_id).all()
            player_names = {}
            for pl in found_players:
                player_names[rename_player(pl.name)] = pl

            print(sorted(list(player_names.keys())))
            for name in list(data.keys()) :
                if name in list(player_names.keys()):
                    player_names[name].fbref_id = '/'.join(data[name].split('/')[-2:])
                    print('/'.join(data[name].split('/')[-2:]))
                    session.commit()
                else:
                    print(name)
                    new_name = input()
                    if new_name in list(player_names.keys()):
                        player_names[new_name].fbref_id = '/'.join(data[name].split('/')[-2:])
                        session.commit()
                    else:
                        print(name)
                        
            

            
            
            

            
            #scrap_player_image(driver, links,team_tag)

        except Exception as e:
            print(e)


 
if __name__ == '__main__':
    # #sc = ScrapMarketTransfers()
    # found_league : Leagues = session.query(Leagues).filter(Leagues.name == 'Serie A').first()

    # teams = session.query(Teams).filter(Teams.league_id == found_league.league_id).all()
    
    # ##
    # sc = PlayersScrapper()
    # print([x.get_transfermarkt_url() for x in teams])
    # for t in teams:
    #     sc.collect_team_info( t.team_id,t.league_id, t.get_transfermarkt_url())
     
    # ScrapPlayers('Serie A')

    # p = session.query(Players).filter(Players.name.contains('Soualiho')).first()
    # print(p.name)
    # players = session.query(Players).all()

    # for pl  in players:
    #     rename = rename_player(pl.name)
    #     if rename != pl.name:
    #         print(pl.name, '---->', rename )


    found_league : Leagues = session.query(Leagues).filter(Leagues.name == 'Serie A').first()
    teams = session.query(Teams).filter(Teams.league_id == found_league.league_id).all()

    scrap_players_link(teams)

 
