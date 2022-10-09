from datetime import datetime 
from pathlib import Path
import sys
import os
from typing import List

import requests
# ADD THE SRC FOLDER TO THE SYS PATH
APP_FOLDER = str(Path(Path(Path(Path(__file__).parent.absolute()).parent.absolute()).parent.absolute()).parent.absolute())
sys.path.insert(0, APP_FOLDER) 
from sqlalchemy import func
import pandas as pd
from src.model.db.tables.Players import Players
from src.model.db.tables.Teams import Teams
from src.model.db.tables.StatKeeper import StatKeeper
from src.model.db.tables.StatPassing import StatPassing
from src.model.db.tables.StatPassingTypes import StatPassingTypes 
from src.model.db.tables.StatDefense import StatDefense
from src.model.db.tables.StatPossession import StatPossession
from src.model.db.tables.StatPerformance import StatPerformance
from src.model.db.database import session
RAW_FOLDER = '/Users/karis/dev/Python/fb_analysis/data/Serie A/2223/CSVs/Raw/Matches/'
SEASON = 2223

def stat_keeper(matchday = None):

    csvs = [RAW_FOLDER + x for x in os.listdir(RAW_FOLDER) if 'keeper' in x]
    
    if matchday:
        csvs = [x for x in csvs if f'{matchday})' in x]
    
    
    for csv in csvs:

        FILE_NAME = csv.split('/')[-1]
        df = pd.read_csv(csv)
        print(df)

        df.columns = (df.columns[:1].tolist() +  df.iloc[0, 1:].tolist())
        print(df)

        df = df[1:]
        print(df)
        df = df.fillna(0)
        FILE_INFO = FILE_NAME.split(' ')
        MATCHDAY = FILE_INFO[0].split(')')[0]
            
        HOME = FILE_INFO[2].split('-')[0]
        AWAY = FILE_INFO[2].split('-')[1]
        TEAM = FILE_INFO[4][1:4]

        DATE = FILE_INFO[1]

        for i,row in df.iterrows():
            try:
                found_player : Players = session.query(Players).filter(Players.fbref_id.contains(str(df.loc[i,'-9999']))).first()
            except:
                found_player : Players = session.query(Players).filter(Players.fbref_id.contains(str(df.loc[i,-9999]))).first()
            
            
            if found_player:


                stat_keeper = StatKeeper(
                    match_day=MATCHDAY, date=DATE, 
                    home=HOME, away=AWAY, 
                    min=int(df.loc[i,'Min']), 
                    team=TEAM,team_id=found_player.team_id, 
                    player_id=found_player.player_id, player=found_player.name, season=SEASON, league_id=found_player.league_id, 
                    SoTA=int(df.loc[i,'SoTA']), GA=int(df.loc[i,'GA']), saves=int(df.loc[i,'Saves']), pass_A=df.loc[i,'Att'][1], throws=df.loc[i,'Thr'], 
                    launch_A=df.loc[i,'Att'][0], launch_C=df.loc[i,'Cmp'], pass_launch_perc=df.loc[i,'Launch%'][0], pass_avg_len=df.loc[i,'AvgLen'][0],
                    GK_A=df.loc[i,'Att'][2], GK_launch_perc=df.loc[i,'Launch%'][1], GK_avg_len=df.loc[i,'AvgLen'][1], 
                    opp_cross_A=df.loc[i,'Opp'], opp_cross_stop=df.loc[i,'Stp'], 
                    n_sweeps_out_PA=df.loc[i,'#OPA'], sweeps_avg_dist_GL=df.loc[i,'AvgDist']
                )
                
                found_stat : StatKeeper = session.query(StatKeeper).filter(StatKeeper.stat_id == stat_keeper.stat_id).first()
                if not found_stat:
                    session.add(stat_keeper)
                    session.commit()
                else:
                     
                    found_stat.season=SEASON
                    found_stat.min=int(df.loc[i,'Min'])
                    found_stat.SoTA=int(df.loc[i,'SoTA'])
                    found_stat.GA=int(df.loc[i,'GA'])
                    found_stat.saves=int(df.loc[i,'Saves'])
                    found_stat.pass_A=df.loc[i,'Att'][1]
                    found_stat.throws=df.loc[i,'Thr']
                    found_stat.launch_A=df.loc[i,'Att'][0]
                    found_stat.launch_C=df.loc[i,'Cmp']
                    found_stat.pass_launch_perc=df.loc[i,'Launch%'][0]
                    found_stat.pass_avg_len=df.loc[i,'AvgLen'][0]
                    found_stat.GK_A=df.loc[i,'Att'][2]
                    found_stat.GK_launch_perc=df.loc[i,'Launch%'][1]
                    found_stat.GK_avg_len=df.loc[i,'AvgLen'][1]
                    found_stat.opp_cross_A=df.loc[i,'Opp']
                    found_stat.opp_cross_stop=df.loc[i,'Stp']               
                    found_stat.n_sweeps_out_PA=df.loc[i,'#OPA']
                    found_stat.sweeps_avg_dist_GL=df.loc[i,'AvgDist']
                    found_stat.last_update = datetime.now()
                    session.commit()



