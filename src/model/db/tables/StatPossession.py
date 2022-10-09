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


class StatPossession(base):
    __tablename__ = 'stat_possession'
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
    touch = Column(Integer, nullable = False)
    touch_live = Column(Integer, nullable = False)
    touch_DEF_PA = Column(Integer, nullable = False)
    touch_DEF = Column(Integer, nullable = False)
    touch_MID = Column(Integer, nullable = False)
    touch_ATT = Column(Integer, nullable = False)
    touch_ATT_PA = Column(Integer, nullable = False)
    dribs_A = Column(Integer, nullable = False)
    dribs_W = Column(Integer, nullable = False)
    dribs_n_pl = Column(Integer, nullable = False)    
    dribs_megs = Column(Integer, nullable = False)
    ctrl = Column(Integer, nullable = False)    
    ctrl_tot_dist = Column(Numeric, nullable = False)
    ctrl_prog_dist = Column(Numeric, nullable = False)
    ctrl_prog = Column(Integer, nullable = False)
    ctrl_ATT = Column(Integer, nullable = False)    
    ctrl_PA = Column(Integer, nullable = False)
    ctrl_L = Column(Integer, nullable = False)
    ctrl_TO = Column(Integer, nullable = False)
    rec_A = Column(Integer, nullable = False)
    rec_W = Column(Integer, nullable = False)
    rec_prog = Column(Integer, nullable = False)
     
 
    
    def __init__(self,
    match_day,date,home,away,min,
    team, team_id, player_id, player, pos,
    season, league_id,
    touch,
    touch_live,
    touch_DEF_PA,
    touch_DEF,
    touch_MID,
    touch_ATT,
    touch_ATT_PA,
    dribs_A,
    dribs_W,
    dribs_n_pl,
    dribs_megs,
    ctrl,
    ctrl_tot_dist,
    ctrl_prog_dist,
    ctrl_prog,
    ctrl_ATT,
    ctrl_PA,
    ctrl_L,
    ctrl_TO,
    rec_A,
    rec_W,
    rec_prog
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
        
        self.touch = touch
        self.touch_live = touch_live
        self.touch_DEF_PA = touch_DEF_PA
        self.touch_DEF = touch_DEF
        self.touch_MID = touch_MID
        self.touch_ATT = touch_ATT
        self.touch_ATT_PA = touch_ATT_PA
        self.dribs_A = dribs_A
        self.dribs_W = dribs_W
        self.dribs_n_pl = dribs_n_pl
        self.dribs_megs = dribs_megs
        self.ctrl = ctrl
        self.ctrl_tot_dist = float(ctrl_tot_dist) * 0.9144
        self.ctrl_prog_dist = float(ctrl_prog_dist) * 0.9144
        self.ctrl_prog = ctrl_prog
        self.ctrl_ATT = ctrl_ATT
        self.ctrl_PA = ctrl_PA
        self.ctrl_L = ctrl_L
        self.ctrl_TO = ctrl_TO
        self.rec_A = rec_A
        self.rec_W = rec_W
        self.rec_prog = rec_prog




      
        
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
 
# DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
# engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)
 
# # # DELETE TABLE
# # StatPossession.__table__.drop(engine)

# # # # CREATE TABLE
# base.metadata.create_all(engine)


 
    
