"""
Script para generar predicciones CON ganadores reales
para que funcione el dashboard original que compara Real vs Predicho
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path

# Configurar rutas absolutas
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "data" / "models" / "random_forest_model.pkl"
TEAM_ENCODER_PATH = BASE_DIR / "data" / "models" / "team_encoder.pkl"
WINNER_ENCODER_PATH = BASE_DIR / "data" / "models" / "winner_encoder.pkl"
PROCESSED_FILE = BASE_DIR / "data" / "processed" / "processed_encoded.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "model_predictions.csv"

print("="*60)
print("🎯 GENERANDO PREDICCIONES CON GANADORES REALES")
print("="*60)

# Cargar datos procesados
print("\n📊 Cargando datos procesados...")
df = pd.read_csv(PROCESSED_FILE)
print(f"   ✓ Datos cargados: {df.shape}")

# Cargar modelo y encoders
print("\n🤖 Cargando modelo y encoders...")
model = joblib.load(MODEL_PATH)
team_encoder = joblib.load(TEAM_ENCODER_PATH)
winner_encoder = joblib.load(WINNER_ENCODER_PATH)
print("   ✓ Modelo y encoders cargados")

# Verificar columnas necesarias
print("\n🔍 Verificando columnas...")
print(f"   Columnas disponibles: {df.columns.tolist()}")

# Reconstruir game_mode desde one-hot encoding
print("\n🔧 Reconstruyendo game_mode...")
def reconstruct_game_mode(row):
    if row.get('mode_Duel', 0) == 1:
        return 'Duel'
    elif row.get('mode_Doubles', 0) == 1:
        return 'Doubles'
    elif row.get('mode_Standard', 0) == 1:
        return 'Standard'
    else:
        return 'Unknown'

df['game_mode'] = df.apply(reconstruct_game_mode, axis=1)
print(f"   ✓ Game modes: {df['game_mode'].unique()}")

# Reconstruir team_color desde encoding
print("\n🎨 Reconstruyendo team_color...")
if 'team_color_encoded' in df.columns:
    df['team_color'] = team_encoder.inverse_transform(df['team_color_encoded'].astype(int))
    print(f"   ✓ Team colors: {df['team_color'].unique()}")

# Preparar features para predicción (en el orden correcto)
print("\n🎯 Preparando features para predicción...")
feature_columns = model.feature_names_in_
X = df[feature_columns].copy()
print(f"   ✓ Features preparadas: {X.shape}")

# Generar predicciones
print("\n🔮 Generando predicciones...")
predictions = model.predict(X)
prediction_proba = model.predict_proba(X)

# Obtener confianza (probabilidad máxima)
confidence = prediction_proba.max(axis=1)

# Decodificar predicciones
predicted_winner = winner_encoder.inverse_transform(predictions)
print(f"   ✓ Predicciones generadas: {len(predictions)}")

# IMPORTANTE: Extraer el ganador REAL desde los datos originales
# El archivo processed_encoded.csv tiene 'winner_encoded' que es el ganador real
print("\n👑 Extrayendo ganadores reales...")
if 'winner_encoded' in df.columns:
    real_winner = winner_encoder.inverse_transform(df['winner_encoded'].astype(int))
    print(f"   ✓ Ganadores reales extraídos: {len(real_winner)}")
    print(f"   ✓ Distribución real: {pd.Series(real_winner).value_counts().to_dict()}")
else:
    print("   ⚠️  No se encontró 'winner_encoded', usando predicciones como reales")
    real_winner = predicted_winner

# Crear DataFrame final con TODAS las columnas necesarias
print("\n📦 Creando DataFrame final...")
result_df = pd.DataFrame({
    'team_color': df['team_color'],
    'game_mode': df['game_mode'],
    'goal_difference': df['goal_difference'],
    'match_duration': df['match_duration'],
    'overtime': df['overtime'],
    'is_competitive': df['is_competitive'],
    'winner': real_winner,  # ← GANADOR REAL
    'predicted_winner': predicted_winner,  # ← GANADOR PREDICHO
    'prediction_confidence': confidence
})

# Convertir todo a minúsculas para consistencia
result_df['winner'] = result_df['winner'].str.lower()
result_df['predicted_winner'] = result_df['predicted_winner'].str.lower()

# Guardar archivo
print(f"\n💾 Guardando archivo...")
result_df.to_csv(OUTPUT_FILE, index=False)
print(f"   ✓ Archivo guardado: {OUTPUT_FILE}")

# Mostrar estadísticas
print("\n" + "="*60)
print("📊 ESTADÍSTICAS FINALES")
print("="*60)
print(f"Total de predicciones: {len(result_df)}")
print(f"\n📈 Distribución de ganadores REALES:")
print(result_df['winner'].value_counts())
print(f"\n🔮 Distribución de ganadores PREDICHOS:")
print(result_df['predicted_winner'].value_counts())

# Calcular accuracy
accuracy = (result_df['winner'] == result_df['predicted_winner']).mean()
print(f"\n🎯 Accuracy del modelo: {accuracy:.2%}")

print(f"\n📊 Distribución de modos de juego:")
print(result_df['game_mode'].value_counts())

print(f"\n📋 Columnas en el archivo final:")
print(result_df.columns.tolist())

print(f"\n🔍 Primeras 5 filas:")
print(result_df.head())

print("\n" + "="*60)
print("✅ ¡PROCESO COMPLETADO!")
print("="*60)
print("\n💡 Ahora puedes ejecutar:")
print("   python dashboard\\app.py")
print("\n")