def stat_passing(update=False, matchday = None):

    csvs = [RAW_FOLDER + x for x in os.listdir(RAW_FOLDER) if 'passing.csv' in x]
    if matchday:
        csvs = [x for x in csvs if f'{matchday})' in x]
    
  
    not_fp = []
    wrong_team = []
    for csv in csvs:

        FILE_NAME = csv.split('/')[-1]
        df = pd.read_csv(csv)
        print(df)

        df.columns = (df.columns[:1].tolist() +  df.iloc[0, 1:].tolist())
 
        df = df[1:-1]
         

 
        df = df.fillna(0)
        FILE_INFO = FILE_NAME.split(' ')
        MATCHDAY = FILE_INFO[0].split(')')[0]
            
        HOME = FILE_INFO[2].split('-')[0]
        AWAY = FILE_INFO[2].split('-')[1]
        TEAM = FILE_INFO[4][1:4]

        DATE = FILE_INFO[1]

        for i,row in df.iterrows():
            # COLUMN is sometimes numeric
            try:
                found_player : Players = session.query(Players).filter(Players.fbref_id.contains(str(df.loc[i,'-9999']))).first()
            except:
                found_player : Players = session.query(Players).filter(Players.fbref_id.contains(str(df.loc[i,-9999]))).first()
            
            
            # NOT FOUND PLAYERS are usually players who changed team before the DB scrapping
            if not found_player:
                print(csv)
                print(df.loc[i][[0]])
                not_fp.append([df.loc[i][[0]], TEAM])
            else:

                found_tm : Teams = session.query(Teams).filter(Teams.team_id == found_player.team_id).first()
                # CHECK IF the current player team is the same of the stat
                if found_tm and not TEAM.lower() in found_tm.name.lower():
                    wrong_team.append(f'{TEAM} --> {found_tm.name} | {found_player.name}')
                    
                    # IF NOT, check for team with same TAG
                    found_tm : Teams = session.query(Teams).filter( func.lower(Teams.name).contains(TEAM.lower())).first()
                    if found_tm:
                        wrong_team.pop(-1)

                # IF THERE IS THE TEAM     
                if found_tm:
                    print(csv)
                    print(df) 
                    stat_passing = StatPassing(
                        match_day=MATCHDAY, date=DATE, 
                        home=HOME, away=AWAY, 
                        min=int(df.loc[i,'Min']), 
                        pos=df.loc[i,'Pos'], 
                        team=TEAM,team_id=found_tm.team_id, 
                        player_id=found_player.player_id, player=found_player.name, season=SEASON, league_id=found_tm.league_id, 
                        pass_tot_dist = df.loc[i,'TotDist'],
                        pass_prog_dist = df.loc[i,'PrgDist'],
                        pass_A = df.loc[i,'Att'][0],
                        pass_C = df.loc[i,'Cmp'][0],
                        pass_short_A = df.loc[i,'Att'][1],
                        pass_short_C = df.loc[i,'Cmp'][1],
                        pass_med_A = df.loc[i,'Att'][2],
                        pass_med_C = df.loc[i,'Cmp'][2],
                        pass_long_A = df.loc[i,'Att'][3],
                        pass_long_C = df.loc[i,'Cmp'][3],
                        pass_ATT = df.loc[i,'1/3'],
                        cross_PA = df.loc[i,'CrsPA'],
                        pass_prog = df.loc[i,'Prog'],
                        ast = df.loc[i,'Ast'],
                        KP = df.loc[i,'KP']
                    )
                    
                    found_stat : StatPassing = session.query(StatPassing).filter(StatPassing.stat_id == stat_passing.stat_id).first()
                    if not found_stat:
                        session.add(stat_passing)
                        session.commit()
                    
                    elif update: 
                        found_stat.season=SEASON
                        found_stat.min=int(df.loc[i,'Min'])
                        found_stat.pos=df.loc[i,'Pos']
                        found_stat.pass_tot_dist = df.loc[i,'TotDist']
                        found_stat.pass_prog_dist = df.loc[i,'PrgDist']
                        found_stat.pass_A = df.loc[i,'Att'][0]
                        found_stat.pass_C = df.loc[i,'Cmp'][0]
                        found_stat.pass_short_A = df.loc[i,'Att'][1]
                        found_stat.pass_short_C = df.loc[i,'Cmp'][1]
                        found_stat.pass_med_A = df.loc[i,'Att'][2]
                        found_stat.pass_med_C = df.loc[i,'Cmp'][2]
                        found_stat.pass_long_A = df.loc[i,'Att'][3]
                        found_stat.pass_long_C = df.loc[i,'Cmp'][3]
                        found_stat.pass_ATT = df.loc[i,'1/3']
                        found_stat.cross_PA = df.loc[i,'CrsPA']
                        found_stat.pass_prog = df.loc[i,'Prog']
                        found_stat.ast = df.loc[i,'Ast']
                        found_stat.KP = df.loc[i,'KP']
                        found_stat.last_update = datetime.now()
                        session.commit()
                    

    print(not_fp)
    print(wrong_team)


