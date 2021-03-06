import pandas as pd
import numpy as np
import sys
import os
from termcolor import colored
import plotly.offline as pyo
import plotly.graph_objects as go
import random
import secrets

#obsFileName = sys.argv[1]

# create csv folder
if not os.path.exists('csv'):
    os.makedirs('csv')

# convert time
def fixTime(wtime):
    wtime = wtime.replace(' ','-',2)
    wtime = wtime.replace(' ',':',2)
    wtime = wtime.replace(':',' ',1)
    return wtime

# covert obs to csv
def convertToCsv(fileName):
    print(colored("Info",'green'),": converting obs to csv...")
    df = pd.read_csv(fileName, sep = '\t')
    df.to_csv('csv/{0}.csv'.format(fileName))
    print(colored("Info",'green'),": csv format of {0} saved to csv folder.".format(fileName))

# read header of the obs file
def converttoDF(fileName):
    print(colored('Info','green'),': Converting obs file to data frame')
    obsColumns = []
    headerCount = 0
    with open(fileName,mode='r') as f:
        for x in range(100):
            head = next(f)
            obsColumns.append(head.strip())
            if head.strip() == '######':
                headerCount = x +1
                break
    obsColumns = obsColumns[1:len(obsColumns)-1]
    # read body of the obs file
    with open(fileName,mode='r') as f:
        body = f.read()
    body = body.split("\n",headerCount)[headerCount]
    bodyList = body.split('\n')
    # convert body to dataframe
    obsColumnsTm = ['time'] + obsColumns
    df = pd.DataFrame([x.split('\t') for x in bodyList], columns = obsColumnsTm)
    return df

def checkTime(df):
    print(colored('Info','green'),': Checking time format.')
    try:
        df['time'] = pd.to_datetime(df['time'])
        print(colored('Info','green'),': Time format is ok.')
    except:
        print(colored('Warning','yellow'),': Wrong fromat for time. Trying to convert...')
        df['time'] = df['time'].apply(lambda x : fixTime(x))
        try:
            df['time'] = pd.to_datetime(df['time'])
            print(colored('Info','green'), ': Time converted to correct format.')
        except:
            print(colored('Info','red'),': Was not able to fix the time issue. Please make sure your time format is: YYYY-MM-DD HH:MM')
    return df

def plot_go(df, title, path):
    os.chdir(path)
    data = []
    shapes = [dict(width=2),dict(width=4, dash='dot'),dict(width=2,dash='dash')]
    i = 0
    for x in df.columns[1:]:
        if i % 2 ==0:
            shape = shapes[0]
        else:
            shape = shapes[1]
        trace = go.Scatter(x=df['time'],
                            y=df[x],
                            mode='lines',
                            name=x,
                            line= shape,
                            #fill='tonexty',
                            #line_color='indigo'
        )
        data.append(trace)
        i = i + 1
    #print(colored('Info','green'),": Generating plot for {}...".format(obsFileName))
    layout = go.Layout(title='<b>'+ title +'<b>', titlefont=dict(family="Balto",
                                                        size=35,
                                                        color="black"

                                                        ))
    layout.hovermode = 'x'
    fig = go.Figure(data=data, layout=layout)

    pyo.plot(fig)

#plot(checkTime(converttoDF(obsFileName)), obsFileName)



