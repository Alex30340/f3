import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import ta

dash.register_page(__name__, path="/analyse", name="Analyse")

layout = dbc.Container([
    html.H2("Analyse Technique Complète"),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='pair-selector',
            options=[
                {'label': 'EUR/USD', 'value': 'EURUSD=X'},
                {'label': 'BTC/USD', 'value': 'BTC-USD'},
                {'label': 'XAU/USD', 'value': 'GC=F'}
            ],
            value='EURUSD=X',
            style={'width': '100%'}
        ), md=6),
        dbc.Col(dcc.Dropdown(
            id='timeframe-selector',
            options=[
                {'label': '1H', 'value': '60m'},
                {'label': '4H', 'value': '240m'},
                {'label': 'Journalier', 'value': '1d'}
            ],
            value='1d',
            style={'width': '100%'}
        ), md=6)
    ]),
    html.Button("Analyser", id="analyze-button", className="btn btn-warning mt-2"),
    html.Div(id="results", className="mt-4"),
    dcc.Graph(id="chart")
], fluid=True)

def detect_levels(df, window=5):
    levels = []
    for i in range(window, len(df) - window):
        low = df['Low'].iloc[i]
        high = df['High'].iloc[i]
        is_support = all(low < df['Low'].iloc[i - j] and low < df['Low'].iloc[i + j] for j in range(1, window))
        is_resistance = all(high > df['High'].iloc[i - j] and high > df['High'].iloc[i + j] for j in range(1, window))
        if is_support or is_resistance:
            levels.append((df.index[i], low if is_support else high))
    return levels

def detect_candlestick_patterns(df):
    patterns = []
    for i in range(1, len(df)):
        o, h, l, c = df.iloc[i][['Open', 'High', 'Low', 'Close']]
        po, ph, pl, pc = df.iloc[i-1][['Open', 'High', 'Low', 'Close']]

        if abs(o - c) <= (h - l) * 0.1:
            patterns.append((df.index[i], 'Doji'))
        elif c > o and po > pc and c > po and o < pc:
            patterns.append((df.index[i], 'Engulfing Bullish'))
        elif o > c and pc > po and o > pc and c < po:
            patterns.append((df.index[i], 'Engulfing Bearish'))
        elif (h - l) > 3 * abs(o - c) and (c - l) / (0.001 + h - l) > 0.6:
            patterns.append((df.index[i], 'Hammer'))
        elif (h - l) > 3 * abs(o - c) and (h - c) / (0.001 + h - l) > 0.6:
            patterns.append((df.index[i], 'Shooting Star'))
    return patterns

@dash.get_app().callback(
    Output("results", "children"),
    Output("chart", "figure"),
    Input("analyze-button", "n_clicks"),
    State("pair-selector", "value"),
    State("timeframe-selector", "value")
)
def run_analysis(n, symbol, interval):
    if not symbol:
        return "Veuillez sélectionner une paire", go.Figure()
    df = yf.download(symbol, period="6mo", interval=interval)
    if df.empty:
        return "Données indisponibles.", go.Figure()
    df.dropna(inplace=True)
    df['EMA20'] = ta.trend.EMAIndicator(df['Close'], 20).ema_indicator()
    df['EMA50'] = ta.trend.EMAIndicator(df['Close'], 50).ema_indicator()
    df['EMA200'] = ta.trend.EMAIndicator(df['Close'], 200).ema_indicator()
    df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    macd = ta.trend.MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()
    levels = detect_levels(df)
    patterns = detect_candlestick_patterns(df)
    entry = df['Close'].iloc[-1]
    sl = round(entry * 0.98, 2)
    tp = round(entry * 1.03, 2)
    rr = round(abs(tp - entry) / abs(entry - sl), 2)
    alerts = []
    if df['RSI'].iloc[-1] > 70:
        alerts.append("RSI > 70 : Surachat")
    elif df['RSI'].iloc[-1] < 30:
        alerts.append("RSI < 30 : Survente")
    alerts.append("MACD haussier" if df['MACD'].iloc[-1] > df['MACD_signal'].iloc[-1] else "MACD baissier")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'], name="Bougies"
    ))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], line=dict(color='cyan'), name='EMA20'))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA50'], line=dict(color='orange'), name='EMA50'))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA200'], line=dict(color='red'), name='EMA200'))
    for date, level in levels:
        fig.add_shape(type="line", x0=date, x1=date, y0=level*0.995, y1=level*1.005,
                      line=dict(color="purple", width=1, dash="dot"))
    for date, name in patterns:
        fig.add_annotation(
            x=date,
            y=df.loc[date]['High'] * 1.01,
            text=name,
            showarrow=True,
            arrowhead=1,
            font=dict(color="yellow"),
            bgcolor="black"
        )
    fig.add_hline(y=entry, line_color="blue", line_dash="dot", annotation_text="Entrée")
    fig.add_hline(y=tp, line_color="green", line_dash="dash", annotation_text="TP")
    fig.add_hline(y=sl, line_color="red", line_dash="dash", annotation_text="SL")
    fig.update_layout(title=f"Analyse de {symbol} ({interval})", template="plotly_dark", height=650)
    return html.Div([
        html.H5(f"Entrée : {entry:.2f} | SL : {sl:.2f} | TP : {tp:.2f} | RR : {rr}"),
        html.Ul([html.Li(a) for a in alerts]) if alerts else html.P("Aucune alerte détectée.")
    ]), fig
