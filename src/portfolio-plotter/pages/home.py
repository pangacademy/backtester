# package imports
import dash
from dash import html, _dash_renderer
import dash_mantine_components as dmc

import pandas as pd

# utils
from utils import performanceMetric

# components
from components.header import header
from components.docUpload import docUpload
from components.footer import footer
from components.performanceCard import create_performance_card

_dash_renderer._set_react_version("18.2.0")

dash.register_page(
    __name__,
    path='/',
    redirect_from=['/home'],
    title='Home'
)

# daily PNL Graph
df = pd.read_csv('../data/BuyandHold_EQL_DOLLAR_pnl.csv')

data = df.to_dict(orient='records')

# data = [
#   {"date": "Mar 22", "Apples": 2890, "Oranges": 2338, "Tomatoes": 2452},
#   {"date": "Mar 23", "Apples": 2756, "Oranges": 2103, "Tomatoes": 2402},
#   {"date": "Mar 24", "Apples": 3322, "Oranges": 986, "Tomatoes": 1821},
#   {"date": "Mar 25", "Apples": 3470, "Oranges": 2108, "Tomatoes": 2809},
#   {"date": "Mar 26", "Apples": 3129, "Oranges": 1726, "Tomatoes": 2290}
# ]
layout = dmc.MantineProvider(
    forceColorScheme="light",
    id="mantine-provider",
    children= [
        dmc.AppShell(
            children=[
                header,
                dmc.AppShellNavbar("Navbar"),
                dmc.AppShellMain(
                    children=[
                        dmc.Stack(
                            [
                                docUpload,
                                dmc.Group(
                                    align={"sm": "center"},
                                    children=[
                                        create_performance_card("Cumulative Return", 100 * df['cumulative_pnl'].iloc[-1] / 1-000-000),
                                        create_performance_card("Sharpe Ratio", performanceMetric.calculate_sharpe_ratio(
                                            df['cumulative_pnl'].diff(periods = 1) / df['total_value'])),
                                        create_performance_card("Maximum Drawdown", performanceMetric.calculate_max_drawdown(df['total_value'])),
                                    ]
                                ),
                                html.Div(id='output-data-upload'),
                                dmc.Title(f"Equity Curve", order=1),
                                dmc.Divider(size="md"),
                                dmc.LineChart(
                                    h=300,
                                    dataKey="Date",
                                    data=data,
                                    withLegend=True,
                                    series=[
                                        {"name": "total_value", "color": "indigo.6"},
                                    ],
                                    curveType="linear",
                                    gridAxis="xy",
                                    tickLine="xy",
                                    xAxisLabel="Date",
                                    yAxisLabel="Equity",
                                    withDots=False,
                                    xAxisProps={"angle": -20},
                                    legendProps={"verticalAlign": "bottom", "height": 50},
                                    lineChartProps={"syncId": "equity-curve"},
                                ),
                                dmc.Title(f"Daily Profit & Loss Curve", order=1),
                                dmc.Divider(size="md"),
                                dmc.LineChart(
                                    h=300,
                                    dataKey="Date",
                                    data=data,
                                    withLegend=True,
                                    series=[
                                        {"name": "daily pnl returns", "color": "teal.6"},
                                    ],
                                    curveType="linear",
                                    tickLine="xy",
                                    gridAxis="xy",
                                    xAxisLabel="Date",
                                    yAxisLabel="PNL Returns",
                                    withDots=False,
                                    xAxisProps={"angle": -20},
                                    legendProps={"verticalAlign": "bottom", "height": 50},
                                    lineChartProps={"syncId": "equity-curve"},
                                )
                            ]
                        ),
                    ]),
                    footer
            ],
            # bg="#f8f9fa",
            padding="xl",
            zIndex=1400,
            header={"height": 100, "display":"flex", "alignItems":"center"},
            footer={"height": 75},
            navbar={
                "width": 350,
                "breakpoint": "sm",
                "collapsed": {"mobile": True},
            },
        )
    ]
)


