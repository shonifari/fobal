from cmath import rect
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go  

def main(): 
	DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
	engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)

	conn = engine.connect()
	
	team = 'Udinese'
	query = f'''
	SELECT * FROM stat_performance WHERE team_id IN 
   	(SELECT team_id FROM teams WHERE name LIKE '%{team}%')
	'''
	df = pd.read_sql(query, con=conn)
	print(df)
	df = df.groupby(['match_day'], as_index = False).sum()
	print(df)

	for i,row in df.iterrows():
		print(f'''{df.loc[i,'match_day']}) 
SH_A: {df.loc[i,'SH_A']}
SoT: {df.loc[i,'Sot']}
Accurcy:{round(df.loc[i,'Sot'] * 100 / df.loc[i,'SH_A'], 2)}%
			''')

	print(f'''TOTALE
SH_A: {df.sum()['SH_A']}
SoT: {df.sum()['Sot']}
Accurcy:{round(df.sum()['Sot'] * 100 / df.sum()['SH_A'], 2)}%
			''')
	sot =  df.sum()['Sot']
	sh_off = df.sum()['SH_A'] - sot
	fig = go.Figure(data=[go.Pie(labels=[f'({sot}) - Shots on target',f'({sh_off}) - Shots out of targe'], values=[sot, sh_off], hole=.9)])
	fig.show()


def main2(): 
	DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
	engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)

	conn = engine.connect()
	
	team = 'Udinese'
	query = f'''
	SELECT * FROM stat_performance
	'''
	df = pd.read_sql(query, con=conn)
	print(df)
	df = df.groupby(['player'], as_index = False).sum()
	
	marcatori = df.sort_values(by=['goals'], ascending=False)[:25]
	print(marcatori)
	fig = go.Figure(go.Bar(x=marcatori['player'], y=marcatori['goals'], name='Montreal'))
	fig.show()
	
	assist_man = df.sort_values(by=['ast'], ascending=False)[:25]
	print(assist_man)
	fig = go.Figure(go.Bar(x=assist_man['player'], y=assist_man['ast'], name='Montreal'))
	fig.show()

	# assist_man = df.sort_values(by=['ast'], ascending=False)[:25]
	# print(assist_man)
	# fig = go.Figure(go.Bar(x=assist_man['player'], y=assist_man['ast'], name='Montreal'))
	# fig.show()
	
def main3(): 
	DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
	engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)

	conn = engine.connect()
	 
	query = f'''
	SELECT * FROM stat_passing
	'''
	df = pd.read_sql(query, con=conn)
	print(df)

	df = df.groupby(['team'], as_index = False).sum()
	print(df)
	
	import plotly.express as px
	
	fig = px.scatter_3d(df, x='pass_long_A', y='pass_med_A', z='pass_short_A',
				color='pass_A', size='pass_A', size_max=18,
				symbol='team', opacity=0.7)
	fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
	# fig = go.Figure(data=[go.Scatter3d(x=df['pass_long_A'], y=df['pass_med_A'], z=df['pass_short_A'],
    #                                mode='markers', size=df['pass_A'])])
	fig.show()
	 
def main4(): 
	DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
	engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)

	conn = engine.connect()
	 
	query = f'''
	SELECT * FROM stat_performance
	'''
	df = pd.read_sql(query, con=conn)
	print(df)

	df = df.groupby(['team'], as_index = False).sum()
	print(df)
	
	import plotly.express as px

	fig = px.scatter(df, x="goals", y="Sot", color='SH_A', size='goals' , text='team', )
	# fig = go.Figure(data=[go.Scatter3d(x=df['pass_long_A'], y=df['pass_med_A'], z=df['pass_short_A'],
    #                                mode='markers', size=df['pass_A'])])
	fig.show()
	 
def main5(): 
	DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
	engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)

	conn = engine.connect()
	 
	query = f'''
	SELECT * FROM stat_possession
	'''
	df = pd.read_sql(query, con=conn)
	print(df)

	pls_df = df.groupby(['player','team','pos'], as_index = False).sum()

	pls_df = pls_df[~pls_df['pos'].astype(str).isin(['CB','LB', 'RB']) ]

	def percs(df):
		return round(100 * df['rec_W'] / df['rec_A'], 2)

	pls_df = pls_df.assign(perc=lambda x: percs(x))
	pls_df = pls_df.sort_values(by='rec_A', ascending=False).head(100)
	pls_df = pls_df.sort_values(by='perc', ascending=False)

	print(pls_df.loc[:, ['player','team','pos', 'rec_A', 'rec_W', 'perc']])
	import plotly.express as px
	fig = px.scatter(pls_df, x="rec_A", y="rec_W", color='pos' ,size='perc', text='pos',  )
	
	fig.show()
	 
 
	 
def main6(): 
	DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
	engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)

	conn = engine.connect()
	 
	query = f'''
	SELECT * FROM stat_possession
	'''
	df = pd.read_sql(query, con=conn)
	print(df)

	pls_df = df.groupby(['player','team','pos'], as_index = False).sum()

	#pls_df = pls_df[~pls_df['pos'].astype(str).isin(['CB','LB', 'RB']) ]

	def percs(df):
		return round(100 * df['ctrl_prog_dist'] / df['ctrl_tot_dist'], 2)

	pls_df = pls_df.assign(perc=lambda x: percs(x))
	pls_df = pls_df.sort_values(by='ctrl_tot_dist', ascending=False).head(10)
	pls_df = pls_df.sort_values(by='perc', ascending=False)

	print(pls_df.loc[:, ['player','team','pos', 'ctrl_tot_dist', 'ctrl_prog_dist', 'perc']])
	import plotly.express as px
	fig = px.scatter(pls_df, x="ctrl_tot_dist", y="ctrl_prog_dist", color='pos' ,size='perc', text='player',  )
	
	fig.show()
	 
