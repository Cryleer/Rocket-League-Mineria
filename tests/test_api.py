"""
Tests unitarios para la API de predicción
Cubre endpoints, validaciones y manejo de errores
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Ajustar el path para encontrar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

# Importar después de ajustar el path
from main import app, normalize_team_color, normalize_winner, MatchInput


client = TestClient(app)


class TestNormalizationFunctions:
    """Tests para las funciones de normalización"""
    
    def test_normalize_team_color_blue_lowercase(self):
        """Verifica normalización de 'blue' a 'Blue'"""
        assert normalize_team_color('blue') == 'Blue'
    
    def test_normalize_team_color_blue_uppercase(self):
        """Verifica que 'Blue' se mantenga"""
        assert normalize_team_color('Blue') == 'Blue'
    
    def test_normalize_team_color_orange_lowercase(self):
        """Verifica normalización de 'orange' a 'Orange'"""
        assert normalize_team_color('orange') == 'Orange'
    
    def test_normalize_team_color_orange_uppercase(self):
        """Verifica que 'Orange' se mantenga"""
        assert normalize_team_color('Orange') == 'Orange'
    
    def test_normalize_team_color_spanish(self):
        """Verifica normalización de términos en español"""
        assert normalize_team_color('azul') == 'Blue'
        assert normalize_team_color('naranja') == 'Orange'
    
    def test_normalize_winner_blue_variants(self):
        """Verifica normalización de variantes de blue para winner"""
        assert normalize_winner('blue') == 'Blue'
        assert normalize_winner('Blue') == 'Blue'
        assert normalize_winner('azul') == 'Blue'
    
    def test_normalize_winner_orange_variants(self):
        """Verifica normalización de variantes de orange para winner"""
        assert normalize_winner('orange') == 'Orange'
        assert normalize_winner('Orange') == 'Orange'
        assert normalize_winner('naranja') == 'Orange'
    
    def test_normalize_winner_draw_variants(self):
        """Verifica normalización de variantes de empate"""
        assert normalize_winner('draw') == 'Draw'
        assert normalize_winner('Draw') == 'Draw'
        assert normalize_winner('tie') == 'Draw'
        assert normalize_winner('empate') == 'Draw'


class TestRootEndpoint:
    """Tests para el endpoint raíz"""
    
    def test_root_returns_200(self):
        """Verifica que el endpoint raíz retorne 200"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_returns_json(self):
        """Verifica que retorne JSON válido"""
        response = client.get("/")
        assert response.headers['content-type'] == 'application/json'
        data = response.json()
        assert isinstance(data, dict)
    
    def test_root_contains_message(self):
        """Verifica que contenga mensaje de bienvenida"""
        response = client.get("/")
        data = response.json()
        assert 'message' in data
        assert 'status' in data
    
    def test_root_contains_endpoints_info(self):
        """Verifica que contenga información de endpoints"""
        response = client.get("/")
        data = response.json()
        assert 'endpoints' in data
        assert isinstance(data['endpoints'], dict)
    
    def test_root_contains_encoder_info(self):
        """Verifica que contenga información de encoders"""
        response = client.get("/")
        data = response.json()
        assert 'encoders' in data
        assert 'team_color_classes' in data['encoders']
        assert 'winner_classes' in data['encoders']


class TestPredictEndpoint:
    """Tests para el endpoint de predicción"""
    
    @pytest.fixture
    def valid_match_data(self):
        """Datos válidos para predicción"""
        return {
            "team_color": "Blue",
            "game_mode": "Duel",
            "goal_difference": 2,
            "match_duration": 320,
            "overtime": False
        }
    
    def test_predict_with_valid_data(self, valid_match_data):
        """Verifica predicción con datos válidos"""
        response = client.post("/predict", json=valid_match_data)
        assert response.status_code == 200
    
    def test_predict_returns_winner(self, valid_match_data):
        """Verifica que retorne predicción de ganador"""
        response = client.post("/predict", json=valid_match_data)
        data = response.json()
        
        assert 'winner_prediction' in data
        assert data['winner_prediction'] in ['Blue', 'Orange', 'Draw']
    
    def test_predict_returns_confidence(self, valid_match_data):
        """Verifica que retorne confianza de la predicción"""
        response = client.post("/predict", json=valid_match_data)
        data = response.json()
        
        assert 'confidence' in data
        assert 0 <= data['confidence'] <= 1
    
    def test_predict_returns_probabilities(self, valid_match_data):
        """Verifica que retorne probabilidades para cada clase"""
        response = client.post("/predict", json=valid_match_data)
        data = response.json()
        
        assert 'probabilities' in data
        probs = data['probabilities']
        assert 'Blue' in probs
        assert 'Orange' in probs
        assert 'Draw' in probs
        
        # Las probabilidades deben sumar aproximadamente 1
        total = probs['Blue'] + probs['Orange'] + probs['Draw']
        assert 0.99 <= total <= 1.01
    
    def test_predict_with_lowercase_team_color(self):
        """Verifica predicción con color en minúsculas"""
        data = {
            "team_color": "blue",  # Minúscula
            "game_mode": "Doubles",
            "goal_difference": 1,
            "match_duration": 350,
            "overtime": True
        }
        response = client.post("/predict", json=data)
        assert response.status_code == 200
    
    def test_predict_with_spanish_team_color(self):
        """Verifica predicción con colores en español"""
        data = {
            "team_color": "azul",
            "game_mode": "Standard",
            "goal_difference": 3,
            "match_duration": 380,
            "overtime": False
        }
        response = client.post("/predict", json=data)
        assert response.status_code == 200
    
    def test_predict_with_different_game_modes(self):
        """Verifica predicción con diferentes modos de juego"""
        modes = ["Duel", "Doubles", "Standard"]
        
        for mode in modes:
            data = {
                "team_color": "Blue",
                "game_mode": mode,
                "goal_difference": 2,
                "match_duration": 320,
                "overtime": False
            }
            response = client.post("/predict", json=data)
            assert response.status_code == 200
    
    def test_predict_with_negative_goal_difference(self):
        """Verifica predicción con diferencia de goles negativa"""
        data = {
            "team_color": "Orange",
            "game_mode": "Duel",
            "goal_difference": -3,
            "match_duration": 310,
            "overtime": False
        }
        response = client.post("/predict", json=data)
        assert response.status_code == 200
    
    def test_predict_with_overtime(self):
        """Verifica predicción con tiempo extra"""
        data = {
            "team_color": "Blue",
            "game_mode": "Doubles",
            "goal_difference": 1,
            "match_duration": 420,
            "overtime": True
        }
        response = client.post("/predict", json=data)
        assert response.status_code == 200
    
    def test_predict_missing_field(self):
        """Verifica error cuando falta un campo requerido"""
        data = {
            "team_color": "Blue",
            "game_mode": "Duel",
            # Falta goal_difference
            "match_duration": 320,
            "overtime": False
        }
        response = client.post("/predict", json=data)
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_predict_invalid_type(self):
        """Verifica error con tipo de dato incorrecto"""
        data = {
            "team_color": "Blue",
            "game_mode": "Duel",
            "goal_difference": "dos",  # Debería ser int
            "match_duration": 320,
            "overtime": False
        }
        response = client.post("/predict", json=data)
        assert response.status_code == 422


