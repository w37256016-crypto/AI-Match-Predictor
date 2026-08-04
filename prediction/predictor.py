from .model import MatchPredictionModel


class MatchPredictor:

    def __init__(self):
        self.model = MatchPredictionModel()

    def predict(self, match_data):
        return self.model.predict(match_data)
