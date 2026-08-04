from api.football_api import FootballAPI


class MatchFeatures:
    def __init__(self):
        self.api = FootballAPI()

    def extract(self, league_id, season, fixture_id, home_team_id, away_team_id):
        home_stats = self.api.get_team_statistics(
            league_id, season, home_team_id
        )

        away_stats = self.api.get_team_statistics(
            league_id, season, away_team_id
        )

        h2h = self.api.get_h2h(
            home_team_id,
            away_team_id
        )

        fixture_stats = self.api.get_fixture_statistics(
            fixture_id
        )

        return {
            "home_stats": home_stats,
            "away_stats": away_stats,
            "h2h": h2h,
            "fixture_stats": fixture_stats
        }
