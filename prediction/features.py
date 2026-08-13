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

        # --------------------------------------------------
        # TEAM STATISTICS
        # --------------------------------------------------

        stats_season = season

        try:
            home = self.api.get_team_statistics(
                league_id,
                stats_season,
                home_team_id
            )

            away = self.api.get_team_statistics(
                league_id,
                stats_season,
                away_team_id
            )

        except Exception as current_error:

            error_text = str(current_error)

            # Free API plan may block the current season.
            # Fall back to 2024 statistics.
            if "Free plans do not have access" not in error_text:
                raise

            stats_season = 2024

            home = self.api.get_team_statistics(
                league_id,
                stats_season,
                home_team_id
            )

            away = self.api.get_team_statistics(
                league_id,
                stats_season,
                away_team_id
            )

        # --------------------------------------------------
        # VALIDATE API RESPONSES
        # --------------------------------------------------

        if "response" not in home or not home["response"]:
            raise ValueError(
                f"Home team statistics not found: {home}"
            )

        if "response" not in away or not away["response"]:
            raise ValueError(
                f"Away team statistics not found: {away}"
            )

        home_stats = home["response"]
        away_stats = away["response"]

        # API-Football can return a list.
        if isinstance(home_stats, list):
            if not home_stats:
                raise ValueError(
                    "Home statistics list is empty."
                )
            home_stats = home_stats[0]

        if isinstance(away_stats, list):
            if not away_stats:
                raise ValueError(
                    "Away statistics list is empty."
                )
            away_stats = away_stats[0]

        # --------------------------------------------------
        # BASIC FEATURES
        # --------------------------------------------------

        home_form = self._calculate_form(home_stats)
        away_form = self._calculate_form(away_stats)

        home_attack = self._calculate_attack(home_stats)
        away_attack = self._calculate_attack(away_stats)

        home_defense = self._calculate_defense(home_stats)
        away_defense = self._calculate_defense(away_stats)

        # --------------------------------------------------
        # H2H
        # --------------------------------------------------

        h2h_score = self._calculate_h2h(
            home_team_id,
            away_team_id
        )

        # --------------------------------------------------
        # MOMENTUM
        # --------------------------------------------------

        momentum = self._calculate_momentum(
            home_form,
            away_form
        )

        # --------------------------------------------------
        # LEAGUE STRENGTH
        # --------------------------------------------------

        # Neutral for now.
        # We will replace this later with a real calculation.
        league_strength = 0.5

        # --------------------------------------------------
        # RETURN FEATURES
        # --------------------------------------------------

        return {
            "home_form": home_form,
            "away_form": away_form,

            "home_attack": home_attack,
            "away_attack": away_attack,

            "home_defense": home_defense,
            "away_defense": away_defense,

            "home_advantage": 1.0,

            "h2h_score": h2h_score,

            "momentum": momentum,

            "league_strength": league_strength,

            "stats_season": stats_season
        }

    # ==================================================
    # FORM
    # ==================================================

    def _calculate_form(self, stats):

        form = stats.get("form", "")

        if not isinstance(form, str):
            return 0.5

        if not form:
            return 0.5

        points = 0

        for result in form:

            if result == "W":
                points += 3

            elif result == "D":
                points += 1

        maximum = len(form) * 3

        if maximum <= 0:
            return 0.5

        return round(
            points / maximum,
            3
        )

    # ==================================================
    # ATTACK
    # ==================================================

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
            return 0.5

        if played <= 0:
            return 0.5

        goals_per_game = goals / played

        value = min(
            goals_per_game / 3,
            1.0
        )

        return round(value, 3)

    # ==================================================
    # DEFENSE
    # ==================================================

    def _calculate_defense(self, stats):

        goals_against = (
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
            goals_against = float(goals_against)
            played = float(played)

        except (TypeError, ValueError):
            return 0.5

        if played <= 0:
            return 0.5

        goals_per_game = goals_against / played

        value = 1 - min(
            goals_per_game / 3,
            1.0
        )

        return round(
            max(value, 0.0),
            3
        )

    # ==================================================
    # HEAD TO HEAD
    # ==================================================

    def _calculate_h2h(
        self,
        home_team_id,
        away_team_id
    ):

        try:

            data = self.api.get_h2h(
                home_team_id,
                away_team_id
            )

            matches = data.get(
                "response",
                []
            )

            if not matches:
                return 0.5

            home_points = 0
            total_matches = 0

            for match in matches[:10]:

                teams = match.get(
                    "teams",
                    {}
                )

                match_home = teams.get(
                    "home",
                    {}
                )

                match_away = teams.get(
                    "away",
                    {}
                )

                home_id = match_home.get("id")
                away_id = match_away.get("id")

                home_winner = match_home.get("winner")
                away_winner = match_away.get("winner")

                if home_id is None or away_id is None:
                    continue

                total_matches += 1

                # Home team won
                if (
                    home_id == home_team_id
                    and home_winner is True
                ):
                    home_points += 3

                # Home team lost
                elif (
                    away_id == home_team_id
                    and away_winner is True
                ):
                    home_points += 0

                # Draw
                else:
                    home_points += 1

            if total_matches == 0:
                return 0.5

            return round(
                home_points / (total_matches * 3),
                3
            )

        except Exception:

            # H2H is optional.
            # If unavailable, remain neutral.
            return 0.5

    # ==================================================
    # MOMENTUM
    # ==================================================

    def _calculate_momentum(
        self,
        home_form,
        away_form
    ):

        difference = home_form - away_form

        momentum = (
            0.5 +
            difference / 2
        )

        return round(
            min(
                max(momentum, 0.0),
                1.0
            ),
            3
        )
