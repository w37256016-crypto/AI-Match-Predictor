import os
import requests


class FootballAPI:
    def __init__(self):
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            "x-apisports-key": os.getenv("API_FOOTBALL_KEY")
        }

    def get_fixture(self, fixture_id):
        response = requests.get(
            f"{self.base_url}/fixtures?id={fixture_id}",
            headers=self.headers
        )
        return response.json()

    def search_fixture(self, home_team, away_team):
        response = requests.get(
            f"{self.base_url}/fixtures?team={home_team}",
            headers=self.headers
        )
        return response.json()

    def get_fixture_statistics(self, fixture_id):
        response = requests.get(
            f"{self.base_url}/fixtures/statistics?fixture={fixture_id}",
            headers=self.headers
        )
        return response.json()

    def get_team_statistics(self, league_id, season, team_id):
        response = requests.get(
            f"{self.base_url}/teams/statistics?league={league_id}&season={season}&team={team_id}",
            headers=self.headers
        )
        return response.json()

    def get_h2h(self, home_team, away_team):
        response = requests.get(
            f"{self.base_url}/fixtures/headtohead?h2h={home_team}-{away_team}",
            headers=self.headers
        )
        return response.json()

    def get_standings(self, league_id, season):
        response = requests.get(
            f"{self.base_url}/standings?league={league_id}&season={season}",
            headers=self.headers
        )
        return response.json()

    def get_injuries(self, team_id, season):
        response = requests.get(
            f"{self.base_url}/injuries?team={team_id}&season={season}",
            headers=self.headers
        )
        return response.json()

    def get_odds(self, fixture_id):
        response = requests.get(
            f"{self.base_url}/odds?fixture={fixture_id}",
            headers=self.headers
        )
        return response.json()
