import os
import requests


class FootballAPI:
    def __init__(self):
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            "x-apisports-key": os.getenv("API_FOOTBALL_KEY")
        }

    def get_fixture(self, fixture_id):
        url = f"{self.base_url}/fixtures?id={fixture_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def search_fixture(self, home_team, away_team):
        url = (
            f"{self.base_url}/fixtures?"
            f"team={home_team}"
        )
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_fixture_statistics(self, fixture_id):
        url = f"{self.base_url}/fixtures/statistics?fixture={fixture_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_team_statistics(self, league_id, season, team_id):
        url = (
            f"{self.base_url}/teams/statistics"
            f"?league={league_id}"
            f"&season={season}"
            f"&team={team_id}"
        )
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_standings(self, league_id, season):
        url = (
            f"{self.base_url}/standings"
            f"?league={league_id}"
            f"&season={season}"
        )
        response = requests.get(url, headers=self.headers)
        return response.json()
