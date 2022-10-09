
from pathlib import Path
import sys

# ADD THE SRC FOLDER TO THE SYS PATH
# ADD THE SRC FOLDER TO THE SYS PATH
APP_FOLDER = str(Path(Path(Path(Path(__file__).parent.absolute()).parent.absolute()).parent.absolute()).parent.absolute())
sys.path.insert(0, APP_FOLDER) 

import json 
import os
from typing import Dict, List
from PIL import ImageFont
from PIL import ImageDraw 
from PIL import Image, ImageOps
import numpy as np
import pandas as pd


from src.view.image_creators.img_utils import draw_ellipse

example = {0: {0: ['Tatarusanu'], 1: ['Davide Calabria', 'Kjaer', 'Tomori', 'Ballo Toure'], 2: ['Tonali', 'Kessie'], 3: ['Diaz', 'Krunic', 'Leao'], 4: ['Ibrahimovic']}, 1: {0: ['Handanovic'], 1: ['Skriniar', 'de Vrij', 'Bastoni'], 2: ['Darmian', 'Barella', 'Brozovic', 'Calhanoglu', 'Perisic'], 3: ['Dzeko', 'Martinez']}}

H2H_BGD_PATH = '/Users/karis/dev/Python/fb_analysis/rsrc/Posts/Resources/H2H - bgd.png'
LOGOS_FOLDER_PATH = '/Users/karis/dev/Python/fb_analysis/rsrc/Teams/Serie A/Logos/2122/'
PLAYER_ICONS_FOLDER = '/Users/karis/dev/Python/fb_analysis/rsrc/Teams/Serie A/Players Images/2122/'
ANONYMOUS_PLAYER_ICON = '/Users/karis/dev/Python/fb_analysis/rsrc/anonymous player.png'
MATCH_EVENT_ICONS = '/Users/karis/dev/Python/fb_analysis/rsrc/Posts/Resources/Match game icons/'
TEAM_COLORS ={'Fiorentina' : '482E92',
'Milan':'FB090B',
'Roma':'feb42f',
'Atalanta':'0071bc',
'Cagliari':'1d1e23',
'Juventus':'bbbbba',
'Napoli':'12A0D7',
'Lazio':'b0d0ff',
'Torino':'8A1E03',
'Udinese':'7F7F7F',
'Sassuolo':'00A752',
'Genoa':'AD1919',
'Hellas Verona':'FFE74A',
'Empoli':'00579C',
'Bologna':'1A2F48',
'Inter':'010E80',
'Venezia':'E3791C',
'Spezia':'746D56',
'Salernitana':'71211A',
'Sampdoria':'1B5497',}


LIVE_RESULTS_FOLDER = '/Users/karis/dev/Python/fb_analysis/data/Serie A/2122/CSVs/Output/Live Match Results/'
LINEUPS_JSON_PATH = '/Users/karis/dev/Python/fb_analysis/data/Serie A/2122/lineups.json'

