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


class StatDefense(base):
    __tablename__ = 'stat_defense'
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
    tkl_A = Column(Integer, nullable = False)
    tkl_W = Column(Integer, nullable = False)
    tkl_DEF = Column(Integer, nullable = False)
    tkl_MID = Column(Integer, nullable = False)
    tkl_ATT = Column(Integer, nullable = False)
    drib_vs_A = Column(Integer, nullable = False)
    drib_vs_Stop = Column(Integer, nullable = False)
    drib_vs_past = Column(Integer, nullable = False)
    press_A = Column(Integer, nullable = False)
    press_W = Column(Integer, nullable = False)    
    press_DEF = Column(Integer, nullable = False)
    press_MID = Column(Integer, nullable = False)    
    press_ATT = Column(Integer, nullable = False)
    blk = Column(Integer, nullable = False)
    blk_SH = Column(Integer, nullable = False)
    blk_SoT = Column(Integer, nullable = False)    
    blk_pass = Column(Integer, nullable = False)
    inter = Column(Integer, nullable = False)
    clr = Column(Integer, nullable = False)
    err_SH = Column(Integer, nullable = False)
     
 
    
    def __init__(self,
    match_day,date,home,away,min,
    team, team_id, player_id, player, pos,
    season, league_id,
    tkl_A,
    tkl_W,
    tkl_DEF,
    tkl_MID,
    tkl_ATT,
    drib_vs_A,
    drib_vs_Stop,
    drib_vs_past,
    press_A,
    press_W,
    press_DEF,
    press_MID,
    press_ATT,
    blk,
    blk_SH,
    blk_SoT,
    blk_pass,
    inter,
    clr,
    err_SH
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
        
        self.tkl_A = tkl_A
        self.tkl_W = tkl_W
        self.tkl_DEF = tkl_DEF
        self.tkl_MID = tkl_MID
        self.tkl_ATT = tkl_ATT
        self.drib_vs_A = drib_vs_A
        self.drib_vs_Stop = drib_vs_Stop
        self.drib_vs_past = drib_vs_past
        self.press_A = press_A
        self.press_W = press_W
        self.press_DEF = press_DEF
        self.press_MID = press_MID
        self.press_ATT = press_ATT
        self.blk = blk
        self.blk_SH = blk_SH
        self.blk_SoT = blk_SoT
        self.blk_pass = blk_pass
        self.inter = inter
        self.clr = clr
        self.err_SH = err_SH





      
        
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
 
# DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
# engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)
 
# # # DELETE TABLE
# # StatDefense.__table__.drop(engine)

# # # # CREATE TABLE
# base.metadata.create_all(engine)


 
    
