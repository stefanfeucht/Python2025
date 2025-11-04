#Github: incluir el mismo chunck de los imports
import plotly as pl
import plotly.express as px
#import numpy as np
import pandas as pd
import pathlib
import dash


from dash import Dash,dcc,html,dash_table
from dash.dependencies import Input,Output
import dash_bootstrap_components as dbc

# Paso 1: Inicializar la app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#Github:agregar linea de server que usa github
server=app.server

app.title = "Dashboard Financiero"

# Paso 2: Cargar dataset
df = pd.read_csv("empresas.csv")

sales_list = [
    "Total Revenues", "Cost of Revenues", "Gross Profit", "Total Operating Expenses",
    "Operating Income", "Net Income", "Shares Outstanding", "Close Stock Price",
    "Market Cap", "Multiple of Revenue"
]

# ====== Layout ======
app.layout = html.Div([

    html.Div([
        # Dropdown para empresas
        html.Div(
            dcc.Dropdown(
                id="empresa-dropdown",
                value=["Apple", "Tesla", "Microsoft", "Google"],  
                options=[{"label": x, "value": x} for x in sorted(df["Company"].unique())],
                multi=True,
                clearable=False
            ),
            className="six columns",
            style={"width": "50%"}
        ),

        # Dropdown para variable numérica
        html.Div(
            dcc.Dropdown(
                id="numericdropdown",
                value="Total Revenues",
                clearable=False,
                options=[{"label": x, "value": x} for x in sales_list]
            ),
            className="six columns",
            style={"width": "50%"}
        )
    ], className="row", style={"display": "flex", "gap": "10px"}),

    # ====== Gráficas ======
    html.Div([
        dcc.Graph(id="bar", figure={})
    ]),

    html.Div([
        dcc.Graph(id="boxplot", figure={})
    ]),

    # ====== Tabla =======
    html.Div(
        html.Div(id="table-container_1"),
        style={"marginBottom": "15px", "marginTop": "0px"}
    )
])

# ====== Callback ======
@app.callback(
    [
        Output("bar", "figure"),
        Output("boxplot", "figure"),
        Output("table-container_1", "children")
    ],
    [
        Input("empresa-dropdown", "value"),
        Input("numericdropdown", "value")
    ]
)
def display_value(selected_stock, selected_numeric):
    # Manejar caso sin selección
    if not selected_stock or len(selected_stock) == 0:
        dfv_fltrd = df[df["Company"].isin(["Amazon", "Tesla", "Microsoft", "Apple", "Google"])]
    else:
        dfv_fltrd = df[df["Company"].isin(selected_stock)]

    # ====== Gráfica de líneas ======
    fig = px.line(
        dfv_fltrd,
        color="Company",
        x="Quarter",
        y=selected_numeric,
        markers=True,
        width=1000,
        height=500
    )

    fig.update_layout(
        title=f"{selected_numeric} de {', '.join(selected_stock)}",
        xaxis_title="Quarters"
    )

    fig.update_traces(line=dict(width=2))

    # ====== Boxplot ======
    fig2 = px.box(
        dfv_fltrd,
        color="Company",
        x="Company",
        y=selected_numeric,
        width=1000,
        height=500
    )
    fig2.update_layout(title=f"{selected_numeric} de {', '.join(selected_stock)}")

    # ====== Tabla ======
    df_reshaped = dfv_fltrd.pivot(index="Company", columns="Quarter", values=selected_numeric)
    df_reshaped2 = df_reshaped.reset_index()

    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_reshaped2.columns],
        data=df_reshaped2.to_dict("records"),
        export_format="csv",
        fill_width=True,
        style_cell={"fontSize": "12px"},
        style_header={"backgroundColor": "blue", "color": "white", "fontWeight": "bold"},
        style_data={"backgroundColor": "white", "color": "black"}
    )

    return fig, fig2, table


# ====== Paso 5: Correr app ======
#Github : en la version para git hay que agregar el host 
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0",port=10000)
