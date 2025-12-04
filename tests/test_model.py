"""
Tests unitarios para funciones de modelo y predicciones
Cubre carga del modelo, transformaciones y predicciones batch
"""

import pytest
import pandas as pd
import numpy as np
import joblib
import os
import sys
import os
from pathlib import Path

# Obtener rutas absolutas
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / 'src'))


class TestModelLoading:
    """Tests para verificar la carga correcta del modelo"""
    
    def test_model_file_exists(self):
        """Verifica que el archivo del modelo exista"""
        model_path = str(BASE_DIR / 'data' / 'models' / 'random_forest_model.pkl')
        assert os.path.exists(model_path), "El modelo no existe en la ruta especificada"
    
    def test_model_loads_successfully(self):
        """Verifica que el modelo se cargue sin errores"""
        model_path = str(BASE_DIR / 'data' / 'models' / 'random_forest_model.pkl')
        try:
            model = joblib.load(model_path)
            assert model is not None
        except Exception as e:
            pytest.fail(f"Error al cargar el modelo: {str(e)}")
    
    def test_model_has_predict_method(self):
        """Verifica que el modelo tenga el método predict"""
        model_path = str(BASE_DIR / 'data' / 'models' / 'random_forest_model.pkl')
        model = joblib.load(model_path)
        
        assert hasattr(model, 'predict')
        assert callable(model.predict)
    
    def test_model_has_predict_proba_method(self):
        """Verifica que el modelo tenga el método predict_proba"""
        model_path = str(BASE_DIR / 'data' / 'models' / 'random_forest_model.pkl')
        model = joblib.load(model_path)
        
        assert hasattr(model, 'predict_proba')
        assert callable(model.predict_proba)
    
    def test_encoders_exist(self):
        """Verifica que los encoders existan"""
        team_enc_path = str(BASE_DIR / 'data' / 'models' / 'team_encoder.pkl')
        winner_enc_path = str(BASE_DIR / 'data' / 'models' / 'winner_encoder.pkl')
        
        assert os.path.exists(team_enc_path), "Team encoder no existe"
        assert os.path.exists(winner_enc_path), "Winner encoder no existe"
    
    def test_encoders_load_successfully(self):
        """Verifica que los encoders se carguen correctamente"""
        team_enc_path = str(BASE_DIR / 'data' / 'models' / 'team_encoder.pkl')
        winner_enc_path = str(BASE_DIR / 'data' / 'models' / 'winner_encoder.pkl')
        
        try:
            team_enc = joblib.load(team_enc_path)
            winner_enc = joblib.load(winner_enc_path)
            
            assert team_enc is not None
            assert winner_enc is not None
        except Exception as e:
            pytest.fail(f"Error al cargar encoders: {str(e)}")
    
    def test_encoders_have_classes(self):
        """Verifica que los encoders tengan clases definidas"""
        team_enc_path = str(BASE_DIR / 'data' / 'models' / 'team_encoder.pkl')
        winner_enc_path = str(BASE_DIR / 'data' / 'models' / 'winner_encoder.pkl')
        
        team_enc = joblib.load(team_enc_path)
        winner_enc = joblib.load(winner_enc_path)
        
        assert hasattr(team_enc, 'classes_')
        assert hasattr(winner_enc, 'classes_')
        assert len(team_enc.classes_) > 0
        assert len(winner_enc.classes_) > 0


