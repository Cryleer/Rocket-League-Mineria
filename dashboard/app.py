import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import requests
from datetime import datetime
from pathlib import Path

# === App con Bootstrap ===
app = Dash(__name__, external_stylesheets=[
    dbc.themes.LUX,
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
])

# === Variable global para datos ===
BASE_DIR = Path(__file__).resolve().parent.parent
PREDICTIONS_FILE = BASE_DIR / "data" / "processed" / "model_predictions.csv"
df = pd.read_csv(PREDICTIONS_FILE)

# === Calcular métricas globales ===
def calculate_metrics(data):
    if "winner" in data.columns:
        accuracy = (data["winner"] == data["predicted_winner"]).mean() * 100
    else:
        accuracy = data.get("prediction_confidence", pd.Series([0.95] * len(data))).mean() * 100
    total_matches = len(data)
    blue_wins = (data["predicted_winner"] == "blue").sum()
    orange_wins = (data["predicted_winner"] == "orange").sum()
    return accuracy, total_matches, blue_wins, orange_wins

accuracy, total_matches, blue_wins, orange_wins = calculate_metrics(df)

# === Layout Moderno ===
app.layout = dbc.Container([
    # Store para manejar datos actualizados
    dcc.Store(id='data-store', data=df.to_dict('records')),
    # Interval para simular loading
    dcc.Interval(id='interval-loading', interval=500, n_intervals=0, disabled=True),
    
    # Header con gradiente
    html.Div([
        html.H1("🚀 Rocket League ML Dashboard", 
                className="text-white text-center mb-0 py-4 fw-bold",
                style={"textShadow": "2px 2px 4px rgba(0,0,0,0.3)"}),
        html.P("Análisis predictivo de partidas competitivas", 
               className="text-white text-center mb-0 pb-3",
               style={"fontSize": "1.1rem", "opacity": "0.9"})
    ], style={
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "borderRadius": "15px",
        "marginBottom": "30px",
        "boxShadow": "0 10px 30px rgba(0,0,0,0.2)"
    }),

    # KPIs Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-bullseye", style={"fontSize": "2.5rem", "color": "#667eea"}),
                        html.H3(id="accuracy-kpi", children=f"{accuracy:.1f}%", className="mt-3 mb-0 fw-bold"),
                        html.P("Confianza Promedio" if "winner" not in df.columns else "Precisión del Modelo", className="text-muted mb-0")
                    ], className="text-center")
                ])
            ], className="shadow-sm border-0 h-100", style={"borderRadius": "12px"})
        ], width=12, lg=3, className="mb-3"),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-gamepad", style={"fontSize": "2.5rem", "color": "#f093fb"}),
                        html.H3(id="total-matches-kpi", children=f"{total_matches:,}", className="mt-3 mb-0 fw-bold"),
                        html.P("Partidas Analizadas", className="text-muted mb-0")
                    ], className="text-center")
                ])
            ], className="shadow-sm border-0 h-100", style={"borderRadius": "12px"})
        ], width=12, lg=3, className="mb-3"),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-trophy", style={"fontSize": "2.5rem", "color": "#4facfe"}),
                        html.H3(id="blue-wins-kpi", children=f"{blue_wins:,}", className="mt-3 mb-0 fw-bold"),
                        html.P("Victorias Azul", className="text-muted mb-0")
                    ], className="text-center")
                ])
            ], className="shadow-sm border-0 h-100", style={"borderRadius": "12px"})
        ], width=12, lg=3, className="mb-3"),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-fire", style={"fontSize": "2.5rem", "color": "#fa709a"}),
                        html.H3(id="orange-wins-kpi", children=f"{orange_wins:,}", className="mt-3 mb-0 fw-bold"),
                        html.P("Victorias Naranja", className="text-muted mb-0")
                    ], className="text-center")
                ])
            ], className="shadow-sm border-0 h-100", style={"borderRadius": "12px"})
        ], width=12, lg=3, className="mb-3"),
    ]),

    # Sección de control: Filtros y botón de generación
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("🎮 Filtrar por modo de juego", className="fw-bold mb-2"),
                    dcc.Dropdown(
                        options=[{"label": m, "value": m} for m in sorted(df["game_mode"].unique())],
                        id="mode_filter",
                        placeholder="Todos los modos",
                        className="shadow-sm"
                    )
                ])
            ], className="shadow-sm border-0", style={"borderRadius": "12px"})
        ], width=12, lg=5, className="mb-4"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("🔮 Generar nuevas predicciones", className="fw-bold mb-2"),
                    dbc.InputGroup([
                        dbc.Input(
                            id="n-matches-input",
                            type="number",
                            min=10,
                            max=500,
                            value=100,
                            placeholder="Cantidad"
                        ),
                        dbc.Button(
                            [html.I(className="fas fa-magic me-2"), "Generar"],
                            id="generate_btn",
                            color="primary",
                            n_clicks=0
                        )
                    ])
                ])
            ], className="shadow-sm border-0", style={"borderRadius": "12px"})
        ], width=12, lg=5, className="mb-4"),
        
        dbc.Col([
            html.Div(id="prediction_status", className="mt-3")
        ], width=12, lg=2, className="mb-4"),
    ], justify="center"),

    # Gráficos principales
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-chart-pie me-2"),
                    "Distribución de Predicciones"
                ], className="fw-bold bg-white border-0"),
                dbc.CardBody([dcc.Graph(id="pie_graph", config={"displayModeBar": False})])
            ], className="shadow-sm border-0 h-100", style={"borderRadius": "12px"})
        ], width=12, lg=6, className="mb-4"),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-balance-scale me-2"),
                    "Predicciones por Modo" if "winner" not in df.columns else "Real vs Predicho"
                ], className="fw-bold bg-white border-0"),
                dbc.CardBody([dcc.Graph(id="compare_graph", config={"displayModeBar": False})])
            ], className="shadow-sm border-0 h-100", style={"borderRadius": "12px"})
        ], width=12, lg=6, className="mb-4"),
    ]),

    # Gráfico grande
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-chart-bar me-2"),
                    "Análisis de Diferencia de Goles"
                ], className="fw-bold bg-white border-0"),
                dbc.CardBody([dcc.Graph(id="goal_diff_graph", config={"displayModeBar": False})])
            ], className="shadow-sm border-0", style={"borderRadius": "12px"})
        ], width=12, className="mb-4")
    ]),

    # Footer
    html.Div([
        html.P("Desarrollado con Machine Learning | Santo Tomás 2025", 
               className="text-center text-muted mb-0 py-3")
    ]),
    
    # Modal de carga
    dbc.Modal([
        dbc.ModalBody([
            html.Div([
                dbc.Spinner(
                    color="primary",
                    type="border",
                    size="lg",
                    spinner_style={"width": "4rem", "height": "4rem"}
                ),
                html.H5(id="loading-message", className="mt-3 text-center", children="Generando predicciones...")
            ], style={"textAlign": "center"})
        ], style={"padding": "3rem"})
    ], id="loading-modal", is_open=False, centered=True, backdrop="static", keyboard=False),
    
], fluid=True, style={"paddingTop": "20px", "paddingBottom": "20px"})

