
import dash
from dash import Dash, Input, Output, State, callback

import dash_mantine_components as dmc

footer = dmc.AppShellFooter(
                children=[
                    dmc.Stack(
                        justify="center",
                        h="100%",
                        children=dmc.Grid(
                            justify="center",
                            align="center",
                            children = [
                                dmc.GridCol(
                                    dmc.Text(
                                        "© 2024 Temple Trading & Technology Club",
                                        ta="center"
                                    )
                                )
                            ]
                        )
                    )

                ]
            )

