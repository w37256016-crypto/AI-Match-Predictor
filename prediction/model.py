from .features import MatchFeatures
from .scorer import MatchScorer
from .probability import ProbabilityEngine


class MatchPredictionModel:

    def __init__(self):
        self.features = MatchFeatures()
        self.scorer = MatchScorer()
        self.probability = ProbabilityEngine()

    ddef predict(
    self,
    league_id,
    season,
    fixture_id,
    home_team_id,
    away_team_id
):
    features = self.features.extract(
        league_id,
        season,
        fixture_id,
        home_team_id,
        away_team_id
    )

    strengths = self.scorer.calculate(features)

    probabilities = self.probability.calculate(
        strengths["home_strength"],
        strengths["away_strength"]
    )

    return probabilities
