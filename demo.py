# make fold
import PySimpleGUI as sg
from re import findall

##chdir('')

playing = 0
highlight_label=None

window_size=(1025,675)

gray = '#F0F0F0'
black_gray='#e8e9ec'
background = '#ffffff'
white = '#ffffff'
background_toolbar = '#b73226'

sg.SetOptions(background_color=white,
              font=("Helvetica", 9),
              margins=(0,0),
              element_background_color=white,
              element_padding=((0,0),(0,0))
             )

# Images are located in a subfolder in the Demo Media Player.py folder
image_pause = './icons/stop.png'
image_start = './icons/start.png'
image_next = './icons/next.png'
image_forward = './icons/forward.png'
image_undo = './icons/undo.png'
image_redo = './icons/redo.png'
image_change_theme = './icons/change_theme.png'
image_setting = './icons/setting.png'
image_min = './icons/min.png'
image_max = './icons/max.png'
image_close = './icons/close.png'
image_search = './icons/afd.png' #'./icons/s.png'
image_find = './icons/find.png'

USE_MARK=1
USE_SPETAER=1

add_mian_panel=0  # only for test

pad_palybar_left_toolbar=130
pad_logo_undo=18
pad_redo_search=2
pad_search_theme=120
pad_left_toolbar_text=7

size_left_toolbar_text=(20,2)


dict_recommend = {
    'find': ('./icons/find.png', '发现音乐'),
    'fm': ('./icons/fm.png', '私人FM'),
    'mv': ('./icons/mv.png', 'MV'),
    'friend': ('./icons/friend.png', '朋友'),
}
dict_my_music = {
    'local': ('./icons/local_music.png', '本地音乐'),
    'download': ('./icons/download.png', '下载管理'),
    'cloud': ('./icons/cloud.png', '我的音乐云盘'),
    'singer': ('./icons/singer.png', '我的歌手')
}
dict_maked_musiclist = {
    'favorite': ('./icons/favorite.png', '我喜欢的音乐'),
    'musiclist': ('./icons/music_list.png', '自定义歌单')
}

def get_playbar_location(button_h=50,pad=10):
    c_l=window.current_location()
    return (0, c_l[1]-button_h)
# define the toolbar
column_toolbar = [
    [sg.Button('', image_filename='./icons/toolbar_logo.png',
               button_color=(background_toolbar, background_toolbar),key='logo',
               border_width=0,)] +[sg.Text(' ' * pad_logo_undo, background_color=background_toolbar)]+ [
        sg.Button('',
                  button_color=(background_toolbar, background_toolbar),
                  image_filename=x,
                  image_size=(20, 40),
                  image_subsample=2,
                  border_width=0,
                  pad=((0, 0), (0, 0)),
                  key=y)
        for x, y in zip([image_undo, image_redo], ['undo', 'redo'])
    ] +[sg.Text(' ' * pad_redo_search, background_color=background_toolbar)]+ [
        sg.Input('search music here',
                 text_color='white',
                 size=(30, 1),
                 key='search_text',
                 background_color=background_toolbar)
    ] + [
        sg.Button('',
                  button_color=(background_toolbar, background_toolbar),
                  image_filename=image_search,
                  image_size=(20, 20),
                  image_subsample=3,
                  border_width=0,
                  pad=((0, 0), (0, 0)),
                  key='search',
                  bind_return_key=True)
    ] + [sg.Text(' ' * pad_search_theme, background_color=background_toolbar)] + [
        sg.Button('',
                  button_color=(background_toolbar, background_toolbar),
                  image_filename=x,
                  image_size=(30, 30),
                  image_subsample=1,
                  border_width=0,
                  pad=((0, 0), (0, 0)),
                  key=y) for x, y in zip([
                      image_change_theme, image_setting, image_min, image_max,
                      image_close
                  ], ['change_theme', 'setting', 'min', 'max', 'close'])
    ]
]

