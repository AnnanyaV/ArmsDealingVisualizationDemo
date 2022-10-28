
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
from plotly.offline import plot, iplot, init_notebook_mode


app = Dash(__name__)


df=pd.read_csv("check-1.csv")
df2=pd.read_csv("check-2.csv")
datasets=[df, df2]

#############################################################################
#Duration comparison amongst users
x=['User 1', 'User 2']
y=[]

for i in datasets:
    time=float(i.iloc[-1,5])-float(i.iloc[0,5])
    y.append(time)
data={'Users':x, 'Duration':y}
df_compare=pd.DataFrame(data)
res = {x[i]: y[i] for i in range(len(x))}
fig_compare = px.bar(data, x='Users', y='Duration', width=10,color="Users", color_discrete_sequence=["green", "goldenrod"],
title="Comparison of total time taken by the users to reach a conclusion.")
# fig_compare.update_layout(width = 2000)
fig_compare['layout'].update(height = 600, width = 700)
# fig_compare.update_traces(width=3)





#Getting the maximum for every segment for the first user
l={}
j=0
m=0
for i in range(0, 47):
    max=0
    p={}
    while df.iloc[j,6]==i:
        if df.iloc[j,3] in p:
            p[df.iloc[j,3]]+=1
        else:
            p[df.iloc[j,3]]=1
        j+=1
    for x,y in p.items():
        if y>max:
            m=x
    l[i]=m

IntTypeMax=[]
segment=[]
for i,j in l.items():
  IntTypeMax.append(j)
  segment.append(i)

#Graph for interaction type vs maximum segment for first user

import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=df['InteractionType'], y=segment,
                    mode='markers',
                    name='markers'))

#Getting the maximum for every segment for the 2ND USER

l={}
j=0
m=0
for i in range(0, 24):
    max=0
    p={}
    while df2.iloc[j,6]==i:
        if df2.iloc[j,3] in p:
            p[df2.iloc[j,3]]+=1
        else:
            p[df2.iloc[j,3]]=1
        j+=1
    for x,y in p.items():
        if y>max:
            m=x
    
    l[i]=m
IntTypeMax1=[]
segment1=[]
for i,j in l.items():
    IntTypeMax1.append(j)
    segment1.append(i)
#Graph for interaction type vs maximum segment for the second user
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df2['InteractionType'], y=segment1,
                    mode='markers',
                    name='markers'))

df_avgIntTypes=pd.read_csv('forAvgTime.csv')


data = dict(
    number=df_avgIntTypes['Average'],
    stage=df_avgIntTypes['IntType'])
fig_main = px.funnel(data, x='number', y='stage', color= "number", color_discrete_sequence=["green", "goldenrod"])
# fig_main.show()


#################################################################################