# === Callback principal para generar predicciones ===
@app.callback(
    [Output("prediction_status", "children"),
     Output("data-store", "data"),
     Output("loading-modal", "is_open"),
     Output("loading-message", "children")],
    [Input("generate_btn", "n_clicks")],
    [State("n-matches-input", "value"),
     State("mode_filter", "value")],
    prevent_initial_call=True
)
def generate_predictions(n_clicks, n_matches, selected_mode):
    if n_clicks == 0:
        return "", df.to_dict('records'), False, ""
    
    try:
        # Validar entrada
        if not n_matches or n_matches < 10:
            return dbc.Alert(
                "❌ Ingresa al menos 10 partidas",
                color="warning",
                duration=4000
            ), df.to_dict('records'), False, ""
        
        # Mostrar mensaje de carga inicial
        loading_msg = f"Generando {n_matches} partidas sintéticas basadas en distribuciones reales..."
        
        # Llamar a la API
        api_url = "http://localhost:8000/generate_synthetic"
        payload = {
            "n_matches": int(n_matches),
            "game_mode": selected_mode if selected_mode else None
        }
        
        response = requests.post(api_url, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            
            # Cargar los nuevos datos generados
            synthetic_file = BASE_DIR / "data" / "processed" / "synthetic_predictions.csv"
            new_df = pd.read_csv(synthetic_file)
            
            # Cerrar modal y mostrar éxito
            return dbc.Alert([
                html.I(className="fas fa-check-circle me-2"),
                html.Strong("✅ ¡Éxito! "),
                f"Generadas {result['summary']['total_matches']} predicciones sintéticas.",
                html.Br(),
                html.Small([
                    f"Confianza promedio: {result['summary']['avg_confidence']:.2%} | ",
                    f"Blue: {result['summary']['predictions'].get('blue', 0)} | ",
                    f"Orange: {result['summary']['predictions'].get('orange', 0)} | ",
                    f"Draw: {result['summary']['predictions'].get('draw', 0)}"
                ])
            ], color="success", duration=6000), new_df.to_dict('records'), False, ""
        else:
            return dbc.Alert(
                f"❌ Error del servidor: {response.status_code}",
                color="danger",
                duration=4000
            ), df.to_dict('records'), False, ""
            
    except requests.exceptions.ConnectionError:
        return dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            "❌ No se pudo conectar con la API. ",
            html.Br(),
            html.Small("Asegúrate de que el servidor FastAPI esté corriendo en http://localhost:8000")
        ], color="danger", duration=6000), df.to_dict('records'), False, ""
    
    except requests.exceptions.Timeout:
        return dbc.Alert(
            "❌ Timeout: La generación tomó demasiado tiempo. Intenta con menos partidas.",
            color="warning",
            duration=5000
        ), df.to_dict('records'), False, ""
    
    except Exception as e:
        return dbc.Alert(
            f"❌ Error inesperado: {str(e)}",
            color="danger",
            duration=4000
        ), df.to_dict('records'), False, ""

