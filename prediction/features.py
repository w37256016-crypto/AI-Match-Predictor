from api.football_api import FootballAPI


class MatchFeatures:
    def __init__(self):
        self.api = FootballAPI()

    def extract(self, league_id, season, fixture_id, home_team_id, away_team_id):

        # Temporary values until the real AI feature extractor is built.
        # This prevents KeyError and lets the bot run.

        return {
            "home_form": 0.75,
            "home_attack": 0.80,
            "home_defense": 0.70,
            "home_advantage": 1.00,

            "away_form": 0.65,
            "away_attack": 0.68,
            "away_defense": 0.66
        }
