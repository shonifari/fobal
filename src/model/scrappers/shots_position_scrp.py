#
import datetime
from unidecode import unidecode
import json
from pathlib import Path
import sys 

# ADD THE SRC FOLDER TO THE SYS PATH
APP_FOLDER = str(Path(Path(Path(Path(__file__).parent.absolute()).parent.absolute()).parent.absolute()).parent.absolute())
sys.path.insert(0, APP_FOLDER) 


from typing import List
from sqlalchemy import func
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
from src.model.db.tables.Players import Players
from src.model.db.tables.ShotsPosition import ShotsPositions
 
from src.model.scrappers.Scrappers import DirettaScrapper
 


class ScrapShotsPositions(DirettaScrapper):

    def __init__(self) -> None:
        '''          '''
        super().__init__()
        
        self.driver : WebDriver = self._driver()
        self.positions_script_xpath = '/html/body/div[1]/div[3]/div[2]/div[1]/div/script'
        

 
 

    def scrap(self, matchday):
        links = [f'https://understat.com/match/{x}' for x in self.get_match_id(matchday)]
        
        for link in links:
            
            self.driver.get(link)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.positions_script_xpath)))
            
            #input()

            # Retreieve data about shots positions
            content = self.driver.execute_script("return shotsData;")
 
            #input()
            
            # Fetch teams
            h_team_fetched_name = content['a'][0]['h_team']
            h_team : Teams = session.query(Teams).filter(func.lower(Teams.name).contains(h_team_fetched_name)).first()
            a_team_fetched_name = content['a'][0]['a_team']
            a_team : Teams = session.query(Teams).filter(func.lower(Teams.name).contains(a_team_fetched_name)).first()

            if not h_team:
                input('______')
            print( h_team_fetched_name, '->', h_team.name)
            if not a_team:
                input('______')
            print( a_team_fetched_name, '->', a_team.name)

            # FETCH FIXTURE
            fixture : Fixtures = session.query(Fixtures).filter(Fixtures.home_id == h_team.team_id , Fixtures.away_id == a_team.team_id , Fixtures.matchday == matchday).first()
            if not fixture:
                print('FIXTURE')
                input('______')
            
            # SORT EVENTS BY ID. Sorted by id to avoid errors in 1H 45min and 2H 45min 
            team_shots = sorted(content['h'] + content['a'], key=lambda d: int(d['id']))
 
            # KEEP TRACK OFF TEAMS SCORE
            h_score = 0
            a_score = 0
            for i, shot in enumerate(team_shots):
                
                team = h_team if shot['h_a']  == 'h' else a_team
                if shot['result'] == 'Goal':
                    if shot['h_a']  == 'h':
                        h_score += 1
                    else:    
                        a_score += 1
                elif shot['result'] == 'OwnGoal':
                    if shot['h_a']  == 'h':
                        a_score += 1
                    else:    
                        h_score += 1

                shot['player'] = shot['player'].replace('&#039;','\'')
                #if shot['player'] == 'Nicolo Rovella' and 'Juventus' in team.name: 
                
                # MANUAL FIX 
                if shot['player'] == 'Marco Faraoni': shot['player'] = 'Davide Faraoni'
                
                player = self.fetch_player(shot['player'], team.team_id)
                
                # CHECK FOR ASSISTS
                player_asst = None
                if shot['player_assisted']:
                    shot['player_assisted'] = shot['player_assisted'].replace('&#039;','\'')
                    if shot['player_assisted'] == 'Marco Faraoni': shot['player_assisted'] = 'Davide Faraoni'
                    player_asst = self.fetch_player(shot['player_assisted'], team.team_id)
                

                shp = ShotsPositions(
                    fixture_id=fixture.fixture_id,
                    order=i,
                    X = float(shot['X']),
                    Y = float(shot['Y']),
                    home = h_team.name,
                    away = a_team.name,
                    home_score = h_score,
                    away_score = a_score,
                    team = team.name,
                    minute = int(shot['minute']),
                    player = player.name,
                    last_action = shot['lastAction'],
                    result = shot['result'],
                    shot_type = shot['shotType'],
                    situation = shot['situation'],
                    team_id = team.team_id,
                    player_id = player.player_id,
                    understat_link =  link,
                    home_id = h_team.team_id,
                    away_id = a_team.team_id,
                    player_assisted = player_asst.name if player_asst else None,
                    player_assisted_id = player_asst.player_id if player_asst else None,
                )

                found_shp : ShotsPositions = session.query(ShotsPositions).filter(ShotsPositions.shot_id == shp.shot_id).first()

                if found_shp:
                    
                    found_shp.fixture_id=fixture.fixture_id
                    found_shp.order=i
                    found_shp.X = float(shot['X'])
                    found_shp.Y = float(shot['Y'])
                    found_shp.home = h_team.name
                    found_shp.away = a_team.name
                    found_shp.home_score = h_score
                    found_shp.away_score = a_score
                    found_shp.team = team.name
                    found_shp.minute = int(shot['minute'])
                    found_shp.player = player.name
                    found_shp.last_action = shot['lastAction']
                    found_shp.result = shot['result']
                    found_shp.shot_type = shot['shotType']
                    found_shp.situation = shot['situation']
                    found_shp.team_id = team.team_id
                    found_shp.player_id = player.player_id
                    found_shp.understat_link = link
                    found_shp.home_id = h_team.team_id
                    found_shp.away_id = a_team.team_id
                    found_shp.player_assisted = player_asst.name if player_asst else None 
                    found_shp.player_assisted_id = player_asst.name if player_asst else None  
                    found_shp.last_update = datetime.datetime.now()

                else:
                    session.add(shp)
                
                session.commit()

             
                 
                



        


  
                    


    def fetch_player(self, name, team_id) -> Players: 
        pl : Players = session.query(Players).filter(Players.name == name).first()
        if not pl:
            pl = session.query(Players).all()
            pl = [p for p in pl if unidecode(p.name)==unidecode(name)]
            if len(pl) > 0:
                pl = pl[0]
            
        if pl: 
            return pl
        
        else:
            team_players : List[Players] = session.query(Players).filter(Players.team_id == team_id).all()
            if team_players:
                _team_pls_dict = {}
                for pl in team_players : _team_pls_dict[unidecode(pl.name)] = pl

                if unidecode(name) in _team_pls_dict.keys():
                    return _team_pls_dict[unidecode(name)]
                
                elif fix_specific_player_names(name) in _team_pls_dict.keys():
                    return _team_pls_dict[fix_specific_player_names(name)]
                    

                else:
                    for pl in team_players : _team_pls_dict[pl.name] = pl
                    
                    if fix_specific_player_names(name) in _team_pls_dict.keys():
                        _team_pls_dict[fix_specific_player_names(name)]
                    
                    else:    
                        print(_team_pls_dict.keys())
                        print(name) 
                        return None
                        


     
    def get_match_id(self, matchday : int = None) -> List[int]:
        OUTPUT = []
        
        game_1 = 18582 - 10
        current_matchday_game_1 = matchday * 10 + game_1

        for i in range(0,10):
            OUTPUT.append(current_matchday_game_1 + i)
        return OUTPUT
      
        
         
        
 