def stat_passing_types(update=False, matchday = None):

    csvs = [RAW_FOLDER + x for x in os.listdir(RAW_FOLDER) if 'passing_types.csv' in x]
    if matchday:
        csvs = [x for x in csvs if f'{matchday})' in x]

    not_fp = []
    wrong_team = []
    for csv in csvs:

        FILE_NAME = csv.split('/')[-1]
        df = pd.read_csv(csv)
        print(df)

        df.columns = (df.columns[:1].tolist() +  df.iloc[0, 1:].tolist())
 
        df = df[1:-1]
         

 
        df = df.fillna(0)
        FILE_INFO = FILE_NAME.split(' ')
        MATCHDAY = FILE_INFO[0].split(')')[0]
            
        HOME = FILE_INFO[2].split('-')[0]
        AWAY = FILE_INFO[2].split('-')[1]
        TEAM = FILE_INFO[4][1:4]

        DATE = FILE_INFO[1]

        for i,row in df.iterrows():
            # COLUMN is sometimes numeric
            try:
                found_player : Players = session.query(Players).filter(Players.fbref_id.contains(str(df.loc[i,'-9999']))).first()
            except:
                found_player : Players = session.query(Players).filter(Players.fbref_id.contains(str(df.loc[i,-9999]))).first()
            
            
            # NOT FOUND PLAYERS are usually players who changed team before the DB scrapping
            if not found_player:
                print(csv)
                print(df.loc[i][[0]])
                not_fp.append([df.loc[i][[0]], TEAM])
            else:

                found_tm : Teams = session.query(Teams).filter(Teams.team_id == found_player.team_id).first()
                # CHECK IF the current player team is the same of the stat
                if found_tm and not TEAM.lower() in found_tm.name.lower():
                    wrong_team.append(f'{TEAM} --> {found_tm.name} | {found_player.name}')
                    
                    # IF NOT, check for team with same TAG
                    found_tm : Teams = session.query(Teams).filter( func.lower(Teams.name).contains(TEAM.lower())).first()
                    if found_tm:
                        wrong_team.pop(-1)

                # IF THERE IS THE TEAM     
                if found_tm:
                    print(csv)
                    print(df) 
                     
                    stat_passing = StatPassingTypes(
                        match_day=MATCHDAY, date=DATE, 
                        home=HOME, away=AWAY, 
                        min=int(df.loc[i,'Min']), 
                        pos=df.loc[i,'Pos'], 
                        team=TEAM,team_id=found_tm.team_id, 
                        player_id=found_player.player_id, player=found_player.name, season=SEASON, league_id=found_tm.league_id, 
                        pass_live = df.loc[i,'Live'],
                        pass_dead = df.loc[i,'Dead'],
                        pass_FK = df.loc[i,'FK'],
                        pass_through = df.loc[i,'TB'],
                        pass_UP = df.loc[i,'Press'],
                        pass_switches = df.loc[i,'Sw'],
                        CK = df.loc[i,'CK'],
                        CK_IN = df.loc[i,'In'],
                        CK_OUT = df.loc[i,'Out'][0],
                        CK_STR = df.loc[i,'Str'],
                        pass_ground = df.loc[i,'Ground'],
                        pass_low = df.loc[i,'Low'],
                        pass_high = df.loc[i,'High'],
                        pass_LX = df.loc[i,'Left'],
                        pass_RX = df.loc[i,'Right'],
                        pass_Head = df.loc[i,'Head'],
                        throws_in = df.loc[i,'TI'],
                        pass_other = df.loc[i,'Other'],
                        pass_C = df.loc[i,'Cmp'],
                        pass_OFF = df.loc[i,'Off'],
                        pass_OUT = df.loc[i,'Out'][1],
                        pass_INT = df.loc[i,'Int'],
                        pass_Block = df.loc[i,'Blocks']
                    )
                    found_stat : StatPassingTypes = session.query(StatPassingTypes).filter(StatPassingTypes.stat_id == stat_passing.stat_id).first()
                    if not found_stat:
                        session.add(stat_passing)
                        session.commit()
                     
                    elif update: 
                        found_stat.season=SEASON
                        found_stat.min=int(df.loc[i,'Min'])
                        found_stat.pos=df.loc[i,'Pos']
                        found_stat.pass_live = df.loc[i,'Live']
                        found_stat.pass_dead = df.loc[i,'Dead']
                        found_stat.pass_FK = df.loc[i,'FK']
                        found_stat.pass_through = df.loc[i,'TB']
                        found_stat.pass_UP = df.loc[i,'Press']
                        found_stat.pass_switches = df.loc[i,'Sw']
                        found_stat.CK = df.loc[i,'CK']
                        found_stat.CK_IN = df.loc[i,'In']
                        found_stat.CK_OUT = df.loc[i,'Out']
                        found_stat.CK_STR = df.loc[i,'Str']
                        found_stat.pass_ground = df.loc[i,'Ground']
                        found_stat.pass_low = df.loc[i,'Low']
                        found_stat.pass_high = df.loc[i,'High']
                        found_stat.pass_LX = df.loc[i,'Left']
                        found_stat.pass_RX = df.loc[i,'Right']
                        found_stat.pass_Head = df.loc[i,'Head']
                        found_stat.throws_in = df.loc[i,'TI']
                        found_stat.pass_other = df.loc[i,'Other']
                        found_stat.pass_C = df.loc[i,'Cmp']
                        found_stat.pass_OFF = df.loc[i,'Off']
                        found_stat.pass_OUT = df.loc[i,'Out']
                        found_stat.pass_INT = df.loc[i,'Int']
                        found_stat.pass_Block = df.loc[i,'Blocks']

                        found_stat.last_update = datetime.now()
                        session.commit()
                    

    print(not_fp)
    print(wrong_team)

