import os
import requests


class FootballAPI:
    def __init__(self):
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            "x-apisports-key": os.getenv("API_FOOTBALL_KEY")
        }

    def _get(self, endpoint, params=None):
        response = requests.get(
            f"{self.base_url}/{endpoint}",
            headers=self.headers,
            params=params,
            timeout=30
        )

        response.raise_for_status()
        return response.json()

    def get_fixture(self, fixture_id):
        return self._get(
            "fixtures",
            {"id": fixture_id}
        )

    def search_fixture(self, team_id):
        return self._get(
            "fixtures",
            {"team": team_id}
        )

    def get_fixture_statistics(self, fixture_id):
        return self._get(
            "fixtures/statistics",
            {"fixture": fixture_id}
        )

    def get_team_statistics(self, league_id, season, team_id):
        return self._get(
            "teams/statistics",
            {
                "league": league_id,
                "season": season,
                "team": team_id
            }
        )

    def get_h2h(self, home_team, away_team):
        return self._get(
            "fixtures/headtohead",
            {
                "h2h": f"{home_team}-{away_team}"
            }
        )

    def get_standings(self, league_id, season):
        return self._get(
            "standings",
            {
                "league": league_id,
                "season": season
            }
        )

    def get_injuries(self, team_id, season):
        return self._get(
            "injuries",
            {
                "team": team_id,
                "season": season
            }
        )

    def get_odds(self, fixture_id):
        return self._get(
            "odds",
            {
                "fixture": fixture_id
            }
                )
