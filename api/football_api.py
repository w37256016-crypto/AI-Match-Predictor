import os
import time
import requests


class FootballAPI:

    def __init__(self):
        self.base_url = "https://v3.football.api-sports.io"

        self.headers = {
            "x-apisports-key": os.getenv("API_FOOTBALL_KEY")
        }

        # Cache API results during the bot's runtime.
        # This prevents repeated requests for the same data.
        self.cache = {}

        # Small delay between API requests.
        self.request_delay = 1.0

    def _get(self, endpoint, params=None):

        if params is None:
            params = {}

        # Create a unique cache key
        cache_key = (
            endpoint,
            tuple(sorted(params.items()))
        )

        # Return cached result if available
        if cache_key in self.cache:
            return self.cache[cache_key]

        url = f"{self.base_url}/{endpoint}"

        # Try the request up to 3 times
        for attempt in range(3):

            try:

                # Small delay before requests
                if attempt > 0:
                    time.sleep(3)

                response = requests.get(
                    url,
                    headers=self.headers,
                    params=params,
                    timeout=30
                )

                # ------------------------------------------
                # Rate limit
                # ------------------------------------------

                if response.status_code == 429:

                    print(
                        f"API rate limit reached. "
                        f"Retry {attempt + 1}/3..."
                    )

                    if attempt < 2:
                        time.sleep(5)
                        continue

                    raise Exception(
                        "API-Football rate limit reached "
                        "after 3 attempts."
                    )

                # ------------------------------------------
                # Other HTTP errors
                # ------------------------------------------

                response.raise_for_status()

                data = response.json()

                # ------------------------------------------
                # API-Football plan errors
                # ------------------------------------------

                errors = data.get("errors", {})

                if errors:

                    # Convert errors to string so we can
                    # safely inspect the message.
                    error_text = str(errors)

                    # Current-season restriction
                    if (
                        "Free plans do not have access"
                        in error_text
                    ):
                        raise Exception(
                            f"API-Football error: {errors}"
                        )

                    # Other API errors
                    raise Exception(
                        f"API-Football error: {errors}"
                    )

                # Save successful result in cache
                self.cache[cache_key] = data

                # Small delay to avoid hammering API
                time.sleep(self.request_delay)

                return data

            except requests.exceptions.Timeout:

                if attempt == 2:
                    raise Exception(
                        "API-Football request timed out."
                    )

                time.sleep(3)

            except requests.exceptions.RequestException as e:

                if attempt == 2:
                    raise e

                time.sleep(3)

        raise Exception(
            "API-Football request failed."
        )

    # ==================================================
    # FIXTURE
    # ==================================================

    def get_fixture(self, fixture_id):

        return self._get(
            "fixtures",
            {
                "id": fixture_id
            }
        )

    # ==================================================
    # SEARCH FIXTURES
    # ==================================================

    def search_fixture(self, team_id):

        return self._get(
            "fixtures",
            {
                "team": team_id
            }
        )

    # ==================================================
    # FIXTURE STATISTICS
    # ==================================================

    def get_fixture_statistics(self, fixture_id):

        return self._get(
            "fixtures/statistics",
            {
                "fixture": fixture_id
            }
        )

    # ==================================================
    # TEAM STATISTICS
    # ==================================================

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

    # ==================================================
    # HEAD TO HEAD
    # ==================================================

    def get_h2h(
        self,
        home_team,
        away_team
    ):

        return self._get(
            "fixtures/headtohead",
            {
                "h2h": f"{home_team}-{away_team}"
            }
        )

    # ==================================================
    # STANDINGS
    # ==================================================

    def get_standings(
        self,
        league_id,
        season
    ):

        return self._get(
            "standings",
            {
                "league": league_id,
                "season": season
            }
        )

    # ==================================================
    # INJURIES
    # ==================================================

    def get_injuries(
        self,
        team_id,
        season
    ):

        return self._get(
            "injuries",
            {
                "team": team_id,
                "season": season
            }
        )

    # ==================================================
    # ODDS
    # ==================================================

    def get_odds(self, fixture_id):

        return self._get(
            "odds",
            {
                "fixture": fixture_id
            }
        )
