
import dash
from dash import Dash, Input, Output, State, callback, clientside_callback

import dash_mantine_components as dmc
from dash_iconify import DashIconify

theme_toggle = dmc.ActionIcon(
    [
        dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=True),
        dmc.Paper(DashIconify(icon="radix-icons:moon", width=25), lightHidden=True),
    ],
    variant="transparent",
    color="yellow",
    id="color-scheme-toggle",
    size="lg",
    ms="auto",
)

header = dmc.AppShellHeader(
        px=25,
        children=[
            dmc.Stack(
                justify="center",
                h="100%",
                children=dmc.Grid(
                    justify="space-between",
                    children=[
                        dmc.GridCol(
                            dmc.Group(
                                [
                                    dmc.Anchor(
                                        dmc.Title("TTT", order=1, style={"color": "black"}),
                                        size="xl", href="/", underline=False
                                    ),
                                ]
                            ),
                            span="content",
                        ),
                        dmc.GridCol(
                            span="auto",
                            children=dmc.Group(
                                justify="flex-end",
                                h="100%",
                                gap="xl",
                                children=[
                                    dmc.ActionIcon(
                                        [
                                            dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=True),
                                            dmc.Paper(DashIconify(icon="radix-icons:moon", width=25), lightHidden=True),

                                        ],
                                        variant="transparent",
                                        color="yellow",
                                        id="color-scheme-toggle",
                                        size="lg",
                                        ms="auto",
                                    ),
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="radix-icons:hamburger-menu",
                                            width=25,
                                        ),
                                        id="drawer-hamburger-button",
                                        variant="transparent",
                                        size="lg",
                                        hiddenFrom="sm",
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            )
        ],
    )



clientside_callback(
    """
    function(n_clicks, theme) {
        dash_clientside.set_props("mantine-provider", {
            forceColorScheme: theme === "dark" ? "light" : "dark"
        });
        return dash_clientside.no_update
    }
    """,
    Output("mantine-provider", "forceColorScheme"),
    Input("color-scheme-toggle", "n_clicks"),
    State("mantine-provider", "forceColorScheme"),
    prevent_initial_call=True,
)