# Callback separado para abrir el modal inmediatamente al hacer clic
@app.callback(
    Output("loading-modal", "is_open", allow_duplicate=True),
    Output("loading-message", "children", allow_duplicate=True),
    Input("generate_btn", "n_clicks"),
    State("n-matches-input", "value"),
    prevent_initial_call=True
)
def open_loading_modal(n_clicks, n_matches):
    if n_clicks > 0 and n_matches and n_matches >= 10:
        return True, f"Procesando {n_matches} predicciones... Por favor espera."
    return False, ""

# === Callback para actualizar gráficos y KPIs ===
@app.callback(
    [Output("pie_graph", "figure"),
     Output("compare_graph", "figure"),
     Output("goal_diff_graph", "figure"),
     Output("accuracy-kpi", "children"),
     Output("total-matches-kpi", "children"),
     Output("blue-wins-kpi", "children"),
     Output("orange-wins-kpi", "children")],
    [Input("mode_filter", "value"),
     Input("data-store", "data")]
)
def update_graphs(selected_mode, stored_data):
    # Convertir data store a DataFrame
    current_df = pd.DataFrame(stored_data)
    
    filtered = current_df.copy()
    if selected_mode:
        filtered = filtered[filtered["game_mode"] == selected_mode]

    # Calcular KPIs actualizados
    acc, total, blue, orange = calculate_metrics(filtered)

    # Gráfico de torta mejorado con colores correctos
    pred_counts = filtered["predicted_winner"].value_counts().reset_index()
    pred_counts.columns = ["winner", "count"]
    
    color_map = {
        "blue": "#0660afe6",
        "orange": "#ee8906",
        "draw": "#95a5a6"
    }
    
    pie_colors = [color_map.get(str(winner).lower(), "#667eea") for winner in pred_counts["winner"]]
    
    pie_fig = go.Figure(data=[go.Pie(
        labels=[str(w).capitalize() for w in pred_counts["winner"]],
        values=pred_counts["count"],
        hole=0.4,
        marker=dict(
            colors=pie_colors,
            line=dict(color='white', width=2)
        ),
        textinfo='label+percent',
        textfont=dict(size=14, color='white'),
        hovertemplate='<b>%{label}</b><br>Cantidad: %{value}<br>Porcentaje: %{percent}<extra></extra>'
    )])
    pie_fig.update_layout(
        showlegend=True,
        height=350,
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )

    # Gráfico de comparación
    if "winner" in filtered.columns:
        compare = filtered.groupby(["winner", "predicted_winner"]).size().reset_index(name="count")
        compare["winner"] = compare["winner"].str.capitalize()
        compare["predicted_winner"] = compare["predicted_winner"].str.capitalize()
        
        compare_fig = px.bar(
            compare, 
            x="winner", 
            y="count", 
            color="predicted_winner",
            barmode="group",
            color_discrete_map={
                "Blue": "#0b81e9", 
                "Orange": "#ec8209",
                "Draw": "#95a5a6"
            }
        )
        compare_fig.update_layout(
            height=350,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Ganador Real", showgrid=False, tickfont=dict(size=12)),
            yaxis=dict(title="Cantidad", showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            legend=dict(title="Predicción", orientation="h", y=-0.2, x=0.5, xanchor="center"),
            hovermode='x unified'
        )
    else:
        compare = filtered.groupby(["game_mode", "predicted_winner"]).size().reset_index(name="count")
        compare["game_mode"] = compare["game_mode"].str.capitalize()
        compare["predicted_winner"] = compare["predicted_winner"].str.capitalize()
        
        compare_fig = px.bar(
            compare, 
            x="game_mode", 
            y="count", 
            color="predicted_winner",
            barmode="group",
            color_discrete_map={
                "Blue": "#0b81e9", 
                "Orange": "#ec8209",
                "Draw": "#95a5a6"
            }
        )
        compare_fig.update_layout(
            height=350,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Modo de Juego", showgrid=False, tickfont=dict(size=12)),
            yaxis=dict(title="Cantidad", showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            legend=dict(title="Predicción", orientation="h", y=-0.2, x=0.5, xanchor="center"),
            hovermode='x unified'
        )

    # Histograma
    goal_diff_fig = go.Figure(data=[go.Histogram(
        x=filtered["goal_difference"],
        nbinsx=20,
        marker=dict(color="#c904cf", line=dict(color='white', width=1)),
        hovertemplate='Diferencia: %{x}<br>Frecuencia: %{y}<extra></extra>'
    )])
    goal_diff_fig.update_layout(
        height=350,
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title="Diferencia de Goles", showgrid=False, zeroline=True, zerolinewidth=2, zerolinecolor='rgba(0,0,0,0.2)'),
        yaxis=dict(title="Frecuencia", showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
        bargap=0.1
    )

    return (pie_fig, compare_fig, goal_diff_fig, 
            f"{acc:.1f}%", f"{total:,}", f"{blue:,}", f"{orange:,}")

if __name__ == "__main__":
    app.run(debug=True, port=8050)