class MatchFeatures:
    def __init__(self):
        pass

    def extract(self, match_data):
        return {
            "home_form": match_data.get("home_form", 0),
            "away_form": match_data.get("away_form", 0),
            "home_attack": match_data.get("home_attack", 0),
            "away_attack": match_data.get("away_attack", 0),
            "home_defense": match_data.get("home_defense", 0),
            "away_defense": match_data.get("away_defense", 0),
            "home_advantage": match_data.get("home_advantage", 1),
        }
