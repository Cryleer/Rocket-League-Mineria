"""
Script para generar predicciones batch del modelo
Crea el archivo model_predictions.csv necesario para el dashboard
Versión 2.0 - Reconstruye columnas originales
"""

import pandas as pd
import joblib
from pathlib import Path

# Rutas
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = DATA_DIR / "models"
PROCESSED_DIR = DATA_DIR / "processed"

# Cargar datos procesados
print("📊 Cargando datos...")
df = pd.read_csv(PROCESSED_DIR / "processed_encoded.csv")

# Reconstruir game_mode desde las columnas one-hot
print("🔧 Reconstruyendo columnas originales...")
def reconstruct_game_mode(row):
    if row.get('mode_Duel', 0) == 1:
        return 'Duel'
    elif row.get('mode_Doubles', 0) == 1:
        return 'Doubles'
    elif row.get('mode_Standard', 0) == 1:
        return 'Standard'
    return 'Unknown'

df['game_mode'] = df.apply(reconstruct_game_mode, axis=1)

# Reconstruir team_color desde team_color_encoded
team_encoder = joblib.load(MODELS_DIR / "team_encoder.pkl")
if 'team_color_encoded' in df.columns:
    df['team_color'] = team_encoder.inverse_transform(df['team_color_encoded'].astype(int))
elif 'team_color' not in df.columns:
    df['team_color'] = 'Blue'  # Default

# Asegurar que existan las columnas necesarias
required_cols = ['goal_difference', 'match_duration', 'overtime']
for col in required_cols:
    if col not in df.columns:
        print(f"⚠️  Columna {col} no encontrada, usando valores por defecto")
        if col == 'overtime':
            df[col] = 0
        elif col == 'goal_difference':
            df[col] = 0
        elif col == 'match_duration':
            df[col] = 300

# Cargar modelo y encoders
print("🤖 Cargando modelo...")
model = joblib.load(MODELS_DIR / "random_forest_model.pkl")
winner_encoder = joblib.load(MODELS_DIR / "winner_encoder.pkl")

# Preparar features para predicción
print("🎯 Preparando features para predicción...")
feature_cols = [
    'team_color_encoded',
    'goal_difference', 
    'match_duration',
    'mode_Duel',
    'mode_Doubles',
    'mode_Standard',
    'is_competitive',
    'overtime'
]

X = df[feature_cols]

# Hacer predicciones
print("🔮 Generando predicciones...")
predictions = model.predict(X)
probabilities = model.predict_proba(X)

# Decodificar predicciones
predicted_winners = winner_encoder.inverse_transform(predictions)

# Crear DataFrame final con columnas necesarias para el dashboard
output_df = pd.DataFrame({
    'team_color': df['team_color'],
    'game_mode': df['game_mode'],
    'goal_difference': df['goal_difference'],
    'match_duration': df['match_duration'],
    'overtime': df['overtime'],
    'is_competitive': df['is_competitive'],
    'predicted_winner': predicted_winners,
    'prediction_confidence': probabilities.max(axis=1)
})

# Guardar
output_path = PROCESSED_DIR / "model_predictions.csv"
output_df.to_csv(output_path, index=False)

print(f"\n✅ Predicciones guardadas en: {output_path}")
print(f"📈 Total de predicciones: {len(output_df)}")
print(f"\n📊 Distribución de ganadores predichos:")
print(output_df['predicted_winner'].value_counts())
print(f"\n📊 Distribución de modos de juego:")
print(output_df['game_mode'].value_counts())
print(f"\n📊 Columnas en el archivo final:")
print(output_df.columns.tolist())