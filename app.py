import os
import pathlib
import pandas as pd
import dash
import plotly.express as px
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# dashboard financiero

# paso 1

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "Dashboard Financiero"

# dataset
df = pd.read_csv("empresas.csv")

sales_list = ["Total Revenues", "Cost of Revenues", "Gross Profit", "Total Operating Expenses", 
                "Operating Income", "Net Income", "Shares Outstanding", "Close Stock Price",
                "Market Cap", "Multiple of Revenue"]

# dashboard 

app.layout = html.Div([

    html.Div([
        #dropdown para empresas
        html.Div(dcc.Dropdown(
            id="empresa-dropdown", #"stockdropdown"
            value=["Apple","Tesla", "Microsoft", "Apple", "Google"],
            options=[{"label":x,"value":x} for x in sorted(df.Company.unique())]),
            className= "six columns", style={"width":"50%"}), #clearable=False,

        #html del segundo dropdown para elegir variable numerica a ver en el dashboard
        html.Div(dcc.Dropdown(
            id="numericdropdown",value="Total Revenues", clearable=False,
            options=[{"label":x,"value":x} for x in sales_list]), className="six columns",
            style={"width":"50%"})],className="row"), className="custom-dropdown"],

    #html de las graficas
    html.Div([dcc.Graph(id="bar", figure={})]),

    html.Div([dcc.Graph(id="boxplot", figure{})]),.

    html.Div(html.Div(id="table-container_1"), style={"marginBottom":"15px", "marginTop":"0px"}),

        )

    ])

])

#paso 3 callback para actualizar las graficas y la tabla
@app.callback(
    #output: las 2 graficas actualizadas y la tabla 
    [Output("bar","figure"),
     Output("boxplot","figure"),
     Output("table-container_1","children")],
    [Input("stockdropdown","value"),
     Input("empresa-dropdown","value")]
)

#paso 4 definicion de las funciones para armar las graficas y la tabla
def display_value(selected_stock, selected_numeric):
    if len(selected_stock)==0:
        dfv_fltrd=df[df["Company"].isin(["Amazon","Tesla","Microsoft","Apple","Google"])]
    else:
        dfv_fltrd=df[df["Company"].isin(selected_stock)] #seleccionar empresas

    #primera grafica de lineas con empresas seleccionadas:
    fig = px.line(dfv_fltrd, color="Company",x="Quarter",markers=True,y=selected_numeric,
                width=1000,hight=500)

    #hacer titulo de la grafica variable 
    fig.update_layout(title=f"{selected_numeric} de {selected_stock}",
                     xaxis_title="Quarters")

    fig.update_traces(line=dict(width=2))  #ancho de lineas, si no usa defult

    #segunda grafica: boxplot 
    fig2= px.box(dfv_fltrd, color="Company", x="Company", y=selected_numeric, width=1000,height=500)
    fig2.update_layout(title=f"{selected_numeric} de {selected_stock}") #titulo variable 

    #tabla: modificar dataframe para poder hacerlo tabla 
    df_reshaped = dfv_fltrd.pivot(index="Company", columns="Quarter", values=selected_numeric)
    df_reshaped2 = df_reshaped.reset_index()

    #return de la funcion indicando como va a desplegar la tabla 
    return (fig,fig2,
            dash_table.DataTable(columns=[{"name":i,"id":i} for i in df_reshaped2.columns],
                                data=df_reshaped2.to_dict("records"),
                                export_format='csv', #para descargar los datos filtrados 
                                fill_width=True, #que ocupe todo el ancho del dash 
                                 style_cell={"font-size":"12px"},
                                 style_table={"backgroundColor":"blue",
                                              "color":"white"}, #los encabezados tendran fondo azul y texto blanco 
                                 style_data_conditional=[{"backgroundColor":"white","color":"black"}]
                                ))

#paso 5 correre el app
if__name__=="__main__":
    app.run(port=10000)