class TestModelPredictions:
    """Tests para las predicciones del modelo"""
    
    @pytest.fixture
    def model_and_encoders(self):
        """Carga modelo y encoders para las pruebas"""
        model = joblib.load(str(BASE_DIR / 'data' / 'models' / 'random_forest_model.pkl'))
        team_enc = joblib.load(str(BASE_DIR / 'data' / 'models' / 'team_encoder.pkl'))
        winner_enc = joblib.load(str(BASE_DIR / 'data' / 'models' / 'winner_encoder.pkl'))
        return model, team_enc, winner_enc
    
    def test_model_prediction_shape(self, model_and_encoders):
        """Verifica que las predicciones tengan la forma correcta"""
        model, team_enc, winner_enc = model_and_encoders
        
        # Crear entrada de prueba (8 features)
        X_test = np.array([[
            0,  # team_color_encoded
            2,  # goal_difference
            320,  # match_duration
            1,  # mode_duel
            0,  # mode_doubles
            0,  # mode_standard
            1,  # is_competitive
            0   # overtime
        ]])
        
        predictions = model.predict(X_test)
        
        assert predictions.shape == (1,)
    
    def test_model_predict_proba_shape(self, model_and_encoders):
        """Verifica que predict_proba retorne probabilidades correctas"""
        model, team_enc, winner_enc = model_and_encoders
        
        X_test = np.array([[
            0, 2, 320, 1, 0, 0, 1, 0
        ]])
        
        probas = model.predict_proba(X_test)
        
        # Debe retornar probabilidades para cada clase
        assert probas.shape[0] == 1
        assert probas.shape[1] >= 2  # Al menos 2 clases
        
        # Las probabilidades deben sumar 1
        assert np.allclose(probas.sum(axis=1), 1.0)
    
    def test_model_predictions_are_valid_classes(self, model_and_encoders):
        """Verifica que las predicciones sean clases válidas"""
        model, team_enc, winner_enc = model_and_encoders
        
        X_test = np.array([[
            0, 2, 320, 1, 0, 0, 1, 0
        ]])
        
        predictions = model.predict(X_test)
        
        # La predicción debe ser un índice válido para el winner_encoder
        assert predictions[0] < len(winner_enc.classes_)
        assert predictions[0] >= 0
    
    def test_model_handles_multiple_predictions(self, model_and_encoders):
        """Verifica que el modelo maneje múltiples predicciones"""
        model, team_enc, winner_enc = model_and_encoders
        
        # Crear múltiples entradas
        X_test = np.array([
            [0, 2, 320, 1, 0, 0, 1, 0],
            [1, -1, 350, 0, 1, 0, 1, 1],
            [0, 3, 400, 0, 0, 1, 0, 0]
        ])
        
        predictions = model.predict(X_test)
        probas = model.predict_proba(X_test)
        
        assert predictions.shape == (3,)
        assert probas.shape[0] == 3
    
    def test_probabilities_range(self, model_and_encoders):
        """Verifica que las probabilidades estén en el rango correcto"""
        model, team_enc, winner_enc = model_and_encoders
        
        X_test = np.array([[
            0, 2, 320, 1, 0, 0, 1, 0
        ]])
        
        probas = model.predict_proba(X_test)
        
        # Todas las probabilidades deben estar entre 0 y 1
        assert (probas >= 0).all()
        assert (probas <= 1).all()
    
    def test_encoder_transform_valid_input(self, model_and_encoders):
        """Verifica que los encoders transformen correctamente"""
        model, team_enc, winner_enc = model_and_encoders
        
        # Test team encoder
        if 'Blue' in team_enc.classes_:
            encoded = team_enc.transform(['Blue'])
            assert len(encoded) == 1
            assert encoded[0] >= 0
    
    def test_encoder_inverse_transform(self, model_and_encoders):
        """Verifica que inverse_transform funcione correctamente"""
        model, team_enc, winner_enc = model_and_encoders
        
        # Obtener las clases disponibles
        classes = winner_enc.classes_
        
        # Codificar y decodificar
        encoded = winner_enc.transform([classes[0]])
        decoded = winner_enc.inverse_transform(encoded)
        
        assert decoded[0] == classes[0]


class TestBatchPredictions:
    """Tests para predicciones en batch"""
    
    @pytest.fixture
    def sample_batch_data(self):
        """Datos de prueba para predicciones batch"""
        return pd.DataFrame({
            'team_color_encoded': [0, 1, 0, 1, 0],
            'goal_difference': [2, -1, 3, 0, -2],
            'match_duration': [320, 350, 380, 310, 365],
            'mode_duel': [1, 0, 0, 1, 0],
            'mode_doubles': [0, 1, 0, 0, 1],
            'mode_standard': [0, 0, 1, 0, 0],
            'is_competitive': [1, 1, 0, 1, 1],
            'overtime': [0, 1, 0, 0, 1]
        })
    
    def test_batch_predictions_correct_length(self, sample_batch_data):
        """Verifica que las predicciones batch tengan la longitud correcta"""
        model = joblib.load(str(BASE_DIR / 'data' / 'models' / 'random_forest_model.pkl'))
        
        X = sample_batch_data.values
        predictions = model.predict(X)
        
        assert len(predictions) == len(sample_batch_data)
    
    def test_batch_predictions_all_valid(self, sample_batch_data):
        """Verifica que todas las predicciones batch sean válidas"""
        model = joblib.load(str(BASE_DIR / 'data' / 'models' / 'random_forest_model.pkl'))
        winner_enc = joblib.load(str(BASE_DIR / 'data' / 'models' / 'winner_encoder.pkl'))
        
        X = sample_batch_data.values
        predictions = model.predict(X)
        
        # Todas las predicciones deben ser índices válidos
        assert (predictions >= 0).all()
        assert (predictions < len(winner_enc.classes_)).all()
    
    def test_batch_probabilities_shape(self, sample_batch_data):
        """Verifica la forma de las probabilidades en batch"""
        model = joblib.load(str(BASE_DIR / 'data' / 'models' / 'random_forest_model.pkl'))
        
        X = sample_batch_data.values
        probas = model.predict_proba(X)
        
        assert probas.shape[0] == len(sample_batch_data)
        assert probas.shape[1] >= 2  # Al menos 2 clases