class Lineup:
    '''
    asòkda
    '''
    def __init__(self, match) -> None:
        
        self.fixture_id = None
        self.fixture = None
        self.home = None     
        self.away = None     
        
        self.matchday : int = None


        self.match = match
        self.matchday = int(match.Giornata)

        self.home_tag = self.match.Home[:3].upper()
        if self.home_tag == 'VER':
            self.home_tag = 'HEL'
        self.away_tag = self.match.Away[:3].upper()
        if self.away_tag == 'VER':
            self.away_tag = 'HEL'
        
        
        
        _match_path = LIVE_RESULTS_FOLDER + f'Matchday {self.matchday}/{self.home_tag}-{self.away_tag}.csv'
        self.match_events = pd.read_csv(_match_path)  
         


        with open(LINEUPS_JSON_PATH, 'r', encoding='utf-8') as f:
            self.lineups = json.load(f)['lineups'][str(self.matchday)][f'{self.home_tag}-{self.away_tag}']
        
        self.omonimus_player = set()

    def check_omonimus_player(self, name):
        if name == 'Coulibaly':
            if name in self.omonimus_player:
                self.omonimus_player = set()
                return 'Lassana Coulibaly' 
                
            else: 
                self.omonimus_player.add(name)
                return 'Mamadou Coulibaly'
        if name == 'Anderson':
                if name in self.omonimus_player:
                    self.omonimus_player = set()
                    return 'Felipe Anderson' 
                    
                else: 
                    self.omonimus_player.add(name)
                    return 'Anderson Lima'


    # FIELD IMAGE
    def field(self) -> Image:
        return Image.open('/Users/karis/dev/Python/fb_analysis/rsrc/Posts/Resources/Field.png')
    
    # FIND PLAYER
    def _find_player(self, name : str, team : str) -> str:
        ''' Checks for Player images with the given name and returns the full name
            name = 'Calabria'
            team = 'MIL'
            return -> 'Davide Calabria'
        '''
        _players = [f for f in os.listdir(PLAYER_ICONS_FOLDER) if team in f]
          

        if len(name.split(' ')) > 1 and '.' in name:
            name = name.split(' ')[-1] if not '.' in name.split(' ')[-1] else name.split(' ')[0]
       
        _player = [f for f in _players if name in f]

        if len(_player) == 0:
            print('Name not found in images:' + name)
            return name
        
        else:
            if len(_player) == 1:
                return _player[0]
            
            
            else:
                # Check for players like Rui that is contained in Fabian Ruiz
                _similar_player = [f for f in _player if name + ' ' in f]
                if len(_similar_player) == 1:
                    return _player[0]
    
                

                elif len(name.split(' ')) > 1:
                    name_initial = name.split(' ')[-1].replace('.','')

                    for player in _player:
                        if player.split(' ')[0][0] == name_initial:
                            return player
                else:
                    return self.check_omonimus_player(name)

 
        




    def _get_visual_name(self,name : str) -> str:
        while name[-1] == ' ':
            name = name[:-1]
 

        if len(name.split(' ')) > 1:
            first_name = name.split(' ')[0]
            first_name = first_name[0].upper() + '.'
            second_name = ' '.join(name.split(' ')[1:])
            return first_name + ' ' + second_name
        else:
            return name
            

        

    def _player_icon(self, name, team) -> Image: 

        # GET TEAM COLOR
        color =[ f for f in TEAM_COLORS.keys() if f[:3].upper() == team][0]
        color = TEAM_COLORS[color]

        # GET PALYER ICON
        try:
            icon = Image.open(PLAYER_ICONS_FOLDER + name).resize( (72,72), Image.ANTIALIAS).convert("RGB")
        except:
            icon = Image.open(ANONYMOUS_PLAYER_ICON).resize( (72,72), Image.ANTIALIAS)
        
        # CREATE EMPTY IMAGE AS BASE
        img = Image.new('RGBA', (80, 80), (255,255,255,255))
        img.paste(icon,(4,4))
        
        # DRAW ELLIPSE
        ellipse_box = [2, 2, 78, 78]
        draw_ellipse(img, ellipse_box, outline=f'#{color}', width=5)  
       
        h,w=img.size

        # Create same size alpha layer with circle
        mask = Image.new('L', img.size,0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([0,0,h - 0.1,w - 0.1],0,360,fill=255)
        
        
        output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)

        return output


    def _player_box(self, name, team) -> Image:

        # GET PLAYER EVENTS
        print(self.match_events)
        player_events = self.match_events[(self.match_events['Player'].str.contains(name)) | (self.match_events['Info'].str.contains(name))]
 
        name = self._find_player(name, team)
        player_icon = self._player_icon(name, team)
        icon = Image.new('RGBA',(80 + 20, 80 + 20))#, (100,100,100,255))
        icon.paste(player_icon,(10,10), player_icon)
        
        
        
        # ADD PLAYER EVENTS ICON
         
        if len(player_events) > 0:
            for i, row in player_events.iterrows():
                 
                if not row.Event in ['Subs', 'Missed Pen', 'Pen Made']:
                    icn = None
                    pos = (0,0)
                    if row.Event == 'Goal':
                         
                        if name.split(' ')[1] in str(row.Player):
                            icn = Image.open(MATCH_EVENT_ICONS + row.Event +'.png').resize((35,35), Image.ANTIALIAS) 
                            pos = (0,0)
                        
                    elif row.Event == 'Own Goal':
                        icn = Image.open(MATCH_EVENT_ICONS + row.Event +'.png').resize((35,35), Image.ANTIALIAS) 
                        pos = (0,55)
                         

                    
                    elif 'Card' in row.Event:
                        pos = (68,0)
                        icn = Image.open(MATCH_EVENT_ICONS + row.Event +' - lineup.png').resize((35,35), Image.ANTIALIAS)
                    


                    if icn:
                        icon.paste(icn, pos, icn)
                
                
                elif row.Event == 'Subs':
                    icn = Image.open(MATCH_EVENT_ICONS + 'Sub_OUT.png').resize((40,40), Image.ANTIALIAS) 
                    pos = (66,60)
                        
                    icon.paste(icn, pos, icn)
        
        
        
        
        
        
        short_name = self._get_visual_name(name.split('(')[0])
         
         
        
        # PLACE NAME
        font = ImageFont.truetype("/Library/fonts/SF-Pro-Text-Bold.otf",20)
        text_w,h = font.getsize(short_name)
        if text_w < 100:
            w = 100
        else:
            w = text_w
        

        img = Image.new('RGBA',(w, h + 100))
        draw = ImageDraw.Draw(img)    
        
        img.paste(icon, ((w // 2) - 50, 0), icon)

        icon_w, icon_h = icon.size
        text_x = int((w / 2) - ( text_w / 2))
        draw.text((text_x, 90), short_name,(255,255,255),font=font)

        box = Image.new('RGBA',(text_w, h + icon_w) , (50,50,50,255))

        box.paste(img,(10,10), img)
        

        

        return img

    

    def _substitute_player_box(self, sub_in, sub_out, team) -> Image:
        

        # GET PLAYER EVENTS
        player_events = self.match_events[(self.match_events['Player'] == sub_in) & (self.match_events['Event'] != 'Subs')]

        sub_in = self._find_player(sub_in, team)
        in_icon = self._player_icon(sub_in, team)
        icon_w,icon_h = in_icon.size
        short_name = self._get_visual_name(sub_in.split('(')[0])
        
        
        
        box_w =  260
        padding = 7
        fits = False
        font_size = 24

        # BASE IMAGE
        img = Image.new('RGBA',(box_w, icon_h) )
        draw = ImageDraw.Draw(img)   

        # PASTE ICON
        img.paste(in_icon, (0, 0), in_icon)


        # GET FONT SIZE FOR SUB IN NAME
        while not fits:
            font = ImageFont.truetype("/Library/fonts/SF-Pro-Text-Bold.otf",font_size)
            w,h = font.getsize(short_name)
            total_w = w + padding + icon_w
            if total_w <= box_w:
                fits = True
            else:
                font_size -= 2
        
        # ADD SUB IN NAME
        draw.text((padding + icon_w, 8.5), short_name,(255,255,255,255),font=font)




        sub_icon_size = 35  
        sub_icon = Image.open('/Users/karis/dev/Python/fb_analysis/rsrc/Posts/Resources/Match game icons/Sub_IN.png').resize((sub_icon_size,sub_icon_size), Image.ANTIALIAS)
        # PASTE ICON
        img.paste(sub_icon, (padding + icon_w, 43), sub_icon)
        
        # GET NAME
        sub_out = self._find_player(sub_out, team)
        out_short_name = self._get_visual_name(sub_out.split('(')[0])
        if out_short_name[-1] == ' ':
            out_short_name = out_short_name[:-1]
        out_short_name = f'({out_short_name})'
        
        
        # GET FONT SIZE FOR SUB IN NAME
        font_size = 20
        fits = False
        while not fits:
            font = ImageFont.truetype("/Library/fonts/SF-Pro-Text-Bold.otf",font_size)
            w,h = font.getsize(out_short_name)
            total_w = w + padding + icon_w + sub_icon_size
            if total_w <= box_w:
                fits = True
            else:
                font_size -= 2


        # ADD SUB OUT NAME
        draw.text((padding + icon_w + sub_icon_size, 43), out_short_name,(173,173,173),font=font)

        # CREATE ROW BOX
        final_box = Image.new('RGBA', (281,108),)
        draw = ImageDraw.Draw(final_box)

        final_box.paste(img,(20,18), img)


        # ADD PLAYER EVENTS ICON
        if len(player_events) > 0:
            for i, row in player_events.iterrows():
                icn = Image.open(MATCH_EVENT_ICONS + row.Event +'.png').resize((40,40), Image.ANTIALIAS) 
                pos = (0,0)
                if row.Event == 'Goal':
                    pos = (0,10)
                elif row.Event == 'Own Goal':
                    pos = (0,10)
                
                elif 'Card' in row.Event:
                    pos = (75,10)
                    icn = Image.open(MATCH_EVENT_ICONS + row.Event +' - lineup.png').resize((35,35), Image.ANTIALIAS)

                
                icn = icn
                final_box.paste(icn, pos, icn)
         



        
        
        separator = Image.new('RGBA', (261,2), (55,92,121))
        
        final_box.paste(separator,(20,106), separator)


        return final_box




    def _create_subs(self) -> Image:
        subs = []
        
        home = self.match_events['Home'].values[0]
        away = self.match_events['Away'].values[0]
         
        
        for  tag, team in zip([self.home_tag, self.away_tag], [home, away]):
             
            df = self.match_events[(self.match_events['Team'] == team ) & (self.match_events['Event'] == 'Subs')]
            
            bgd = Image.new('RGBA',(281,540))
            y = 0
            
            for i, sub in df.iterrows():
                box = self._substitute_player_box(sub.Player, sub.Info, tag)
                bgd.paste(box,(0, y),box)
                y += 108
            
            subs.append(bgd)
        
        return subs[0], subs[1]

    def _create_lineup(self, to_return = None) -> Image:
        
        _lineups   = []
        
        for i, team in enumerate([self.home_tag,self.away_tag]):
            _field = self.field()
            
            squad = self.lineups[str(i)]
            
            sections = len(squad)
            w,h = _field.size
            vertical_padding = 10
            box_size = 120
            if i == 0:
                x = 11
                
                for section in squad.keys():
                    
                    _players = squad[section]

                    boxes_h = box_size * len(_players) + vertical_padding * (len(_players) - 1)
                    if boxes_h >= h:
                        boxes_h = h
                        vertical_padding = 0

                    y = int((h / 2) - (boxes_h / 2))
                    box_y = y
                    for player in _players:
                         
                        box = self._player_box(player, team)
                        ww, hh = box.size
                        box_x = x - ( ww // 2) + (w // sections // 2) if section != 0 else x
                        _field.paste(box,(box_x, y),box)
                        y += (box_size + vertical_padding)

                    x += (w - 1) // sections
                
                if to_return == team:
                    return _field 

                        
            
            else:
                x = w - 11
                
                for section in squad.keys():
                    
                    _players = squad[section]

                    boxes_h = box_size * len(_players) + vertical_padding * (len(_players) - 1)
                    if boxes_h >= h:
                        boxes_h = h
                        vertical_padding = 0
                    y = int((h / 2) - (boxes_h / 2))
                    box_y = y
                    for player in _players: 
                        box = self._player_box(player, team)
                        ww, hh = box.size
                        box_x = x - ( ww // 2) - (w // sections // 2) if section != 0 else x - ww
                        _field.paste(box,(box_x, y),box)
                        y += (box_size + vertical_padding)

                    x -= (w - 1) // sections
                
                if to_return == team:
                    return _field 
                        
            _lineups.append(_field)

        return _lineups[0], _lineups[1]


    def get_logo(self, tag) -> Image:
        files = [f for f in os.listdir(LOGOS_FOLDER_PATH) if f.upper()[:3] == tag]
        if len(files) == 1:
            return Image.open( LOGOS_FOLDER_PATH + files[0])
        else:
            return None


    def __create_base_image(self) -> Image:
            

            
            result = f"{self.match['Home score']} - {self.match['Away score']}"
            date = self.match.Day
            # Load BGD
            bgd = Image.open(H2H_BGD_PATH)
            bgd_w,bgd_h = bgd.size
            
            # Load LOGS
            home_logo : Image = self.get_logo(self.home_tag).resize((150, 150), Image.ANTIALIAS)
            away_logo : Image = self.get_logo(self.away_tag).resize((150, 150), Image.ANTIALIAS)
            


            # Add LOGS
            logo_w,logo_l = home_logo.size
            x_1 = (bgd_w // 4) - (logo_w // 2) 
            bgd.paste(home_logo, (x_1, 20), home_logo)
            x_2 = (bgd_w // 4) * 3 - (logo_w // 2) 
            bgd.paste(away_logo, (x_2, 20), away_logo)
            
            # Add time and date
            draw = ImageDraw.Draw(bgd)    
            
            font = ImageFont.truetype("/Library/fonts/SF-Pro-Text-Bold.otf",50)
            w,h = font.getsize(result)
            x = (bgd_w // 2) - (w // 2)
            draw.text((x, 40), result,(255,255,255),font=font)
    

            font = ImageFont.truetype("/Library/fonts/SF-Pro-Text-Bold.otf",35)
            w,h = font.getsize('Full time')
            x = (bgd_w // 2) - (w // 2)
            draw.text((x, 100), 'Full time',(255,255,255),font=font)
            
            # SUBS BOX
            subs_box_title = Image.new('RGBA',(276,53),(55,92,121))
            box_w, box_h = subs_box_title.size
            draw2 = ImageDraw.Draw(subs_box_title)
            font = ImageFont.truetype("/Library/fonts/SF-Pro-Text-Bold.otf",30)
            w,h = font.getsize('Substitutes')
            x = (box_w // 2) - (w // 2)
            y = (box_h // 2) - (h // 2)
            draw2.text((x,y), 'Substitutes', (255,255,255), font=font)
            
            bgd.paste(subs_box_title,((808,285)),subs_box_title)




            # FOOTER
            font = ImageFont.truetype("/Library/fonts/SF-Pro-Text-Bold.otf",20)
            draw.text((30, 1052), '@seriea.overview',(173,173,173),font=font)
            draw.text((830, 1052), 'Source: www.fbref.com',(173,173,173),font=font)

            return bgd


    def lineup_for_team(self,tag):
        h,a = self.match_lineup()
        return h if self.home_tag == tag else a


    def match_lineup(self):


        bgd1 = self.__create_base_image()
        bgd2 = self.__create_base_image()

        
        h_line, a_line = self._create_lineup()
        h_subs, a_subs = self._create_subs()


        bgd1.paste(h_line,(16,285),h_line)
        bgd1.paste(h_subs,(799,352),h_subs)

        bgd2.paste(a_line,(16,285),a_line)
        bgd2.paste(a_subs,(799,352),a_subs)

        return bgd1, bgd2


 





if __name__ == '__main__':
    #player_box('Paulo Dybala')
    # h, a  = create_lineup(example, ['MIL', 'INT'])

    # h.show()
    # a.show()

    # LINEUPS_JSON_PATH = '/Users/karis/dev/Python/fb_analysis/data/Serie A/2122/lineups.json'
    # with open(LINEUPS_JSON_PATH, 'r', encoding='utf-8') as f:
    #     LINEUPS = json.load(f)['lineups']
    # prev_matchday = str(14)
    # matches = list(LINEUPS[prev_matchday].keys())
    # prev_match = matches[0]
    # lineup = LINEUPS[prev_matchday][prev_match] 
    # print(lineup)
    # img, img2 = create_lineup(lineup, prev_match.split('-'))
    # img.show()


    # CALENDAR_PATH = f'/Users/karis/dev/Python/fb_analysis/data/Serie A/2122/calendar.csv'
    # calendar = pd.read_csv(CALENDAR_PATH)
    # match_lineups(calendar.iloc[50])
    # #match_lineups(calendar[0])
    
    #substitute_player_box('Davide Calabria', 'Kessie','MIL').show()

    # PATH = f'/Users/karis/dev/Python/fb_analysis/data/Serie A/2122/CSVs/Output/Live Match Results/Matchday 15/LAZ-UDI.csv'
    # calendar = pd.read_csv(PATH)
    # lu  = Lineup(calendar.iloc[0])
    #lu._substitute_player_box('Caldara M.','as','VEN').show()
    # h,a = lu._create_lineup()
    # h.show()
    # a.show()

    # lu._create_subs()
    
    # PATH = f'/Users/karis/dev/Python/fb_analysis/data/Serie A/2122/CSVs/Output/Live Match Results/Matchday 1/SAM-MIL.csv'
    # calendar = pd.read_csv(PATH)
    # lu  = Lineup(calendar.iloc[0])
    # lu.match_lineup()
 
 
    

    for i in range(31,32):
        PATH = f'/Users/karis/dev/Python/fb_analysis/data/Serie A/2122/CSVs/Output/Live Match Results/Matchday {i}/'
        files = [PATH + f for f in os.listdir(PATH) if f != '.DS_Store']
        
        for csv in files:
            df = pd.read_csv(csv)
            lu  = Lineup(df.iloc[0])
            a,b = lu.match_lineup()
            a.show()
            b.show()
            break
            #a.save(f'/Users/karis/Desktop/TWOTCH FOOTBALL/MATERIALE EPISODI/EP.1/Stats/RESULTS/Lineups/{lu.home_tag}-{lu.away_tag} ({lu.home_tag}).png')
            #b.save(f'/Users/karis/Desktop/TWOTCH FOOTBALL/MATERIALE EPISODI/EP.1/Stats/RESULTS/Lineups/{lu.home_tag}-{lu.away_tag} ({lu.away_tag}).png')

 