def stat_defense(update=False, matchday = None):

    csvs = [RAW_FOLDER + x for x in os.listdir(RAW_FOLDER) if 'defense.csv' in x]
    if matchday:
        csvs = [x for x in csvs if f'{matchday})' in x]

    not_fp = []
    wrong_team = []
    for csv in csvs:

        FILE_NAME = csv.split('/')[-1]
        df = pd.read_csv(csv)
        print(df)

        df.columns = (df.columns[:1].tolist() +  df.iloc[0, 1:].tolist())
 
        df = df[1:-1]
         

 
        df = df.fillna(0)
        FILE_INFO = FILE_NAME.split(' ')
        MATCHDAY = FILE_INFO[0].split(')')[0]
            
        HOME = FILE_INFO[2].split('-')[0]
        AWAY = FILE_INFO[2].split('-')[1]
        TEAM = FILE_INFO[4][1:4]

        DATE = FILE_INFO[1]

        for i,row in df.iterrows():
            # COLUMN is sometimes numeric
            try:
                found_player : Players = session.query(Players).filter(Players.fbref_id.contains(str(df.loc[i,'-9999']))).first()
            except:
                found_player : Players = session.query(Players).filter(Players.fbref_id.contains(str(df.loc[i,-9999]))).first()
            
            
            # NOT FOUND PLAYERS are usually players who changed team before the DB scrapping
            if not found_player:
                print(csv)
                print(df.loc[i][[0]])
                not_fp.append([df.loc[i][[0]], TEAM])
            else:

                found_tm : Teams = session.query(Teams).filter(Teams.team_id == found_player.team_id).first()
                # CHECK IF the current player team is the same of the stat
                if found_tm and not TEAM.lower() in found_tm.name.lower():
                    wrong_team.append(f'{TEAM} --> {found_tm.name} | {found_player.name}')
                    
                    # IF NOT, check for team with same TAG
                    found_tm : Teams = session.query(Teams).filter( func.lower(Teams.name).contains(TEAM.lower())).first()
                    if found_tm:
                        wrong_team.pop(-1)

                # IF THERE IS THE TEAM     
                if found_tm:
                    print(csv)
                    print(df) 
                    
                    stat_defense = StatDefense(
                        match_day=MATCHDAY, date=DATE, 
                        home=HOME, away=AWAY, 
                        min=int(df.loc[i,'Min']), 
                        pos=df.loc[i,'Pos'], 
                        team=TEAM,team_id=found_tm.team_id, 
                        player_id=found_player.player_id, player=found_player.name, season=SEASON, league_id=found_tm.league_id, 
                        tkl_A = df.loc[i,'Tkl'][0],
                        tkl_W = df.loc[i,'TklW'],
                        tkl_DEF = df.loc[i,'Def 3rd'][0],
                        tkl_MID = df.loc[i,'Mid 3rd'][0],
                        tkl_ATT = df.loc[i,'Att 3rd'][0],
                        drib_vs_A = df.loc[i,'Att'],
                        drib_vs_Stop = df.loc[i,'Tkl'][1],
                        drib_vs_past = df.loc[i,'Past'],
                        press_A = df.loc[i,'Press'],
                        press_W = df.loc[i,'Succ'],
                        press_DEF = df.loc[i,'Def 3rd'][1],
                        press_MID = df.loc[i,'Mid 3rd'][1],
                        press_ATT = df.loc[i,'Att 3rd'][1],
                        blk = df.loc[i,'Blocks'],
                        blk_SH = df.loc[i,'Sh'],
                        blk_SoT = df.loc[i,'ShSv'],
                        blk_pass = df.loc[i,'Pass'],
                        inter = df.loc[i,'Int'],
                        clr = df.loc[i,'Clr'],
                        err_SH = df.loc[i,'Err']
                    )
                    found_stat : StatDefense = session.query(StatDefense).filter(StatDefense.stat_id == stat_defense.stat_id).first()
                    if not found_stat:
                        session.add(stat_defense)
                        session.commit()
                     
                    elif update: 
                        found_stat.season=SEASON
                        found_stat.min=int(df.loc[i,'Min'])
                        found_stat.pos=df.loc[i,'Pos']
                        found_stat.tkl_A = df.loc[i,'Tkl'][0]
                        found_stat.tkl_W = df.loc[i,'TklW']
                        found_stat.tkl_DEF = df.loc[i,'Def 3rd'][0]
                        found_stat.tkl_MID = df.loc[i,'Mid 3rd'][0]
                        found_stat.tkl_ATT = df.loc[i,'Att 3rd'][0]
                        found_stat.drib_vs_A = df.loc[i,'Att']
                        found_stat.drib_vs_Stop = df.loc[i,'Tkl'][1]
                        found_stat.drib_vs_past = df.loc[i,'Past']
                        found_stat.press_A = df.loc[i,'Press']
                        found_stat.press_W = df.loc[i,'Succ']
                        found_stat.press_DEF = df.loc[i,'Def 3rd'][1]
                        found_stat.press_MID = df.loc[i,'Mid 3rd'][1]
                        found_stat.press_ATT = df.loc[i,'Att 3rd'][1]
                        found_stat.blk = df.loc[i,'Blocks']
                        found_stat.blk_SH = df.loc[i,'Sh']
                        found_stat.blk_SoT = df.loc[i,'ShSv']
                        found_stat.blk_pass = df.loc[i,'Pass']
                        found_stat.inter = df.loc[i,'Int']
                        found_stat.clr = df.loc[i,'Clr']
                        found_stat.err_SH = df.loc[i,'Err']

                        found_stat.last_update = datetime.now()
                        session.commit()
                    

    print(not_fp)
    print(wrong_team)