#Average InteractionType for - user1
InteractionTypes= df['InteractionType'].unique()
gk = df.groupby('InteractionType')
listAvgInteractionTimes=[]
for i in InteractionTypes:
  summ=0
  y= gk.get_group(i)
  for j in y['duration']:
    summ= summ+int(j)

  listAvgInteractionTimes.append(int(summ)//int(len(y)))
  data = {'IntType': InteractionTypes,
        'Average': listAvgInteractionTimes}
# Average InteractionType duration comparison - user2
df_avgIntTypes1 = pd.DataFrame(data)
data = dict(
    number=df_avgIntTypes1['Average'],
    stage=df_avgIntTypes1['IntType'])
fig_user1 = px.funnel(data, x='number', y='stage')
# fig_user1.show()

##################################################################################

#Documents accessed analysis
d=pd.read_csv("doc.csv")
for i in range(len(d)):
    # print(d.iloc[i,6])
    if ',' in d.iloc[i,5]:
        x,y= d.iloc[i,5].split(',')
        d.iloc[i,5]=x
gk = d.groupby('ID')
sums={}
ll=d['ID'].unique()
for i in ll:
    p=gk.get_group(i)
    summ=p['duration'].sum()
    sums[i]=summ

l_ID=[]
l_duration=[]
for i,j in sums.items():
    l_ID.append(i)
    l_duration.append(j)

# doc_list = pd.DataFrame(
#     {'Document': l_ID,
#      'Duration': l_duration
#     })

# figdocs = go.Figure()
data={'Docs':l_ID, 'Duration':l_duration}
# figdocs = px.data.tips()
# figdocs = px.bar(data, y="Duration", x="Docs")
figdocs= px.sunburst(data, path=['Duration', 'Docs']
                  )
# figdocs = px.pie(data, y="Duration", x="Docs", title='Population of European continent')
figdocs = px.treemap(data, path=['Duration', 'Docs'])






app.layout = html.Div(children=[
    html.H1(children='User logs visualization'),
    
    dcc.Dropdown(['User1', 'User2', 'All'], 'User1', id='demo-dropdown', multi=True),

    html.Div(children=[     
        dcc.Graph(
        id='example-graph',
        figure=fig,
        style={'display': 'inline-block'}
    ),
    dcc.Graph(
        id='bar',
        figure=fig_compare,
        style={'display': 'inline-block'}
    )
    ]),

    
    # dcc.Graph(
    #     id='example-graph',
    #     figure=fig
    # ), 

    dcc.Dropdown(['User1', 'User2', 'All'], 'User1', id='dropdown-second'),
    dcc.Graph(
        id='funnel-avg',
        figure=fig_main
    ),
    # dcc.Graph(
    #     id='bar',
    #     figure=fig_compare
    # ),
    dcc.Graph(
        id='docs',
        figure=figdocs
    ),
    
    html.Div(id='dd-output-container')
], )

@app.callback(
    Output('example-graph', 'figure'),
    [Input('demo-dropdown', 'value')],
)
def update_output(value):
    # print(value)
    # print(len(value))
    if value=='User1':
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['InteractionType'], y=segment,
                    mode='markers',
                    name='markers'))
       
        return fig
    elif len(value)==1 and value[0]=='User1':
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['InteractionType'], y=segment,
                    mode='markers',
                    name='markers'))
        return fig

    elif len(value)==1 and value[0]=='User2':
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df2['InteractionType'], y=segment1,
                    mode='markers',
                    name='markers'))
        return fig
    
    elif len(value)==1 and value[0]=='All':
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=df2['InteractionType'], y=segment1,
                    mode='markers',
                    name='User2',
                    marker=dict(
        color='rgb(34,163,192)'
               )))
        fig.add_trace(go.Scatter(x=df['InteractionType'], y=segment,
                    mode='markers',
                    name='User1'),secondary_y=True)
        fig['layout'].update(height = 600, width = 1200)
        return fig
    

    else:
        if 'All' in value or ('User1' and 'User2' in value):
            # fig = go.Figure()
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=df2['InteractionType'], y=segment1,
                    mode='markers',
                    name='User2',
                    marker=dict(
        color='rgb(34,163,192)'
               )))
            fig.add_trace(go.Scatter(x=df['InteractionType'], y=segment,
                    mode='markers',
                    name='User1'),secondary_y=True)
            fig['layout'].update(height = 600, width = 1200)
            return fig
        

@app.callback(
    Output('funnel-avg', 'figure'),
    [Input('dropdown-second', 'value')],
)
def update_output(value):
    if value=='User1':
        data = dict(
        number=df_avgIntTypes['Average'],
        stage=df_avgIntTypes['IntType'])
        fig_main = px.funnel(data, x='number', y='stage')
       
        return fig_main
    if value=='User2':
        
        data = dict(
        number=df_avgIntTypes1['Average'],
        stage=df_avgIntTypes1['IntType'])
        fig_user1 = px.funnel(data, x='number', y='stage')
        
        return fig_user1

    else:
        if value=='All':
            fig = go.Figure(data=[
            go.Bar(name='User 1', x=df_avgIntTypes['IntType'], y=df_avgIntTypes['Average']),
            go.Bar(name='User 2', x=df_avgIntTypes1['IntType'], y=df_avgIntTypes1['Average'])
                ])
            
            fig.update_layout(barmode='stack')
            return fig

#Do it without docopen







if __name__ == '__main__':
    app.run_server(debug=True)
