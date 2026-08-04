from api.football_api import FootballAPI


class MatchFeatures:
    def __init__(self):
        self.api = FootballAPI()

    def extract(self, league_id, season, fixture_id, home_team_id, away_team_id):

        home = self.api.get_team_statistics(
            league_id,
            season,
            home_team_id
        )

        away = self.api.get_team_statistics(
            league_id,
            season,
            away_team_id
        )

        home_stats = home["response"]
        away_stats = away["response"]

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
            "home_advantage": 1.0
        }

    def _calculate_form(self, stats):
        form = stats.get("form", "")

        if not form:
            return 0.5

        points = 0

        for result in form:
            if result == "W":
                points += 3
            elif result == "D":
                points += 1

        return round(points / (len(form) * 3), 2)

    def _calculate_attack(self, stats):
        goals = stats["goals"]["for"]["total"]["total"]
        played = stats["fixtures"]["played"]["total"]

        if played == 0:
            return 0.5

        return round(min(goals / played / 3, 1), 2)

    def _calculate_defense(self, stats):
        goals = stats["goals"]["against"]["total"]["total"]
        played = stats["fixtures"]["played"]["total"]

        if played == 0:
            return 0.5

        value = 1 - min(goals / played / 3, 1)

        return round(value, 2)
