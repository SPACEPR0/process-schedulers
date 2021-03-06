import statistics
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.figure_factory as ff
import datetime
import numpy as np
import pandas as pd

## Genera un dataframe con el diccionario del resultado
def genera_df(resultado):
    df = {
            "ids": [resultado["ids"][i] for i in range(len(resultado["ids"]))],
            "cpu_bursts": [resultado["cpu_bursts"][i] for i in range(len(resultado["cpu_bursts"]))],
            "ts_llegada": [resultado["ts_llegada"][i] for i in range(len(resultado["ts_llegada"]))],
            "ts_respuesta": [resultado["ts_respuesta"][i] for i in range(len(resultado["ts_respuesta"]))],
            "ts_salida": [resultado["ts_salida"][i] for i in range(len(resultado["ts_salida"]))],
            "ts_retorno": [resultado["ts_retorno"][i] for i in range(len(resultado["ts_retorno"]))],
            "ts_espera": [resultado["ts_espera"][i] for i in range(len(resultado["ts_espera"]))]
        }
    dataframe = pd.DataFrame(df)
    return dataframe

## Genera tabla
def crear_tabla(dataframe, resultado, cambio, cap, q=0):
    max_rows=100
    rowcol=['#F3F5F6' if i%2==0 else '#FFFFFF' for i in range(1, len(dataframe.index)+1)]
    
    return html.Table([
        html.Thead([html.Th(cap)]),
        html.Thead(
            html.Tr([html.Th("ID", style={'textAlign': 'center'}), html.Th("CPU Burst", style={'textAlign': 'center'}), html.Th("T. Llegada", style={'textAlign': 'center'}), 
            html.Th("T. Respuesta", style={'textAlign': 'center'}), html.Th("T. Salida", style={'textAlign': 'center'}), html.Th("T. Retorno", style={'textAlign': 'center'}),
            html.Th("T. Espera", style={'textAlign': 'center'})], style={'backgroundColor': '#B4B5BB'})
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col], style={'textAlign': 'center'}) for col in dataframe.columns
            ], style={'backgroundColor': rowcol[i]}) for i in range(min(len(dataframe), max_rows))
        ]),
       html.Thead([html.Th("Promedios", style={'textAlign': 'center'}), html.Td("-", style={'textAlign': 'center'}), html.Td("-", style={'textAlign': 'center'}), 
       html.Th(statistics.mean(resultado['ts_respuesta']), style={'textAlign': 'center'}), html.Td("-", style={'textAlign': 'center'}), 
       html.Th(statistics.mean(resultado['ts_retorno']), style={'textAlign': 'center'}), html.Th(statistics.mean(resultado['ts_espera']), style={'textAlign': 'center'})], style={'backgroundColor': '#A0E4C1'}),
       html.Thead([html.Th("Cambios de Contexto: "), html.Td(cambio), html.Th("Quantum: " if q!=0 else ""), html.Td(q if q!=0 else "")]) 
    ], className = 'column')

## Función para gráfica de Gantt
def convert_to_datetime(x):
  return datetime.datetime.fromtimestamp(31536000+x*24*3600).strftime("%Y-%m-%d")

## Genera gráfica de Gantt en plotly
def graficaGantt(orden, typ):
# iterando sobre la lista de orden para generar un dataframe con fechas para la gráfica de Gantt:
    gantt = []
    i = 0
    st = 0
    p = ''
    tarea = 0
    end = 0
    le = len(orden)-1
    while i < le:
        if orden[i] != '-':
            p = orden[i]
            st = i
            for j in range(i, le):
                if orden[j] != p:
                    end = j
                    break
                if j ==le-1:
                    end = j+1
                    break
            gantt.append(dict(Start = convert_to_datetime(st), Finish = convert_to_datetime(end), Task = p))
            i = end
        else:
            i += 1
    df = pd.DataFrame(gantt)

    # Grafica de Gantt

    fig = px.timeline(df, x_start='Start', x_end='Finish', y='Task', color='Task',
        labels={"Task": "Proceso"},
            title=typ)
    fig.layout.xaxis.update({
            'tickvals' : np.concatenate(([df['Start'].values[0]],df['Finish'].values)),
            'title': 'Tiempo',
            'tickfont': {'size': 10},
            'ticktext' : [0]+[(pd.to_datetime(df['Finish'][i]) - pd.to_datetime(df['Start'][0])).days for i in range(df.shape[0])],
            'tickangle': 90
            })
    fig.update_layout({
        'showlegend': False
    })
    fig.layout.yaxis.update({
            'tickmode': 'linear',
            'tick0': df['Task'][0],
            'dtick': 1,
            'autorange': 'reversed',
            'showgrid': True
    })
    for i in df['Finish'].values:
        fig.add_vline(i, line_color="gray")
    return fig

