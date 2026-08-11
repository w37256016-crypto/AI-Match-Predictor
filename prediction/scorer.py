class MatchScorer:

    def __init__(self):
        pass

    def calculate(self, features):

        home_form = float(
            features.get("home_form", 0.5)
        )

        away_form = float(
            features.get("away_form", 0.5)
        )

        home_attack = float(
            features.get("home_attack", 0.5)
        )

        away_attack = float(
            features.get("away_attack", 0.5)
        )

        home_defense = float(
            features.get("home_defense", 0.5)
        )

        away_defense = float(
            features.get("away_defense", 0.5)
        )

        home_advantage = float(
            features.get("home_advantage", 1.0)
        )

        h2h = float(
            features.get("h2h_score", 0.5)
        )

        momentum = float(
            features.get("momentum", 0.5)
        )

        league_strength = float(
            features.get("league_strength", 0.5)
        )

        # Keep every feature between 0 and 1
        home_form = self._clamp(home_form)
        away_form = self._clamp(away_form)

        home_attack = self._clamp(home_attack)
        away_attack = self._clamp(away_attack)

        home_defense = self._clamp(home_defense)
        away_defense = self._clamp(away_defense)

        home_advantage = self._clamp(
            home_advantage
        )

        h2h = self._clamp(h2h)
        momentum = self._clamp(momentum)
        league_strength = self._clamp(
            league_strength
        )

        # ------------------------------------------
        # HOME TEAM
        # ------------------------------------------

        home_strength = (
            home_form * 0.25 +
            home_attack * 0.25 +
            home_defense * 0.20 +
            home_advantage * 0.10 +
            h2h * 0.08 +
            momentum * 0.07 +
            league_strength * 0.05
        )

        # ------------------------------------------
        # AWAY TEAM
        # ------------------------------------------

        away_strength = (
            away_form * 0.25 +
            away_attack * 0.25 +
            away_defense * 0.20 +
            (1 - home_advantage) * 0.10 +
            (1 - h2h) * 0.08 +
            (1 - momentum) * 0.07 +
            (1 - league_strength) * 0.05
        )

        return {
            "home_strength": round(
                home_strength,
                4
            ),
            "away_strength": round(
                away_strength,
                4
            )
        }

    def _clamp(self, value):

        return max(
            0.0,
            min(
                float(value),
                1.0
            )
        )
