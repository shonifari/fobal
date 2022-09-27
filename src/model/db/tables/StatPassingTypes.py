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


class StatPassingTypes(base):
    __tablename__ = 'stat_passing_type'
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
    
    creation_date = Column(DateTime, default = datetime.now )
    last_update = Column(DateTime)
    
    min = Column(Integer, nullable = False)
    
    ##
    pass_live = Column(Integer, nullable = False)
    pass_dead = Column(Integer, nullable = False)
    pass_FK = Column(Integer, nullable = False)
    pass_through = Column(Integer, nullable = False)    
    pass_UP = Column(Integer, nullable = False)
    pass_switches = Column(Integer, nullable = False)    
    CK = Column(Integer, nullable = False)
    CK_IN = Column(Integer, nullable = False)
    CK_OUT = Column(Integer, nullable = False)
    CK_STR = Column(Integer, nullable = False)    
    pass_ground = Column(Integer, nullable = False)
    pass_low = Column(Integer, nullable = False)
    pass_high = Column(Integer, nullable = False)
    pass_LX = Column(Integer, nullable = False)
    pass_RX = Column(Integer, nullable = False)
    pass_Head = Column(Integer, nullable = False)    
    throws_in = Column(Integer, nullable = False)
    pass_other = Column(Integer, nullable = False)    
    pass_C = Column(Integer, nullable = False)
    pass_OFF = Column(Integer, nullable = False)
    pass_OUT = Column(Integer, nullable = False)
    pass_INT = Column(Integer, nullable = False)
    pass_Block = Column(Integer, nullable = False)
 
    
    def __init__(self,
    match_day,date,home,away,min,
    team, team_id, player_id, player, pos,
    season, league_id,
    pass_live,
    pass_dead,
    pass_FK,
    pass_through,
    pass_UP,
    pass_switches,
    CK,
    CK_IN,
    CK_OUT,
    CK_STR,
    pass_ground,
    pass_low,
    pass_high,
    pass_LX,
    pass_RX,
    pass_Head,
    throws_in,
    pass_other,
    pass_C,
    pass_OFF,
    pass_OUT,
    pass_INT,
    pass_Block
) -> None:
        super().__init__()
        
        self.stat_id = str(uuid3(NAMESPACE_URL, name=match_day + date + home + away + team + player + self.__tablename__))
        
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
        
        self.pass_live = pass_live
        self.pass_dead = pass_dead
        self.pass_FK = pass_FK
        self.pass_through = pass_through
        self.pass_UP = pass_UP
        self.pass_switches = pass_switches
        self.CK = CK
        self.CK_IN = CK_IN
        self.CK_OUT = CK_OUT
        self.CK_STR = CK_STR
        self.pass_ground = pass_ground
        self.pass_low = pass_low
        self.pass_high = pass_high
        self.pass_LX = pass_LX
        self.pass_RX = pass_RX
        self.pass_Head = pass_Head
        self.throws_in = throws_in
        self.pass_other = pass_other
        self.pass_C = pass_C
        self.pass_OFF = pass_OFF
        self.pass_OUT = pass_OUT
        self.pass_INT = pass_INT
        self.pass_Block = pass_Block





      
        
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
 
# DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
# engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)
 
# # # DELETE TABLE
# # StatPassingTypes.__table__.drop(engine)

# # # # CREATE TABLE
# base.metadata.create_all(engine)


 
    