## estructura para la grafica de comparacion
def gen_comp(res):
    df = {}
    for p in res['ids']:
        traza = []
        for i in res['orden']:
            if p == i:
                traza.append(i)
            else:
                traza.append(None)
        df[p] = traza
    return df
## Gráfica de comparación de algritmos

def comparacion(res_srtf, res_rr):
    c_srtf = gen_comp(res_srtf)
    c_rr = gen_comp(res_rr)
    ids = list(c_rr.keys())
    coincide = {}
    for p in ids:
        traza = []
        for i in range(len(c_srtf[p])):
            if c_srtf[p][i] == c_rr[p][i] and c_srtf[p][i] != None:
                traza.append(c_srtf[p][i])
            else:
                traza.append(None)
        coincide[p] = traza
    
    # SRTF
    fig = px.scatter(x=[x for x in range(len(c_srtf[ids[0]]))], y=c_srtf[ids[0]])
    for i in range(len(ids)):
        fig.add_scatter(x=[x for x in range(len(c_srtf[ids[0]]))], y=c_srtf[ids[i]], mode="lines+markers",
                marker=dict(color="darkorange"))
    # RR
    for i in range(len(ids)):
        fig.add_scatter(x=[x for x in range(len(c_rr[ids[0]]))], y=c_rr[ids[i]], mode="lines+markers",
                marker=dict(color="LightSeaGreen"))
    # Puntos donde coinciden
    for i in range(len(ids)):
        fig.add_scatter(x=[x for x in range(len(coincide[ids[0]]))], y=coincide[ids[i]], mode="lines+markers",
                marker=dict(color="maroon"))
    fig.update_layout({
        'showlegend': False
    })
    fig.layout.xaxis.update({
            'title': 'Tiempo'
            })
    fig.layout.yaxis.update({
            'title': 'Procesos',
            'tickmode': 'linear',
            'dtick': 1,
            'autorange': 'reversed',
    })
    return fig

## Layouts para la página ##

## Ambos algoritmos

def layout_all(res_srtf, res_rr, q=0):
    return html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.H1(children='SIMULACIÓN DE CALENDARIZADORES DE PROCESOS', style={
                    'textAlign': 'center'}),
                    html.H2(children =["Resultados de la ejecución de los algoritmos SRTF y Round Robin"])
                ], style={
                        'textAlign': 'center'
                })
                ], style = {'backgroundColor': '#F1F0FA'}),
                html.Div(children=[
                html.H4(children='Tablas de tiempos', style={
                        'textAlign': 'center'
                })
            ]),
            html.Div(children=[
            crear_tabla(genera_df(res_srtf), res_srtf, res_srtf['cambios_contexto'], "SRTF"),
            crear_tabla(genera_df(res_rr), res_rr, res_rr['cambios_contexto'], "Round Robin", q)
            ], style={
                'marginLeft': 100, 'marginRight': 100, 'columnWidth': 600
            }, className = 'row'),
            html.Div(children=[
                html.H4(children='Diagramas de Ejecución', style={
                    'textAlign': 'center'
                }),
                dcc.Graph(
                id='gantt-srtf',
                figure=graficaGantt(res_srtf['orden'], "SRTF")
                ),
            ], style={
                'marginLeft': 200, 'marginRight': 350
            }, className = 'row'),
            html.Div(children=[
                dcc.Graph(
                id='gantt-rr',
                figure=graficaGantt(res_rr['orden'], "Round Robin")
                ),
            ], style={
                'marginLeft': 200, 'marginRight': 350
            }, className = 'row'),
            html.Div(children=[
                html.H4(children="Comparación de Algoritmos", style={'textAlign': 'center'}),
                dcc.Graph(
                id='comparacion',
                figure=comparacion(res_srtf, res_rr)
                ),
            ], style={
                'marginLeft': 200, 'marginRight': 350
            }, className = 'row')
        ])

## Un solo algoritmo
def layout_uni(res, alg, q=0):
    return html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.H1(children='SIMULACIÓN DE CALENDARIZADORES DE PROCESOS', style={
                    'textAlign': 'center'}),
                    html.H2(children =["Resultados de la ejecución del algoritmo ", alg])
                ], style={
                        'textAlign': 'center'
                })
                ], style = {'backgroundColor': '#F1F0FA'}),
                html.Div(children=[
                html.H4(children='Tabla de tiempos', style={
                        'textAlign': 'center'
                })
            ]),
            html.Div(children=[
            crear_tabla(genera_df(res), res, res['cambios_contexto'], alg, q)
            ], style={
                'marginLeft': 100, 'marginRight': 150
            }, className = 'row'),
            html.Div(children=[
                html.H4(children='Diagrama de Ejecución', style={
                    'textAlign': 'center'
                }),
                dcc.Graph(
                id='gantt',
                figure=graficaGantt(res['orden'], alg)
                ),
            ], style={
                'marginLeft': 200, 'marginRight': 350
            }, className = 'row')
        ])