# define the left toolbar
column_left_toolbar = [[
    sg.Text('推荐',  background_color=white, pad=((0,0),(1,1)),key='recommand')
]] + [[
    sg.Column([[
        sg.Button('',
                  button_color=(white, white),
                  image_filename=x,
                  image_size=(30, 30),
                  image_subsample=1,
                  border_width=0,
                  pad=((12, 0), 1),
                  key=y),
        sg.Text(z,  enable_events=True,size=size_left_toolbar_text,
                key=y + '_text',pad=((0,0),(pad_left_toolbar_text,0)))
    ]],
              key=y + '_column',
              pad=((0, 0), (0, 0)),
              size=(200, 34)
    )
] for y, (x, z) in dict_recommend.items()] + [[
    sg.Text('我的音乐',  background_color=white, pad=((0,0),(1,1)), key='mymusic')
]] + [[
    sg.Column([[
        sg.Button('',
                  button_color=(white, white),
                  image_filename=x,
                  
                  image_size=(30, 30),
                  image_subsample=1,
                  border_width=0,
                  pad=((0, 0), 1),
                  key=y),
        sg.Text(z,  enable_events=True,size=size_left_toolbar_text,
                key=y + '_text',pad=((0,0),(pad_left_toolbar_text,0)))
    ]],
              key=y + '_column',
              pad=(12, 0),
              size=(200, 34)
    )
] for y, (x, z) in dict_my_music.items()] + [[
    sg.Text('创建的歌单',  background_color=white, pad=((0,0),(1,1)), key='createdmusiclist')
]] + [[
    sg.Column([[
        sg.Button('',
                  button_color=(white, white),
                  image_filename=x,
                  image_size=(30, 30),
                  image_subsample=1,
                  border_width=0,
                  pad=((0, 0), 1),
                  key=y),
        sg.Text(z,  enable_events=True,size=size_left_toolbar_text,
                key=y + '_text',pad=((0,0),(pad_left_toolbar_text,0)))
    ]],
              key=y + '_column',
              pad=(12, 0),
              size=(200, 34)
    )
] for y, (x, z) in dict_maked_musiclist.items()]


# define the main panel

pad_main_panel_board_text=30
pad_main_panel_middle_text=5

dict_m_p_text={'personal_rcmd':'个性推荐','musiclist_m_p':'歌单',
               'anchor_radio':'主播电台','leader_board':'排行榜','lastest_music':'最新音乐'}
column_main_panel=[
    [sg.Text(v,key=k) for k,v in dict_m_p_text.items()],
    [sg.Image('./icons/avatar.png',size=(300,50))],
    [sg.Text('推荐歌单',key='rcmd_music_list')],
    [sg.Image('./icons/avatar.png',size=(300,50))],
]

# define the playbar
column_playbar = [
    [sg.Button('move_l_t_down',visible=False),sg.Button('move_l_t_up',visible=False),]+
    [sg.Image('./icons/avatar.png',size=(50,50),pad=((0,0),(0,0))),
     sg.Column([[sg.Text('琵琶行',key='music_name',),sg.Image('./icons/favorite.png',key='love_or_no')],
                [sg.Text('奇然/沈谧仁',key='author',),sg.Image('./icons/share.png',key='share')]])],
    [
      sg.Button('',
                button_color=(background, background),
                image_filename=image_forward,
                image_size=(50, 50),
                image_subsample=1,
                border_width=0,
                key='forward'),
        
      sg.Button('',
                button_color=(background, background),
                image_filename=image_start,
                image_size=(30, 30),
                image_subsample=1,
                border_width=0,
                size=((50,50)),
                key='start_or_stop'),
        
      sg.Button('',
                button_color=(background, background),
                image_filename=image_next,
                image_size=(50, 50),
                image_subsample=1,
                border_width=0,
                key='next'),
          ]]


layout = [
    [
        sg.Column(
            column_toolbar,
            background_color=background_toolbar,
            size=(1100, 50),
            pad=((0,0),(0,0)),
            key='toolbar'
        )
    ],
    [sg.Column(column_left_toolbar, background_color=white,
               key='left_toolbar',)]+
     ([sg.Text(' ',key='sperater',background_color=gray,font=("Helvetica", 1))] if USE_SPETAER else [])+
      ([sg.Text(' ',background_color=background_toolbar,
                key='mark_text',font=("Helvetica", 1))] if USE_MARK else []) 
    +([sg.Column(column_main_panel)] if add_mian_panel else []) ,
    
    [sg.Column(
        column_playbar,
        background_color=white,
        key='playbar',
        pad=((0,0),(pad_palybar_left_toolbar,0))
    )],
]

# generate the window

window = sg.Window(
    'Media File Player',
    layout,
    auto_size_text=True,
#     font=("Helvetica", 25),
    size=window_size,
    no_titlebar=False,
    margins=(0,0),
    resizable=True,
    finalize=True
)  #default_element_size=(20, 1),

def get_elem_size_and_posi(e,refresh=0,window=window):
    if refresh: window.Finalize()
    return [int (x) for x in findall('\d+',window.Elem(e).Widget.winfo_geometry())]

g=get_elem_size_and_posi

def place(e,x,y,refresh=0):
    if refresh: window.Finalize()
    window.Elem(e).Widget.place(x=x,y=y)