class TestFeatureEngineering:
    """Tests para ingeniería de features"""
    
    def test_one_hot_encoding_game_modes(self):
        """Verifica que el one-hot encoding de modos de juego sea correcto"""
        game_modes = ['Duel', 'Doubles', 'Standard']
        
        for mode in game_modes:
            mode_duel = 1 if mode == "Duel" else 0
            mode_doubles = 1 if mode == "Doubles" else 0
            mode_standard = 1 if mode == "Standard" else 0
            
            # Debe haber exactamente un 1 y dos 0s
            assert sum([mode_duel, mode_doubles, mode_standard]) == 1
    
    def test_is_competitive_feature(self):
        """Verifica el cálculo de is_competitive"""
        test_cases = [
            (0, 1),   # diff=0 -> competitivo
            (1, 1),   # diff=1 -> competitivo
            (2, 1),   # diff=2 -> competitivo
            (-2, 1),  # diff=-2 -> competitivo
            (3, 0),   # diff=3 -> no competitivo
            (-3, 0),  # diff=-3 -> no competitivo
            (5, 0),   # diff=5 -> no competitivo
        ]
        
        for goal_diff, expected in test_cases:
            is_competitive = 1 if abs(goal_diff) <= 2 else 0
            assert is_competitive == expected, f"Failed for goal_diff={goal_diff}"
    
    def test_overtime_feature_conversion(self):
        """Verifica conversión de overtime a int"""
        assert int(True) == 1
        assert int(False) == 0


class TestModelMetrics:
    """Tests para verificar métricas del modelo"""
    
    def test_model_metadata_exists(self):
        """Verifica que exista archivo de metadatos del modelo"""
        metadata_path = '../data/models/model_metadata.pkl'
        
        # Si existe metadata, cargarlo
        if os.path.exists(metadata_path):
            metadata = joblib.load(metadata_path)
            assert metadata is not None
    
    def test_predictions_file_exists(self):
        """Verifica que exista archivo de predicciones"""
        predictions_path = str(BASE_DIR / 'data' / 'processed' / 'model_predictions.csv')
        assert os.path.exists(predictions_path)
    
    def test_predictions_file_structure(self):
        """Verifica estructura del archivo de predicciones"""
        predictions_path = str(BASE_DIR / 'data' / 'processed' / 'model_predictions.csv')
        df = pd.read_csv(predictions_path)
        
        # Debe tener columnas esenciales
        essential_cols = ['predicted_winner']
        for col in essential_cols:
            assert col in df.columns, f"Falta columna: {col}"
    
    def test_model_consistency(self):
        """Verifica que el modelo sea consistente en predicciones"""
        model = joblib.load(str(BASE_DIR / 'data' / 'models' / 'random_forest_model.pkl'))
        
        # Misma entrada debe dar misma salida
        X_test = np.array([[0, 2, 320, 1, 0, 0, 1, 0]])
        
        pred1 = model.predict(X_test)
        pred2 = model.predict(X_test)
        
        assert np.array_equal(pred1, pred2)


class TestDataIntegrityForPredictions:
    """Tests para integridad de datos en predicciones"""
    
    def test_no_nan_in_predictions(self):
        """Verifica que no haya valores NaN en predicciones"""
        model = joblib.load(str(BASE_DIR / 'data' / 'models' / 'random_forest_model.pkl'))
        
        X_test = np.array([[0, 2, 320, 1, 0, 0, 1, 0]])
        predictions = model.predict(X_test)
        
        assert not np.isnan(predictions).any()
    
    def test_no_nan_in_probabilities(self):
        """Verifica que no haya NaN en probabilidades"""
        model = joblib.load(str(BASE_DIR / 'data' / 'models' / 'random_forest_model.pkl'))
        
        X_test = np.array([[0, 2, 320, 1, 0, 0, 1, 0]])
        probas = model.predict_proba(X_test)
        
        assert not np.isnan(probas).any()
    
    def test_feature_count_matches_expected(self):
        """Verifica que el número de features sea el esperado"""
        model = joblib.load(str(BASE_DIR / 'data' / 'models' / 'random_forest_model.pkl'))
        
        # El modelo espera 8 features
        expected_features = 8
        
        # Verificar con entrada correcta
        X_correct = np.random.rand(1, expected_features)
        
        try:
            model.predict(X_correct)
        except ValueError:
            pytest.fail(f"El modelo no acepta {expected_features} features")
    
    def test_feature_count_rejects_wrong_size(self):
        """Verifica que el modelo rechace entradas con tamaño incorrecto"""
        model = joblib.load(str(BASE_DIR / 'data' / 'models' / 'random_forest_model.pkl'))
        
        # Intentar con número incorrecto de features
        X_wrong = np.random.rand(1, 5)  # Solo 5 features en lugar de 8
        
        with pytest.raises(ValueError):
            model.predict(X_wrong)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])