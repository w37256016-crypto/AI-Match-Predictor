from .features import MatchFeatures
from .scorer import MatchScorer
from .probability import ProbabilityEngine


class MatchPredictionModel:

    def __init__(self):
        self.features = MatchFeatures()
        self.scorer = MatchScorer()
        self.probability = ProbabilityEngine()

    def predict(self, match_data):
        features = self.features.extract(match_data)

        strengths = self.scorer.calculate_strength(features)

        probabilities = self.probability.calculate(
            strengths["home_strength"],
            strengths["away_strength"]
        )

        return probabilities
