class MatchScorer:
    def __init__(self):
        pass

    def calculate_strength(self, features):
        home_strength = (
            features["home_form"] * 0.30 +
            features["home_attack"] * 0.30 +
            features["home_defense"] * 0.20 +
            features["home_advantage"] * 0.20
        )

        away_strength = (
            features["away_form"] * 0.35 +
            features["away_attack"] * 0.35 +
            features["away_defense"] * 0.30
        )

        return {
            "home_strength": round(home_strength, 2),
            "away_strength": round(away_strength, 2)
      }
