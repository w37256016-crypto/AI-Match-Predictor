class PredictionEngine:
    def __init__(self):
        self.name = "AI Match Predictor"

    def predict(self, home_team, away_team):
        return {
            "home_team": home_team,
            "away_team": away_team,
            "prediction": "Home Win",
            "confidence": 75
        }