def stat_possession(update=False, matchday = None):

    csvs = [RAW_FOLDER + x for x in os.listdir(RAW_FOLDER) if 'possession.csv' in x]
    if matchday:
        csvs = [x for x in csvs if f'{matchday})' in x]

    not_fp = []
    wrong_team = []
    for csv in csvs:

        FILE_NAME = csv.split('/')[-1]
        df = pd.read_csv(csv)
        print(df)

        df.columns = (df.columns[:1].tolist() +  df.iloc[0, 1:].tolist())
 
        df = df[1:-1]
         

 
        df = df.fillna(0)
        FILE_INFO = FILE_NAME.split(' ')
        MATCHDAY = FILE_INFO[0].split(')')[0]
            
        HOME = FILE_INFO[2].split('-')[0]
        AWAY = FILE_INFO[2].split('-')[1]
        TEAM = FILE_INFO[4][1:4]

        DATE = FILE_INFO[1]

        for i,row in df.iterrows():
            # COLUMN is sometimes numeric
            try:
                found_player : Players = session.query(Players).filter(Players.fbref_id.contains(str(df.loc[i,'-9999']))).first()
            except:
                found_player : Players = session.query(Players).filter(Players.fbref_id.contains(str(df.loc[i,-9999]))).first()
            
            
            # NOT FOUND PLAYERS are usually players who changed team before the DB scrapping
            if not found_player:
                print(csv)
                print(df.loc[i][[0]])
                not_fp.append([df.loc[i][[0]], TEAM])
            else:

                found_tm : Teams = session.query(Teams).filter(Teams.team_id == found_player.team_id).first()
                # CHECK IF the current player team is the same of the stat
                if found_tm and not TEAM.lower() in found_tm.name.lower():
                    wrong_team.append(f'{TEAM} --> {found_tm.name} | {found_player.name}')
                    
                    # IF NOT, check for team with same TAG
                    found_tm : Teams = session.query(Teams).filter( func.lower(Teams.name).contains(TEAM.lower())).first()
                    if found_tm:
                        wrong_team.pop(-1)

                # IF THERE IS THE TEAM     
                if found_tm:
                    print(csv)
                    print(df) 
                    
                    stat_possession = StatPossession(
                        match_day=MATCHDAY, date=DATE, 
                        home=HOME, away=AWAY, 
                        min=int(df.loc[i,'Min']), 
                        pos=df.loc[i,'Pos'], 
                        team=TEAM,team_id=found_tm.team_id, 
                        player_id=found_player.player_id, player=found_player.name, season=SEASON, league_id=found_tm.league_id, 
                        touch = df.loc[i,'Touches'],
                        touch_live = df.loc[i,'Live'],
                        touch_DEF_PA = df.loc[i,'Def Pen'],
                        touch_DEF = df.loc[i,'Def 3rd'],
                        touch_MID = df.loc[i,'Mid 3rd'],
                        touch_ATT = df.loc[i,'Att 3rd'],
                        touch_ATT_PA = df.loc[i,'Att Pen'],
                        dribs_A = df.loc[i,'Att'],
                        dribs_W = df.loc[i,'Succ'],
                        dribs_n_pl = df.loc[i,'#Pl'],
                        dribs_megs = df.loc[i,'Megs'],
                        ctrl = df.loc[i,'Carries'],
                        ctrl_tot_dist = df.loc[i,'TotDist'],
                        ctrl_prog_dist = df.loc[i,'PrgDist'],
                        ctrl_prog = df.loc[i,'Prog'][0],
                        ctrl_ATT = df.loc[i,'1/3'],
                        ctrl_PA = df.loc[i,'CPA'],
                        ctrl_L = df.loc[i,'Mis'],
                        ctrl_TO = df.loc[i,'Dis'],
                        rec_A = df.loc[i,'Targ'],
                        rec_W = df.loc[i,'Rec'],
                        rec_prog = df.loc[i,'Prog'][1]
                    )
                    found_stat : StatPossession = session.query(StatPossession).filter(StatPossession.stat_id == stat_possession.stat_id).first()
                    if not found_stat:
                        session.add(stat_possession)
                        session.commit()
                     
                    elif update: 
                        found_stat.season=SEASON
                        found_stat.min=int(df.loc[i,'Min'])
                        found_stat.pos=df.loc[i,'Pos']
                        found_stat.touch = df.loc[i,'Touches']
                        found_stat.touch_live = df.loc[i,'Live']
                        found_stat.touch_DEF_PA = df.loc[i,'Def Pen']
                        found_stat.touch_DEF = df.loc[i,'Def 3rd']
                        found_stat.touch_MID = df.loc[i,'Mid 3rd']
                        found_stat.touch_ATT = df.loc[i,'Att 3rd']
                        found_stat.touch_ATT_PA = df.loc[i,'Att Pen']
                        found_stat.dribs_A = df.loc[i,'Att']
                        found_stat.dribs_W = df.loc[i,'Succ']
                        found_stat.dribs_n_pl = df.loc[i,'#Pl']
                        found_stat.dribs_megs = df.loc[i,'Megs']
                        found_stat.ctrl = df.loc[i,'Carries']
                        found_stat.ctrl_tot_dist = df.loc[i,'TotDist']
                        found_stat.ctrl_prog_dist = df.loc[i,'PrgDist']
                        found_stat.ctrl_prog = df.loc[i,'Prog']
                        found_stat.ctrl_ATT = df.loc[i,'1/3']
                        found_stat.ctrl_PA = df.loc[i,'CPA']
                        found_stat.ctrl_L = df.loc[i,'Mis']
                        found_stat.ctrl_TO = df.loc[i,'Dis']
                        found_stat.rec_A = df.loc[i,'Targ']
                        found_stat.rec_W = df.loc[i,'Rec']
                        found_stat.rec_prog = df.loc[i,'Prog']

                        found_stat.last_update = datetime.now()
                        session.commit()
                    

    print(not_fp)
    print(wrong_team)


