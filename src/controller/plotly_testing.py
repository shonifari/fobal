from PIL import Image
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go




def shot_accuracy(): 
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
	Accuracy:{round(df.sum()['Sot'] * 100 / df.sum()['SH_A'], 2)}%
			''')
	sot =  df.sum()['Sot']
	sh_off = df.sum()['SH_A'] - sot
	fig = go.Figure(data=[go.Pie(labels=[f'({sot}) - Shots on target',f'({sh_off}) - Shots out of targe'], values=[sot, sh_off], hole=.9)])
	fig.show()


def goals(): 
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
	
def passes(): 
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
	 
def goal_shots_attempts(): 
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
	 
def ball_reception(): 
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
	 
 
	 
def ball_control(): 
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
	 

	 
def pass_types(): 
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




def field_section_played():
	import numpy as np


	DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
	engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)

	conn = engine.connect()
	 
	query = f'''
	SELECT * FROM stat_possession
	'''
	df = pd.read_sql(query, con=conn)
	print(df)

	df = df.groupby(['fixture_id','team'], as_index = False).sum()

	print(df)
	 
	ids = set(df['fixture_id'].values)
	print(ids)
	for fix_id in ids:
		df = df.loc[(df['fixture_id'] == fix_id)]
		break
	
	
	print(df)
	 
	df.index = [0,1]

	labels = ["DEF","MID","ATT"]
	widths = np.array([27,46,27])
	
	DEF_TOT = df.loc[0,'touch_DEF_PA'] + df.loc[0,'touch_DEF'] + df.loc[1,'touch_DEF_PA'] + df.loc[1,'touch_DEF']
	MID_TOT = df.loc[0,'touch_MID'] + df.loc[1,'touch_MID']
	ATT_TOT = df.loc[0,'touch_ATT'] + df.loc[0,'touch_ATT_PA'] +	df.loc[1,'touch_ATT'] + df.loc[1,'touch_ATT_PA']

	HOME_DEF_PERC =  round((df.loc[0,'touch_DEF_PA'] + df.loc[0,'touch_DEF']) * 100 / DEF_TOT , 2)
	HOME_MID_PERC =  round((df.loc[0,'touch_MID']) * 100 / MID_TOT , 2)
	HOME_ATT_PERC =  round((df.loc[0,'touch_ATT_PA'] + df.loc[0,'touch_ATT']) * 100 / ATT_TOT , 2)

	AWAY_DEF_PERC =  round((df.loc[1,'touch_DEF_PA'] + df.loc[1,'touch_DEF']) * 100 / DEF_TOT , 2)
	AWAY_MID_PERC =  round((df.loc[1,'touch_MID']) * 100 / MID_TOT , 2)
	AWAY_ATT_PERC =  round((df.loc[1,'touch_ATT_PA'] + df.loc[1,'touch_ATT']) * 100 / ATT_TOT , 2)

	 

	data = {
		df.loc[0,'team']: [HOME_DEF_PERC, HOME_MID_PERC, HOME_ATT_PERC],
		df.loc[1,'team']: [AWAY_DEF_PERC, AWAY_MID_PERC, AWAY_ATT_PERC]
		
	}
	

	fig = go.Figure()
	for key in data:
		fig.add_trace(go.Bar(
			name=key,
			y=data[key],
			x=np.cumsum(widths)-widths,
			width=widths,
			offset=0,
			opacity=1,
			customdata=np.transpose([labels, widths*data[key]]),
			texttemplate="%{y}",
			textposition="inside",
			textangle=0,
			textfont_color="white",
			hovertemplate="<br>".join([
				"label: %{customdata[0]}",
				"width: %{width}",
				"height: %{y}",
				"area: %{customdata[1]}",
			])
		))

	fig.update_xaxes(
		tickvals=np.cumsum(widths)-widths/2,
		ticktext= ["%s<br>%d" % (l, w) for l, w in zip(labels, widths)]
	)

	fig.update_xaxes(range=[0,100])
	fig.update_yaxes(range=[0,100])

	fig.update_layout(
		title_text="Marimekko Chart",
		barmode="stack",
		uniformtext=dict(mode="hide", minsize=10),
	)

 
	fig.add_layout_image(
			dict(
        x=0,
        y=100,
        sizex=100, 
        sizey=100,
        xref="x",
        yref="y",
        opacity=1.0,
        layer="above",
		sizing="stretch",
        source=Image.open(f"/Users/karis/dev/Python/fb_analysis/rsrc/Posts/Resources/Field.png")
		)
				
		)

	fig.update_layout(
		#font_color= 'white',
		font_size=24)
	fig.show()



if __name__ =="__main__":
	field_section_played()