def rename_player(name) -> str:

        
         
        chr = set() 
        
        
        alph = 'a b c d e f g h i j k l m n o p q r s t u v w x y z - . \''.split(' ') + [' ']
        output = name

        do_it = False
        for ch in name.lower():
            if not ch in alph:
                do_it = True
                chr.add(ch)
        if do_it: 

            _A = 'ã ą ă á ä à '
            _A = _A.split(' ') + _A.upper().split(' ') 
            _E = 'è ę é ë'
            _E = _E.split(' ') + _E.upper().split(' ') 
            _I = 'ì í ï ı'
            _I = _I.split(' ') + _I.upper().split(' ') 
            _O = 'ó ö ò ô ø'
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
 




def fix_specific_player_names(name) -> str:
    names = {

        'Pepín': 'Jose Machin',
        'Franck Zambo' : 'Andre Zambo Anguissa' ,
        'Mehdi Leris':'Marcel Leris Mehdi Pascal',
        'Ibañez': 'Roger Ibanez',
        'Thórir Helgason': 'Thorir Johann Helgason',
        'Kim Min-Jae': 'Min-Jae Kim',
        #'Marco Faraoni': 'Davide Faraoni',
        'Ruslan Malinovskiy' : 'Ruslan Malinovskyi',
        'Gianmarco Ferrari': 'Gian Marco Ferrari',
        'Marlon Santos': 'Marlon',
        'Igor Julio': 'Igor',
        'Jean-Daniel Akpa-Akpro': 'Jean-Daniel Akpa Akpro',
        'Soualiho Meité': 'Soualiho Meite',
        'Christian Gytkjær': 'Christian Gytkjaer',
        'Fode Toure': 'Fode Ballo-Toure',
        'Mikael Ellertsson': 'Mikael Egill Ellertsson',
        'Emil Ceïde': 'Emil Konradsen Ceide',
        'Wilfried Stephane Singo': 'Stephane Singo',
        'Matìas Soulè Malvano': 'Matias Soule',
        'Iyenoma Destiny Udogie': 'Destiny Udogie',
        'Pierre Kalulu Kyatengwa': 'Pierre Kalulu',
        'Mehmet Zeki Çelik': 'Zeki Celik',
        'Tanguy NDombele Alvaro': 'Tanguy Ndombele',
        'Agustín Álvarez Martínez': 'Agustin Alvarez',
       
    }
    return names[name] if name in names.keys() else name
         





def main():
    sc = ScrapShotsPositions()
     
    for i in range(1,9):
        sc.scrap(i) 

if __name__ == '__main__':
    main() 
     
     