def stat_performance(update=False, matchday = None):

    csvs = [RAW_FOLDER + x for x in os.listdir(RAW_FOLDER) if 'summary.csv' in x]
    if matchday:
        csvs = [x for x in csvs if f'{matchday})' in x]

    not_fp = []
    wrong_team = []
    for csv in csvs:

        FILE_NAME = csv.split('/')[-1]
        df = pd.read_csv(csv)
        df_misc = pd.read_csv(csv.replace('summary','misc'))
        

        df.columns = (df.columns[:1].tolist() +  df.iloc[0, 1:].tolist())
        df_misc.columns = (df_misc.columns[:1].tolist() +  df_misc.iloc[0, 1:].tolist())
 
        df = df[1:-1]
        df_misc = df_misc[1:-1] 

        print(df)
        print(df_misc)
 
        df = df.fillna(0)
        df_misc = df_misc.fillna(0)
        FILE_INFO = FILE_NAME.split(' ')
        MATCHDAY = FILE_INFO[0].split(')')[0]
            
        HOME = FILE_INFO[2].split('-')[0]
        AWAY = FILE_INFO[2].split('-')[1]
        TEAM = FILE_INFO[4][1:4]

        DATE = FILE_INFO[1]

        for i,row in df.iterrows():
            # COLUMN is sometimes numeric
            try:
                found_player : Players = session.query(Players).filter(Players.fbref_id.contains(str(df.loc[i,'-9999']))).first()
            except:
                found_player : Players = session.query(Players).filter(Players.fbref_id.contains(str(df.loc[i,-9999]))).first()
            
            
            # NOT FOUND PLAYERS are usually players who changed team before the DB scrapping
            if not found_player:
                print(csv)
                print(df.loc[i][[0]])
                not_fp.append([df.loc[i][[0]], TEAM])
            else:

                found_tm : Teams = session.query(Teams).filter(Teams.team_id == found_player.team_id).first()
                # CHECK IF the current player team is the same of the stat
                if found_tm and not TEAM.lower() in found_tm.name.lower():
                    wrong_team.append(f'{TEAM} --> {found_tm.name} | {found_player.name}')
                    
                    # IF NOT, check for team with same TAG
                    found_tm : Teams = session.query(Teams).filter( func.lower(Teams.name).contains(TEAM.lower())).first()
                    if found_tm:
                        wrong_team.pop(-1)

                # IF THERE IS THE TEAM     
                if found_tm:
                    print(csv)
                    print(df.loc[i][[0]])
                    player_misc_df = df_misc[df_misc[df_misc.columns[-1]]== df.loc[i][[-1]].values[0]]
                    print(player_misc_df)
                     
                    stat_performance = StatPerformance(
                        match_day=MATCHDAY, date=DATE, 
                        home=HOME, away=AWAY, 
                        min=int(df.loc[i,'Min']), 
                        pos=df.loc[i,'Pos'], 
                        team=TEAM,team_id=found_tm.team_id, 
                        player_id=found_player.player_id, player=found_player.name, season=SEASON, league_id=found_tm.league_id, 
                        goals = df.loc[i,'Gls'],
                        ast = df.loc[i,'Ast'],
                        PK_A = df.loc[i,'PKatt'],
                        PL_C = df.loc[i,'PK'],
                        SH_A = df.loc[i,'Sh'],
                        Sot = df.loc[i,'SoT'],
                        SCA = df.loc[i,'SCA'],
                        GCA = df.loc[i,'GCA'],
                        offside = player_misc_df.loc[i,'Off'],
                        OG = player_misc_df.loc[i,'OG'],
                        YCard = player_misc_df.loc[i,'CrdY'],
                        RCard = player_misc_df.loc[i,'CrdR'],
                        YCard2 = player_misc_df.loc[i,'2CrdY'],
                        fls_against = player_misc_df.loc[i,'Fld'],
                        fls = player_misc_df.loc[i,'Fls'],
                        PK_W = player_misc_df.loc[i,'PKwon'],
                        PK_conceded = player_misc_df.loc[i,'PKcon'],
                        recoveries = player_misc_df.loc[i,'Recov'],
                        AD_W = player_misc_df.loc[i,'Won'],
                        AD_L = player_misc_df.loc[i,'Lost']
                    )
                    found_stat : StatPerformance = session.query(StatPerformance).filter(StatPerformance.stat_id == stat_performance.stat_id).first()
                    if not found_stat:
                        session.add(stat_performance)
                        session.commit()
                     
                    elif update: 
                        found_stat.season=SEASON
                        found_stat.min=int(df.loc[i,'Min'])
                        found_stat.pos=df.loc[i,'Pos']
                        found_stat.goals = df.loc[i,'Gls']
                        found_stat.ast = df.loc[i,'Ast']
                        found_stat.PK_A = df.loc[i,'PKatt']
                        found_stat.PL_C = df.loc[i,'PK']
                        found_stat.SH_A = df.loc[i,'Sh']
                        found_stat.Sot = df.loc[i,'Sot']
                        found_stat.SCA = df.loc[i,'SCA']
                        found_stat.GCA = df.loc[i,'GCA']
                        found_stat.offside = player_misc_df.loc[1,'Off']
                        found_stat.OG = player_misc_df.loc[1,'OG']
                        found_stat.YCard = player_misc_df.loc[1,'CrdY']
                        found_stat.RCard = player_misc_df.loc[1,'CrdR']
                        found_stat.YCard2 = player_misc_df.loc[1,'2CrdY']
                        found_stat.fls_against = player_misc_df.loc[1,'Fld']
                        found_stat.fls = player_misc_df.loc[1,'Fls']
                        found_stat.PK_W = player_misc_df.loc[1,'PKwon']
                        found_stat.PK_conceded = player_misc_df.loc[1,'PKcon']
                        found_stat.recoveries = player_misc_df.loc[1,'Recov']
                        found_stat.AD_W = player_misc_df.loc[1,'Won']
                        found_stat.AD_L = player_misc_df.loc[1,'Lost']

                        found_stat.last_update = datetime.now()
                        session.commit()
                    

    print(not_fp)
    print(wrong_team)


