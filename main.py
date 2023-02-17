from rssparser import RSSParser
from subprocess import Popen,PIPE
import datetime

from dash import Dash, html, dcc, Input, Output, State, ALL

url_dict = {'URL':["https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/YourMoney.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/PersonalTech.xml"
        "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Space.xml",
        ]
}

urls = url_dict['URL']

minutes = 2

rss_p = RSSParser(20)

feeds,categories = rss_p.parserss(urls)
prev_nclicks = []
for x in range(0,len(categories)):
    prev_nclicks.append(0)



process = Popen(['rm','-rf','/tmp/tmp.*.Parser'],stdout=PIPE,stderr=PIPE)

process = Popen(['mktemp','-d','--suffix=.Parser'],stdout=PIPE,stderr=PIPE)
stdout,stderr = process.communicate()

root_dir = str(stdout,'utf-8').strip() + '/'


app = Dash(__name__)
app.layout = html.Div(children=[  
        html.H1(["I'm not Paying for New York Times"],
            style={'max-width': '800px','margin':'auto','padding':'20px 0','color':'#e5d1d0'}),
        html.Div([
            html.Button(entry, 
            id={'type':'button',"index":i}, 
            n_clicks=0,
            style={'margin-left':'10px'}) for i,entry in enumerate(categories)
        ], style={'max-width': '800px','margin':'auto','text-align':'center'}) ,
        dcc.Interval(id='interval-time',
        interval=minutes*60*1000,
        n_intervals=0),
        html.Ul([ html.Li(children=[                
                    html.A(entry['Title'],
                    target='_blank',
                    id={'type': 'link', 'index': i},
                    style={
                        'text-decoration': 'none',
                        'color': '#dce1de',
                        'font-weight': 'bold',
                        'font-size': '18px',
                        'display': 'block',
                        'padding': '10px 0'
                    }
                ),
                html.Span(
                    entry['Date'],
                    id={'type':'date','index':i},
                    style={
                        'font-size': '14px',
                        'display': 'block',
                        'padding': '5px 5',
                        'color': '#9cc5a1'
                    }
                ),
                html.Span(
                    entry['Topic'],
                    id={'type':'topic','index':i},
                    style={
                        'font-size': '12px',
                        'display': 'inline-block',
                        'padding': '5px 2px',
                        'color': '#E5D1D0',
                        },
                )
            ],
            style={
                'list-style': 'none',
                'border-bottom': '1px solid lightgray',
                'padding': '10px 0'
            }
        ) for i, entry in enumerate(feeds)
    ],
    style={
        'max-width': '800px',
        'margin': 'auto',
        'padding': '20px 0'
    }
),
        html.Div(id='last_update',
        style={'max-width': '800px',
            'margin':'auto',
            'text-align':'center',
            'backgroundColor':'#dce1de',
            'border-radius':'5px'})],
        style={'backgroundColor':'#1f2421'})

def get_current_time():
    return "Last Updated " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_key(l1,l2):
    for i in range(0,len(l1)):
        if l1[i] != l2[i]:
            return categories[i]
    return categories[0]



@app.callback(
        Output({'type':'link','index':ALL},'style'),
        Input({'type':'link','index':ALL}, 'n_clicks'),
        State({'type': 'link', 'index': ALL}, 'id'),
        State({'type': 'link', 'index': ALL}, 'style')
)
def link_clicks(n_clicks_list, id_list,style_list):
    
    return rss_p.process_click(n_clicks_list,id_list,style_list,root_dir)

@app.callback(
        Output({'type':'link','index':ALL},'children'),
        Output({'type':'date','index':ALL},'children'),
        Output({'type':'topic','index':ALL},'children'),
        Output('last_update','children'),
        Input('interval-time','n_intervals'),
        Input({'type':'button','index':ALL},'n_clicks')
)
def update_feeds(n_interval,n_clicks):
    global prev_nclicks
    new_titles = []
    new_dates = []
    new_topics = []
    key = '*'

    if all(x == 0 for x in n_clicks):
        key = '*'
        prev_nclicks = n_clicks
    else:
        key = get_key(n_clicks,prev_nclicks)
    
    prev_nclicks = n_clicks
    feeds,categories = rss_p.parserss(urls,key)

    for dicts in feeds:
        new_titles.append(dicts['Title'])
        new_dates.append(dicts['Date'])
        new_topics.append(dicts['Topic'])
    return new_titles,new_dates,new_topics,get_current_time()


    

if __name__ == '__main__':
    app.run_server()
        

