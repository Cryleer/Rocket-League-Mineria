"""
API de Predicción de Ganadores de Rocket League
Versión 2.6 - Compatible con todos los tests
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# === CONFIGURACIÓN DE RUTAS ABSOLUTAS ===
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = DATA_DIR / "models"

MODEL_PATH = MODELS_DIR / "random_forest_model.pkl"
TEAM_ENCODER_PATH = MODELS_DIR / "team_encoder.pkl"
WINNER_ENCODER_PATH = MODELS_DIR / "winner_encoder.pkl"

print("=== INICIANDO API v2.6 (COMPATIBLE CON TESTS) ===")
print(f"Directorio base: {BASE_DIR}")
print(f"Cargando modelo desde: {MODEL_PATH}")

# === CARGA DE MODELOS ===
try:
    model = joblib.load(MODEL_PATH)
    team_encoder = joblib.load(TEAM_ENCODER_PATH)
    winner_encoder = joblib.load(WINNER_ENCODER_PATH)
    
    if hasattr(model, 'feature_names_in_'):
        print(f"✅ Modelos cargados. Features esperadas ({len(model.feature_names_in_)}):")
        for i, name in enumerate(model.feature_names_in_):
            print(f"  {i}: {name}")
    else:
        print(f"✅ Modelos cargados. N features: {model.n_features_in_}")
        
except Exception as e:
    print(f"❌ ERROR AL CARGAR ARCHIVOS: {e}")
    import traceback
    traceback.print_exc()
    raise

# === INICIALIZAR APP ===
app = FastAPI(
    title="Rocket League Winner Prediction API",
    description="API para predecir el ganador de partidas de Rocket League",
    version="2.6"
)

# === MODELOS PYDANTIC ===
class MatchInput(BaseModel):
    team_color: str
    game_mode: str
    goal_difference: int
    match_duration: int
    overtime: bool
    is_competitive: Optional[int] = 0  # Opcional con default 0
    
    class Config:
        json_schema_extra = {
            "example": {
                "team_color": "Blue",
                "game_mode": "Standard",
                "goal_difference": 3,
                "match_duration": 300,
                "overtime": False,
                "is_competitive": 1
            }
        }

class SyntheticRequest(BaseModel):
    n_matches: int = 100
    game_mode: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "n_matches": 100,
                "game_mode": "Standard"
            }
        }

# === FUNCIONES AUXILIARES ===
def normalize_team_color(color: str) -> str:
    """Normaliza color del equipo - retorna capitalizado"""
    color_map = {
        "blue": "Blue", "azul": "Blue", "b": "Blue",
        "orange": "Orange", "naranja": "Orange", "o": "Orange"
    }
    return color_map.get(color.lower(), color.capitalize())

def normalize_winner(winner: str) -> str:
    """Normaliza ganador - retorna capitalizado"""
    winner_map = {
        "blue": "Blue", "azul": "Blue", "b": "Blue",
        "orange": "Orange", "naranja": "Orange", "o": "Orange",
        "draw": "Draw", "empate": "Draw", "tie": "Draw"
    }
    return winner_map.get(winner.lower(), winner.capitalize())

def prepare_features(match: MatchInput) -> pd.DataFrame:
    """Prepara features en el formato correcto para el modelo"""
    
    # Normalizar entradas
    team_color = normalize_team_color(match.team_color)
    
    # Codificar team_color
    team_color_encoded = team_encoder.transform([team_color])[0]
    
    # Crear one-hot encoding para game_mode
    mode_duel = 1 if match.game_mode.lower() == "duel" else 0
    mode_doubles = 1 if match.game_mode.lower() == "doubles" else 0
    mode_standard = 1 if match.game_mode.lower() == "standard" else 0
    
    # Crear DataFrame con todas las features
    features_dict = {
        'team_color_encoded': team_color_encoded,
        'goal_difference': match.goal_difference,
        'match_duration': match.match_duration,
        'mode_Duel': mode_duel,
        'mode_Doubles': mode_doubles,
        'mode_Standard': mode_standard,
        'is_competitive': match.is_competitive if match.is_competitive is not None else 0,
        'overtime': int(match.overtime)
    }
    
    df = pd.DataFrame([features_dict])
    
    # Reordenar columnas según el modelo
    if hasattr(model, 'feature_names_in_'):
        df = df[model.feature_names_in_]
    
    return df

# === ENDPOINTS ===
@app.get("/")
async def root():
    """Root endpoint - compatible con tests"""
    return {
        "status": "active",
        "message": "Rocket League Winner Prediction API v2.6",
        "endpoints": {
            "predict": "/predict",
            "generate_synthetic": "/generate_synthetic",
            "stats": "/stats",
            "docs": "/docs"
        },
        "encoders": {
            "team_color_classes": team_encoder.classes_.tolist(),
            "winner_classes": winner_encoder.classes_.tolist()
        }
    }

@app.post("/predict")
async def predict_winner(match: MatchInput):
    """
    Predice el ganador de una partida de Rocket League
    Retorna formato compatible con tests
    """
    try:
        # Preparar features
        X = prepare_features(match)
        
        # Realizar predicción
        prediction = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0]
        
        # Decodificar predicción
        predicted_winner = winner_encoder.inverse_transform([prediction])[0]
        predicted_winner = normalize_winner(predicted_winner)
        
        # Obtener probabilidades por clase
        winner_classes = [normalize_winner(w) for w in winner_encoder.classes_]
        prob_dict = {winner_classes[i]: float(probabilities[i]) for i in range(len(winner_classes))}
        
        return {
            "winner_prediction": predicted_winner,  # Nombre esperado por tests
            "predicted_winner": predicted_winner,   # Mantener compatibilidad
            "confidence": float(max(probabilities)),
            "probabilities": prob_dict,
            "input_data": {
                "team_color": match.team_color,
                "game_mode": match.game_mode,
                "goal_difference": match.goal_difference,
                "match_duration": match.match_duration,
                "overtime": match.overtime,
                "is_competitive": match.is_competitive
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción: {str(e)}")

@app.post("/generate_synthetic")
async def generate_synthetic(request: SyntheticRequest):
    """Genera predicciones sintéticas"""
    try:
        n_matches = request.n_matches
        selected_mode = request.game_mode
        
        print(f"\n🔮 Generando {n_matches} partidas sintéticas...")
        if selected_mode:
            print(f"   Modo seleccionado: {selected_mode}")
        
        # Generar datos sintéticos
        np.random.seed(int(datetime.now().timestamp()))
        
        game_modes = ["Duel", "Doubles", "Standard"]
        team_colors = ["Blue", "Orange"]
        
        if selected_mode and selected_mode in game_modes:
            modes = [selected_mode] * n_matches
        else:
            modes = np.random.choice(game_modes, n_matches)
        
        # Generar features sintéticas
        synthetic_data = []
        for i in range(n_matches):
            goal_diff = int(np.random.normal(0, 3))
            goal_diff = max(-10, min(10, goal_diff))
            
            duration = int(np.random.normal(300, 60))
            duration = max(180, min(600, duration))
            
            overtime = np.random.random() < 0.2
            if overtime:
                duration += int(np.random.uniform(30, 120))
            
            is_comp = 1 if np.random.random() < 0.7 else 0
            team_color = np.random.choice(team_colors)
            
            match_data = MatchInput(
                team_color=team_color,
                game_mode=modes[i],
                goal_difference=goal_diff,
                match_duration=duration,
                overtime=overtime,
                is_competitive=is_comp
            )
            
            # Predecir
            X = prepare_features(match_data)
            prediction = model.predict(X)[0]
            probabilities = model.predict_proba(X)[0]
            predicted_winner = winner_encoder.inverse_transform([prediction])[0]
            
            synthetic_data.append({
                'team_color': team_color,
                'game_mode': modes[i],
                'goal_difference': goal_diff,
                'match_duration': duration,
                'overtime': overtime,
                'is_competitive': is_comp,
                'predicted_winner': normalize_winner(predicted_winner).lower(),
                'prediction_confidence': float(max(probabilities))
            })
        
        # Crear DataFrame y guardar
        df = pd.DataFrame(synthetic_data)
        output_path = DATA_DIR / "processed" / "synthetic_predictions.csv"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        
        # Calcular estadísticas
        winner_counts = df['predicted_winner'].value_counts().to_dict()
        avg_confidence = df['prediction_confidence'].mean()
        
        print(f"   ✅ {n_matches} predicciones generadas")
        print(f"   📊 Distribución: {winner_counts}")
        print(f"   🎯 Confianza promedio: {avg_confidence:.2%}")
        
        return {
            "status": "success",
            "file_path": str(output_path),
            "summary": {
                "total_matches": n_matches,
                "predictions": winner_counts,
                "avg_confidence": float(avg_confidence),
                "game_mode_filter": selected_mode
            }
        }
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al generar datos sintéticos: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Obtiene estadísticas del modelo y datos"""
    try:
        predictions_path = DATA_DIR / "processed" / "model_predictions.csv"
        
        if predictions_path.exists():
            df = pd.read_csv(predictions_path)
            
            stats = {
                "total_matches": len(df),
                "game_modes": df['game_mode'].value_counts().to_dict(),
                "predicted_winner_distribution": df['predicted_winner'].value_counts().to_dict(),
                "avg_match_duration": float(df['match_duration'].mean()),
                "overtime_percentage": float((df['overtime'].sum() / len(df)) * 100),
                "goal_difference_stats": {
                    "mean": float(df['goal_difference'].mean()),
                    "std": float(df['goal_difference'].std()),
                    "min": int(df['goal_difference'].min()),
                    "max": int(df['goal_difference'].max())
                }
            }
            
            return stats
        else:
            return {
                "message": "No hay predicciones guardadas aún",
                "total_matches": 0
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    print("\n=== INICIANDO SERVIDOR ===")
    print("Accede a: http://localhost:8000")
    print("Documentación: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)