def ready_to_get_all_thing(Column,all_thing,pattern=['Text','Button'],):
    if type(Column)==list:
        for x in Column:
            ready_to_get_all_thing(x,all_thing,pattern)
    elif 'Column' in str(Column) :
        if 'Column' in pattern:all_thing.append(Column)
        for x in Column.Rows:
            ready_to_get_all_thing(x,all_thing,pattern)
    else:
        for x in pattern:
            if x in str(Column):
#                 print(Column)
                all_thing.append(Column)
                break
#     print(Column)
                
def get_all_elem(Column,pattern=['Text','Button'],total=0):
    all_thing=[]
    ready_to_get_all_thing(Column,all_thing,pattern)
    return [x for x in all_thing if x.Key not in ['recommand','mymusic','createdmusiclist']] if total==0 else [x for x in all_thing if x.Key]

def get_correct_x(event):
    index=all_short_key_in_left_toolbar.index(event)
    return 23*(1+index//4) + 33*index

def move_left_toolbar(direction='down',step=10,):
    place('left_toolbar',0, -g('left_toolbar')[3] + step*(1 if direction=='down' else -1))
    
# update size and position
# window.Elem('123').Widget.place(x=100,y=20)
# input('Continue...')
# window.Elem('toolbar').Update(visible=False)
# window.Finalize()
# window.Elem('toolbar').Update(visible=True)

# input('Continue...')

size_of_left_toolbar=get_elem_size_and_posi('left_toolbar')

# mark_text=
all_key_in_left_toolbar=[ x.Key for x in get_all_elem(window.Elem('left_toolbar'))]
all_short_key_in_left_toolbar=[x for x in all_key_in_left_toolbar if '_' not in x]

def init():
    if USE_SPETAER: 
        window.Elem('sperater').set_size((5,size_of_left_toolbar[1]))
        place('sperater',g('sperater')[2]-40,0)
        
    if USE_MARK: 
        window.Elem('mark_text').set_size((1,10))
        place('mark_text',-3,get_correct_x('find'))
        window.Elem('mark_text').set_size((1,10))
        
    window.Elem('start_or_stop').Update(image_filename=image_start,)
    window['start_or_stop'].set_size((50,50))
    
    window['search_text'].Widget.config(insertbackground=white)
    
#     window['find_column'].Widget.bind("<Button-4>", window['search'].ButtonReboundCallback)
#     window['left_toolbar'].Widget.bind("<Button-4>", window['search'].ButtonReboundCallback)

    for x in get_all_elem(window['left_toolbar'],pattern=['Text', 'Button', 'Column'],total=1):
        x.Widget.bind("<Button-4>", window['move_l_t_down'].ButtonReboundCallback)
        x.Widget.bind("<Button-5>", window['move_l_t_up'].ButtonReboundCallback)
        
#         x.expand((True,True),)
#         if 'Text' in  str(x):
#             place(x.Key,g(x.Key)[2],0)
    
    
    
    
init()

# print(all_short_key_in_left_toolbar)
# assert  0
# Our event loop

while (True):
    event, values = window.Read()  # Poll every 100 ms
    if event in ('close', 'Exit', None):
#         print(window.size)
        break
    elif event == 'start_or_stop':
        if playing:
            window.Elem('start_or_stop').Update(
                image_filename=image_start,
            )
        else:
            window.Elem('start_or_stop').Update(
                image_filename=image_pause,
            )
        playing = not playing
        window['start_or_stop'].set_size((50,50))
        
    elif event == 'logo':
#         e = window.Elem('cloud_column')
#         print(e.get_size())
        while 1:
            try:
                input_ = input('>>> ')
                if input_ == 'b': break
                else: 
                    exec(input_)
                    window.Finalize()
                    window.refresh()
            except Exception as e :
                print(e)
                
    elif event in all_key_in_left_toolbar:
        if highlight_label:
            window.Elem(highlight_label).Update(button_color=(white,white))
            window.Elem(highlight_label+'_text').Update(background_color=white)
        short_key=event.split('_')[0]
        window.Elem(short_key).Update(button_color=(black_gray,black_gray))
        window.Elem(short_key+'_text').Update(background_color=black_gray)
        
        window.Elem(short_key+'_column').Widget.configure(background=background_toolbar)
        if USE_MARK: place('mark_text',-3,get_correct_x(short_key))
        highlight_label=short_key
    elif event == 'min':
        window.minimize()
    
    elif event in ['move_l_t_down', 'move_l_t_up']:
        move_left_toolbar(event.split('_')[-1], )
        
    if event != sg.TIMEOUT_KEY:
        print(event)
        window.Element('recommand').Update(event)
        
window.Close()

''' 
print(window.Elem('123').Widget.winfo_geometry()) #绝对位置
print(window.current_location)

'''