def fix_player_fbref_id(team_name, player_name, fbref_id):
    team : Teams = session.query(Teams).filter(Teams.name.like(team_name)).first()
    if not team:
        print(f'TEAM NOT FOUND: {team_name}')
    
    player : Players = session.query(Players).filter(Players.name == player_name).first()
    if not player:
        print(f'PALYER NOT FOUND: {player_name}')
    if player.team_id != team.team_id:
        print(f'TEAM ID AND PLAYER\'S TEAM ID ARE DIFFERENT')

    player.fbref_id = fbref_id
    print(player.name)
    print(player.fbref_id)
    input()
    session.commit()


if __name__ == '__main__':
    matchday = 8
    #stat_keeper(matchday=matchday)
    #stat_passing(matchday=matchday)
    #stat_passing_types(matchday=matchday)
    #stat_defense(matchday=matchday)
    #stat_possession(matchday=matchday)
    #stat_performance(matchday=matchday)
    # found_tm : Teams = session.query(Teams).filter( func.lower(Teams.name).contains('ATA'.lower())).first()
    # print(found_tm.name)



 
# Andrea Ranocchia

# Denis Zakaria
# Samuel Di Carmine
# Jacopo Segre
    # fpl = session.query(Players).filter(Players.name == 'José Machín').first()
    # fpl.fbref_id = '7afb1573/Pepin'
    # pl = Players(
    #     name='Panagiotis Retsos',
    #     team_id='',
    #     league_id='',
    #     nation='Greece',
    #     number='#00',
    #     dob='Aug 9, 1998',
    #     height='1,86 m',
    #     position='Centre-Back',
    #     img='https://img.a.transfermarkt.technology/portrait/header/324351-1661523360.jpg?lm=1',
    #     transfermarkt_id='panagiotis-retsos@324351',
    #     diretta_id='retsos-panagiotis/W6dn3O5H/',
    #     fbref_id='4bd00a50/Panagiotis-Retsos'
    # )
    # pl = Players(
    #     name='Adam Ounas',
    #     team_id='',
    #     league_id='',
    #     nation='Algeria',
    #     number='#00',
    #     dob='Nov 11, 1996',
    #     height='1,72 m',
    #     position='Right Winger',
    #     img='https://img.a.transfermarkt.technology/portrait/header/400485-1661764685.jpg?lm=1',
    #     transfermarkt_id='adam-ounas@400485',
    #     diretta_id='ounas-adam/EBaunUhF/',
    #     fbref_id='ed90babd/Adam-Ounas'
    # )
    # pl = Players(
    #     name='Andrea Ranocchia',
    #     team_id='',
    #     league_id='',
    #     nation='Italy',
    #     number='#00',
    #     dob='Feb 16, 1988',
    #     height='1,95 m',
    #     position='Centre-Back',
    #     img='https://img.a.transfermarkt.technology/portrait/header/44327-1663659408.jpg?lm=1',
    #     transfermarkt_id='andrea-ranocchia@44327',
    #     diretta_id='ranocchia-andrea/S8endwQ4/',
    #     fbref_id='539230cf/Andrea-Ranocchia'
    # )
    
    # pl = Players(
    #     name='Denis Zakaria',
    #     team_id='',
    #     league_id='',
    #     nation='Switzerland',
    #     number='#00',
    #     dob='Nov 20, 1996',
    #     height='1,91 m',
    #     position='Defensive Midfield',
    #     img='https://img.a.transfermarkt.technology/portrait/header/334526-1644234041.jpg?lm=1',
    #     transfermarkt_id='denis-zakaria@334526',
    #     diretta_id='zakaria-denis/d23lOQrL/',
    #     fbref_id='384d58d9/Denis-Zakaria'
    # )
    
    # pl = Players(
    #     name='Samuel Di Carmine',
    #     team_id='',
    #     league_id='',
    #     nation='Italy',
    #     number='#00',
    #     dob='Sep 29, 1988',
    #     height='1,87 m',
    #     position='Centre-Forward',
    #     img='https://img.a.transfermarkt.technology/portrait/header/45389-1558939633.jpg?lm=1',
    #     transfermarkt_id='samuel-di-carmine@45389',
    #     diretta_id='di-carmine-samuel/MDcaUm5C/',
    #     fbref_id='ef94dc2f/Samuel-Di-Carmine'
    # )
    # pl = Players(
    #     name='Jacopo Segre',
    #     team_id='',
    #     league_id='',
    #     nation='Italy',
    #     number='#00',
    #     dob='Feb 17, 1997',
    #     height='1,85 m',
    #     position='Central Midfield',
    #     img='https://img.a.transfermarkt.technology/portrait/header/373899-1613461826.jpg?lm=1',
    #     transfermarkt_id='jacopo-segre@373899',
    #     diretta_id='segre-jacopo/fa6CHtxA/',
    #     fbref_id='3cb132e6/Jacopo-Segre'
    # )
    # session.add(pl)
    # session.commit()
   
    #print(session.query(Teams).filter(Teams.name == 'US Salernitana 1919').first().team_id)
    #
    # input()
    # pl = Players(
    #     name='Julius Beck',
    #     team_id='64c0bf5-e435-310a-abf0-2dfa6e1ebf78',
    #     league_id='c8b561b1-9175-3808-a40b-78330d8e53f4',
    #     nation='Denmark',
    #     number='#16',
    #     dob='Apr 27, 2005',
    #     height='',
    #     position='Central Midfield',
    #     img='https://img.a.transfermarkt.technology/portrait/header/default.jpg?lm=1',
    #     transfermarkt_id='julius-beck@802512',
    #     diretta_id='segre-jacopo/fa6CHtxA/',
    #     fbref_id='e892c325/Julius-Beck'
    # )
    # session.add(pl)
    # session.commit()



# [[Unnamed: 0    Matteo Lovato
# Name: 12, dtype: object, 'SAL'], [Unnamed: 0    Julius Beck
# Name: 10, dtype: object, 'SPE'], [Unnamed: 0    Kelvin Amian
# Name: 15, dtype: object, 'SPE'], [Unnamed: 0    Giulio Donati
# Name: 11, dtype: object, 'MON']]
# []

    # fix_player_fbref_id('Spezia Calcio', 'Kelvin Amian','bcc81786/Kelvin-Amian')
    
    # fix_player_fbref_id('US Salernitana 1919', 'Matteo Lovato','5fa57166/Matteo-Lovato')
    # fix_player_fbref_id('AC Monza', 'Giulio Donati','22051fbe/Giulio-Donati')