def main7(): 
	DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
	engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)

	conn = engine.connect()
	 
	team = 'Roma'
	query = f'''
	SELECT * FROM stat_performance WHERE team_id IN 
   	(SELECT team_id FROM teams WHERE name LIKE '%{team}%')
	'''
	df = pd.read_sql(query, con=conn)
	print(df)

	df = df.groupby(['match_day'], as_index = False).sum()
	print(df)

	return
	#pls_df = pls_df[~pls_df['pos'].astype(str).isin(['CB','LB', 'RB']) ]

	def percs(df):
		return round(100 * df['ctrl_prog_dist'] / df['ctrl_tot_dist'], 2)

	pls_df = pls_df.assign(perc=lambda x: percs(x))
	pls_df = pls_df.sort_values(by='ctrl_tot_dist', ascending=False).head(10)
	pls_df = pls_df.sort_values(by='perc', ascending=False)

	print(pls_df.loc[:, ['player','team','pos', 'ctrl_tot_dist', 'ctrl_prog_dist', 'perc']])
	import plotly.express as px
	fig = px.scatter(pls_df, x="ctrl_tot_dist", y="ctrl_prog_dist", color='pos' ,size='perc', text='player',  )
	
	fig.show()
	 
def main8(): 
	DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
	engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)

	conn = engine.connect()
	 
	query = f'''
	SELECT * FROM stat_passing_type
	'''
	df = pd.read_sql(query, con=conn)
	print(df)

	df = df.groupby(['team_id','team'], as_index = False).sum()

	print(df)
	
	
	import plotly.express as px
	
	fig = px.bar(df, x="team", y=["pass_ground", "pass_low", "pass_high"],
	title="Passes Ground/Low/High" , text_auto=True,
	  opacity=0.7,
    color_discrete_map={
        'pass_ground' : 'green',
		'pass_low' : 'orange',
		'pass_high' : 'blue',
    }
	)
	
	fig.update_traces(width=1)


	img_width = 139
	img_height = 181
	scale_factor = 1
	adj_logo = 0.2
	from PIL import Image
	for i,row in df.iterrows(): 
		fig.add_layout_image(
			dict(
        x=i - adj_logo,
        sizex=img_width * scale_factor, 
        y=img_height * scale_factor,
        sizey=img_height * scale_factor,
        xref="x",
        yref="y",
        opacity=1.0,
        layer="above",

        source=Image.open(f"/Users/karis/dev/Python/fobal/res/image/data/teams/{df.loc[i,'team_id']}.png")
		)
				
		)

		fig.add_layout_image(
			dict(
        x=i - adj_logo,
        y=img_height * scale_factor  + df.loc[i,'pass_ground'] + df.loc[i,'pass_low'] + df.loc[i,'pass_high']
		,
        sizex=img_width * scale_factor, 
        sizey=img_height * scale_factor,
        xref="x",
        yref="y",
        opacity=1.0,
        layer="above",

        source=Image.open(f"/Users/karis/dev/Python/fobal/res/image/data/teams/{df.loc[i,'team_id']}.png")
		)
				
		)
	
		# fig.add_layout_image(
		# 	dict(
        # x=i - 0.5,
       	# y= df.loc[i,'pass_ground'],
        
		# sizex=1, 
        # sizey=df.loc[i,'pass_ground'],
        
        
        # xref="x",
        # yref="y",
        # opacity=0.3,
        # layer="below",
		# sizing="fill",
 
        #  source=Image.open(f"/Users/karis/Downloads/666594.d4b9899-970x546.jpg")
         
		# )
				
		# )

		# fig.add_layout_image(
		# 	dict(
        # x=i - 0.5,
       	# y= df.loc[i,'pass_ground'] + df.loc[i,'pass_low']  ,
        
		# sizex=1, 
        # sizey=df.loc[i,'pass_low'],
        
        
        # xref="x",
        # yref="y",
        # opacity=0.3,
        # layer="below",
		# sizing="fill",
 
        #  source=Image.open(f"/Users/karis/Downloads/https---greenstreethammers.com-wp-content-uploads-getty-images-2017-07-1388451931.jpeg")
		# )
				
		# )
	
		# ###
		# fig.add_layout_image(
		# 	dict(
        # x=i - 0.5,
       	# y= df.loc[i,'pass_ground'] + df.loc[i,'pass_low'] + df.loc[i,'pass_high'],
        
		# sizex=1, 
        # sizey=df.loc[i,'pass_high'],
        
        
        # xref="x",
        # yref="y",
        # opacity=0.3,
        # layer="below",
		# sizing="fill",
 
        #  source=Image.open(f"/Users/karis/Downloads/80213720_10158158516858598_8706583962434142208_n.jpg")
		# )
				
		# )

 

	fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
	fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
	fig.update_layout(
		#font_color= 'white',
		font_size=24)
	fig.show()

if __name__ =="__main__":
	main8()
