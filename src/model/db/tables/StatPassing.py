from datetime import datetime
from pathlib import Path
import sys 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, Boolean,String, DateTime

from datetime import datetime
from uuid import uuid3, NAMESPACE_URL
from pathlib import Path
import sys

import requests
# ADD THE SRC FOLDER TO THE SYS PATH
APP_FOLDER = str(Path(Path(Path(Path(Path(__file__).parent.absolute()).parent.absolute()).parent.absolute()).parent.absolute()).parent.absolute())
sys.path.insert(0, APP_FOLDER) 

 
base = declarative_base()


from uuid import uuid3, NAMESPACE_URL


class StatPassing(base):
    __tablename__ = 'stat_passing'
    stat_id = Column(String, primary_key=True)
    
    match_day = Column(Integer, nullable = False)
    date = Column(String, nullable = False)
    home = Column(String(50), nullable = False)
    away = Column(String(50), nullable = False)
    
    team = Column(String(50), nullable = False)
    team_id = Column(String(50), nullable = False)
    
    player_id = Column(String(50), nullable = False)
    player = Column(String(50), nullable = False)
    pos = Column(String(50), nullable = False)
    
    season = Column(String(50), nullable = False)

    league_id = Column(String(50), nullable = False)
    fixture_id = Column(String(100))
    creation_date = Column(DateTime, default = datetime.now )
    last_update = Column(DateTime)
    
    min = Column(Integer, nullable = False)
    
    ##
    pass_tot_dist = Column(Numeric, nullable = False)
    pass_prog_dist = Column(Numeric, nullable = False)
    pass_A = Column(Integer, nullable = False)
    pass_C = Column(Integer, nullable = False)
    
    pass_short_A = Column(Integer, nullable = False)
    pass_short_C = Column(Integer, nullable = False)
    pass_med_A = Column(Integer, nullable = False)
    pass_med_C = Column(Integer, nullable = False)
    pass_long_A = Column(Integer, nullable = False)
    pass_long_C = Column(Integer, nullable = False)
    
    pass_ATT = Column(Integer, nullable = False)
    cross_PA = Column(Integer, nullable = False)
    pass_prog = Column(Integer, nullable = False)

    ast = Column(Integer, nullable = False)
    KP = Column(Integer, nullable = False)
 
    
    
    def __init__(self,
    match_day,date,home,away,min,
    team, team_id, player_id, player, pos,
    season, league_id,
    pass_tot_dist,
    pass_prog_dist,
    pass_A,
    pass_C,
    pass_short_A,
    pass_short_C,
    pass_med_A,
    pass_med_C,
    pass_long_A,
    pass_long_C,
    pass_ATT,
    cross_PA,
    pass_prog,
    ast,
    KP) -> None:
        super().__init__()
        
        self.stat_id = str(uuid3(NAMESPACE_URL, name=match_day + date + home + away + team + player))
        
        self.match_day = match_day
        self.date = date
        self.home = home
        self.away = away
        self.min = min
        self.team = team
        self.team_id = team_id
        self.player_id = player_id
        self.player = player
        self.pos = pos
        self.season = season
        self.league_id = league_id
        
        self.pass_tot_dist = float(pass_tot_dist) * 0.9144
        self.pass_prog_dist = float(pass_prog_dist) * 0.9144
        self.pass_A = pass_A
        self.pass_C = pass_C
        self.pass_short_A = pass_short_A
        self.pass_short_C = pass_short_C
        self.pass_med_A = pass_med_A
        self.pass_med_C = pass_med_C
        self.pass_long_A = pass_long_A
        self.pass_long_C = pass_long_C
        self.pass_ATT = pass_ATT
        self.cross_PA = cross_PA
        self.pass_prog = pass_prog
        self.ast = ast
        self.KP = KP





      
        
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
 
# DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
# engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)
 
# # DELETE TABLE
# StatPassing.__table__.drop(engine)
# # # CREATE TABLE
# base.metadata.create_all(engine)


 
    
