class MatchScorer:
    def __init__(self):
        pass

    def calculate(self, features):

        home_form = features["home_form"]
        away_form = features["away_form"]

        home_attack = features["home_attack"]
        away_attack = features["away_attack"]

        home_defense = features["home_defense"]
        away_defense = features["away_defense"]

        home_advantage = features.get("home_advantage", 1.0)

        h2h = features.get("h2h_score", 0.50)
        momentum = features.get("momentum", 0.50)
        league_strength = features.get("league_strength", 0.50)

        home_strength = (
            home_form * 0.25 +
            home_attack * 0.25 +
            home_defense * 0.20 +
            home_advantage * 0.15 +
            h2h * 0.05 +
            momentum * 0.05 +
            league_strength * 0.05
        )

        away_strength = (
            away_form * 0.30 +
            away_attack * 0.30 +
            away_defense * 0.25 +
            (1 - h2h) * 0.05 +
            (1 - momentum) * 0.05 +
            (1 - league_strength) * 0.05
        )

        return {
            "home_strength": round(home_strength, 3),
            "away_strength": round(away_strength, 3)
    }