class TestStatsEndpoint:
    """Tests para el endpoint de estadísticas"""
    
    def test_stats_returns_200(self):
        """Verifica que el endpoint de stats retorne 200"""
        response = client.get("/stats")
        assert response.status_code == 200
    
    def test_stats_returns_total_matches(self):
        """Verifica que retorne el total de partidas"""
        response = client.get("/stats")
        data = response.json()
        
        assert 'total_matches' in data
        assert isinstance(data['total_matches'], int)
        assert data['total_matches'] > 0
    
    def test_stats_returns_game_mode_distribution(self):
        """Verifica que retorne distribución de modos de juego"""
        response = client.get("/stats")
        data = response.json()
        
        assert 'game_modes' in data
        assert isinstance(data['game_modes'], dict)
    
    def test_stats_returns_winner_distribution(self):
        """Verifica que retorne distribución de ganadores"""
        response = client.get("/stats")
        data = response.json()
        
        assert 'predicted_winner_distribution' in data
        assert isinstance(data['predicted_winner_distribution'], dict)
    
    def test_stats_returns_avg_duration(self):
        """Verifica que retorne duración promedio"""
        response = client.get("/stats")
        data = response.json()
        
        assert 'avg_match_duration' in data
        assert isinstance(data['avg_match_duration'], (int, float))
        assert data['avg_match_duration'] > 0
    
    def test_stats_returns_overtime_percentage(self):
        """Verifica que retorne porcentaje de tiempo extra"""
        response = client.get("/stats")
        data = response.json()
        
        assert 'overtime_percentage' in data
        assert 0 <= data['overtime_percentage'] <= 100
    
    def test_stats_returns_goal_difference_stats(self):
        """Verifica que retorne estadísticas de diferencia de goles"""
        response = client.get("/stats")
        data = response.json()
        
        assert 'goal_difference_stats' in data
        stats = data['goal_difference_stats']
        assert 'mean' in stats
        assert 'std' in stats
        assert 'min' in stats
        assert 'max' in stats


class TestAPIValidation:
    """Tests para validación de datos de entrada"""
    
    def test_match_input_validation_correct_types(self):
        """Verifica validación de tipos de datos"""
        # Datos válidos
        match = MatchInput(
            team_color="Blue",
            game_mode="Duel",
            goal_difference=2,
            match_duration=320,
            overtime=False
        )
        assert match.team_color == "Blue"
        assert match.goal_difference == 2
    
    def test_match_input_string_fields(self):
        """Verifica que team_color y game_mode sean strings"""
        match = MatchInput(
            team_color="Blue",
            game_mode="Duel",
            goal_difference=0,
            match_duration=300,
            overtime=False
        )
        assert isinstance(match.team_color, str)
        assert isinstance(match.game_mode, str)
    
    def test_match_input_integer_fields(self):
        """Verifica que goal_difference y match_duration sean enteros"""
        match = MatchInput(
            team_color="Blue",
            game_mode="Duel",
            goal_difference=3,
            match_duration=350,
            overtime=True
        )
        assert isinstance(match.goal_difference, int)
        assert isinstance(match.match_duration, int)
    
    def test_match_input_boolean_field(self):
        """Verifica que overtime sea booleano"""
        match = MatchInput(
            team_color="Orange",
            game_mode="Doubles",
            goal_difference=-2,
            match_duration=400,
            overtime=True
        )
        assert isinstance(match.overtime, bool)


class TestAPIErrorHandling:
    """Tests para manejo de errores de la API"""
    
    def test_api_returns_json_error_messages(self):
        """Verifica que los errores retornen mensajes en JSON"""
        data = {
            "team_color": "Blue",
            "game_mode": "Duel",
            # Campos faltantes
        }
        response = client.post("/predict", json=data)
        assert response.headers['content-type'] == 'application/json'
        error_data = response.json()
        assert 'detail' in error_data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])