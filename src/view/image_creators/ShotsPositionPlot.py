import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
import sys
from typing import List

# ADD THE SRC FOLDER TO THE SYS PATH
# ADD THE SRC FOLDER TO THE SYS PATH
APP_FOLDER = str(Path(Path(Path(Path(__file__).parent.absolute()).parent.absolute()).parent.absolute()).parent.absolute())
sys.path.insert(0, APP_FOLDER) 

from src.model.db.tables.Fixtures import Fixtures
from src.model.db.tables.ShotsPosition import ShotsPositions
from src.model.db.database import session

import plotly.graph_objects as go
from PIL import Image

# def mutate_axis(value, axis_x = True, home = True) -> float:
#         if axis_x :
#             if not home : value = 1 - value
#             return value * 135
#         else:
#             if not home : value = 1 - value                               
#             return value * 95

def mutate_axis_x(_df   ) -> float:
    return _df * 135
        
            
            
         
def mutate_axis_y(_df  , axis_x = True) -> float:
    return _df * 95
                            


def plot(df):
 
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x= df['X'],
                y=df['Y'],
                mode='markers',
                text=df['player'],
                marker=dict(size=15,
                color=df['is_goal'],
                
                ),
                    
        ))

        #axis hide、yaxis reversed
        fig.update_layout(
            autosize=False,
            width=1163,
            height=783,
            xaxis=dict(visible=True,autorange=False),
            yaxis=dict(visible=True,autorange=False)
        )
        fig.update_traces(textposition='top center')
        
        # Set templates
        #fig.update_layout(template="plotly_white")
        
        fig.update_xaxes(range=[0,135])
        fig.update_yaxes(range=[95,0])    

        fig.add_layout_image(
            dict(
            x=0,
            y=0,
            sizex=135, 
            sizey=95,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source=Image.open(f"/Users/karis/dev/Python/fb_analysis/rsrc/Posts/Resources/Field.png")
            )
                    
            )

      
        fig.show()






if __name__ == '__main__':

    DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
    engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)

    conn = engine.connect()
        
    team = 'Lazio'
    matchday = 8

    query = f'''
    SELECT * FROM shots_positions WHERE fixture_id IN 
    (SELECT fixture_id FROM fixtures 
        WHERE home LIKE '%{team}%' 
        AND matchday is {matchday}
        )
    '''
    df = pd.read_sql(query, con=conn)
    print(df)
    print(df.columns)


    df.insert(0,'is_goal',0)
    home = df['home'].values[0]
    away = df['away'].values[0]
    for i,row in df.iterrows():
        team = df.loc[i,'team']
        val = df.loc[i,'X'] if team == home else 1 - df.loc[i,'X']
        df.loc[i,'X'] = mutate_axis_x(val)  
        val = 1 - df.loc[i,'Y'] if team == home else df.loc[i,'Y']
        df.loc[i,'Y'] = mutate_axis_y(val)  
        
        res = df.loc[i,'result']

        if res == 'OwnGoal':
            df.loc[i,'is_goal'] = 0
        if res == 'MissedShots':
            df.loc[i,'is_goal'] = 1
        if res == 'SavedShot':
            df.loc[i,'is_goal'] = 2
        if res == 'BlockedShot':
            df.loc[i,'is_goal'] = 3
        if res == 'Goal':
            df.loc[i,'is_goal'] = 5
     
    
    print(df['team'])
    print(df[['team','X','Y']])
    plot(df)
    print(df['understat_link'])
        