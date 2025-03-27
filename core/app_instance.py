from dash import Dash
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    pages_folder="pages",  # <-- ajoute ce paramètre pour forcer Dash à voir le bon dossier
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

server = app.server