import os
import requests


class FootballAPI:

    def __init__(self):
        self.base_url = "https://v3.football.api-sports.io"

        api_key = os.getenv("API_FOOTBALL_KEY")

        if not api_key:
            raise ValueError("Missing API_FOOTBALL_KEY")

        self.headers = {
            "x-apisports-key": api_key
        }

    def _get(self, endpoint, params=None):

        response = requests.get(
            f"{self.base_url}/{endpoint}",
            headers=self.headers,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        errors = data.get("errors")

        if errors:
            raise ValueError(
                f"API-Football error: {errors}"
            )

        return data

    # -------------------------------
    # FIXTURES
    # -------------------------------

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

    def get_fixtures_by_date(self, date):
        return self._get(
            "fixtures",
            {"date": date}
        )

    def get_fixtures_by_league(self, league_id, season):
        return self._get(
            "fixtures",
            {
                "league": league_id,
                "season": season
            }
        )

    def get_upcoming_fixtures(
        self,
        league_id,
        season,
        next_matches=20
    ):
        return self._get(
            "fixtures",
            {
                "league": league_id,
                "season": season,
                "next": next_matches
            }
        )

    # -------------------------------
    # API-FOOTBALL PREDICTION
    # -------------------------------

    def get_prediction(self, fixture_id):
        return self._get(
            "predictions",
            {
                "fixture": fixture_id
            }
        )

    # -------------------------------
    # TEAM STATISTICS
    # -------------------------------

    def get_team_statistics(
        self,
        league_id,
        season,
        team_id
    ):
        return self._get(
            "teams/statistics",
            {
                "league": league_id,
                "season": season,
                "team": team_id
            }
        )

    # -------------------------------
    # FIXTURE STATISTICS
    # -------------------------------

    def get_fixture_statistics(self, fixture_id):
        return self._get(
            "fixtures/statistics",
            {"fixture": fixture_id}
        )

    # -------------------------------
    # HEAD TO HEAD
    # -------------------------------

    def get_h2h(self, home_team, away_team):
        return self._get(
            "fixtures/headtohead",
            {
                "h2h": f"{home_team}-{away_team}"
            }
        )

    # -------------------------------
    # STANDINGS
    # -------------------------------

    def get_standings(self, league_id, season):
        return self._get(
            "standings",
            {
                "league": league_id,
                "season": season
            }
        )

    # -------------------------------
    # INJURIES
    # -------------------------------

    def get_injuries(self, team_id, season):
        return self._get(
            "injuries",
            {
                "team": team_id,
                "season": season
            }
        )

    # -------------------------------
    # ODDS
    # -------------------------------

    def get_odds(self, fixture_id):
        return self._get(
            "odds",
            {
                "fixture": fixture_id
            }
        )

    # -------------------------------
    # LEAGUES
    # -------------------------------

    def get_leagues(self):
        return self._get("leagues")

    # -------------------------------
    # AVAILABLE SEASONS
    # -------------------------------

    def get_available_seasons(self, league_id):

        data = self._get(
            "leagues",
            {"id": league_id}
        )

        seasons = []

        for league in data.get("response", []):

            for season in league.get("seasons", []):

                year = season.get("year")

                if year is not None:
                    seasons.append(year)

        return sorted(
            set(seasons),
            reverse=True
        )

    def get_latest_available_season(self, league_id):

        seasons = self.get_available_seasons(
            league_id
        )

        if not seasons:
            raise ValueError(
                f"No seasons found for league {league_id}"
            )

        return seasons[0]
