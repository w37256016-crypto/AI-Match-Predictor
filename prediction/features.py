from api.football_api import FootballAPI


class MatchFeatures:

    def __init__(self):
        self.api = FootballAPI()

    def extract(
        self,
        league_id,
        season,
        fixture_id,
        home_team_id,
        away_team_id
    ):

        # Get home team statistics
        home = self.api.get_team_statistics(
            league_id,
            season,
            home_team_id
        )

        # Get away team statistics
        away = self.api.get_team_statistics(
            league_id,
            season,
            away_team_id
        )

        # Validate home response
        home_stats = self._extract_response(
            home,
            "Home"
        )

        # Validate away response
        away_stats = self._extract_response(
            away,
            "Away"
        )

        # Calculate basic features
        home_form = self._calculate_form(home_stats)
        away_form = self._calculate_form(away_stats)

        home_attack = self._calculate_attack(home_stats)
        away_attack = self._calculate_attack(away_stats)

        home_defense = self._calculate_defense(home_stats)
        away_defense = self._calculate_defense(away_stats)

        return {
            "home_form": home_form,
            "away_form": away_form,
            "home_attack": home_attack,
            "away_attack": away_attack,
            "home_defense": home_defense,
            "away_defense": away_defense,
            "home_advantage": 1.0,

            # Temporary defaults.
            # We will calculate these properly later.
            "h2h_score": 0.50,
            "momentum": 0.50,
            "league_strength": 0.50
        }

    def _extract_response(self, data, team_name):

        if not isinstance(data, dict):
            raise ValueError(
                f"{team_name} team statistics returned invalid data: {data}"
            )

        # API-Football normally puts the data here
        response = data.get("response")

        if not response:
            raise ValueError(
                f"{team_name} team statistics not found: {data}"
            )

        # Some API responses can contain a list
        if isinstance(response, list):

            if len(response) == 0:
                raise ValueError(
                    f"{team_name} team statistics returned an empty list: {data}"
                )

            response = response[0]

        if not isinstance(response, dict):
            raise ValueError(
                f"{team_name} team statistics have invalid format: {response}"
            )

        return response

    def _calculate_form(self, stats):

        form = stats.get("form", "")

        if not isinstance(form, str) or not form:
            return 0.50

        points = 0
        matches = 0

        for result in form.upper():

            if result == "W":
                points += 3
                matches += 1

            elif result == "D":
                points += 1
                matches += 1

            elif result == "L":
                matches += 1

        if matches == 0:
            return 0.50

        return round(
            min(points / (matches * 3), 1.0),
            2
        )

    def _calculate_attack(self, stats):

        goals = (
            stats
            .get("goals", {})
            .get("for", {})
            .get("total", {})
            .get("total", 0)
        )

        played = (
            stats
            .get("fixtures", {})
            .get("played", {})
            .get("total", 0)
        )

        try:
            goals = float(goals)
            played = float(played)
        except (TypeError, ValueError):
            return 0.50

        if played <= 0:
            return 0.50

        attack = goals / played / 3

        return round(
            max(0.0, min(attack, 1.0)),
            2
        )

    def _calculate_defense(self, stats):

        goals = (
            stats
            .get("goals", {})
            .get("against", {})
            .get("total", {})
            .get("total", 0)
        )

        played = (
            stats
            .get("fixtures", {})
            .get("played", {})
            .get("total", 0)
        )

        try:
            goals = float(goals)
            played = float(played)
        except (TypeError, ValueError):
            return 0.50

        if played <= 0:
            return 0.50

        defense = 1.0 - (goals / played / 3)

        return round(
            max(0.0, min(defense, 1.0)),
            2
        )
