class MatchScorer:

    def __init__(self):
        pass

    def calculate(self, features):

        # Get the main features
        home_form = self._safe_number(
            features.get("home_form", 0.5)
        )

        away_form = self._safe_number(
            features.get("away_form", 0.5)
        )

        home_attack = self._safe_number(
            features.get("home_attack", 0.5)
        )

        away_attack = self._safe_number(
            features.get("away_attack", 0.5)
        )

        home_defense = self._safe_number(
            features.get("home_defense", 0.5)
        )

        away_defense = self._safe_number(
            features.get("away_defense", 0.5)
        )

        home_advantage = self._safe_number(
            features.get("home_advantage", 1.0)
        )

        # Optional advanced features
        h2h = self._safe_number(
            features.get("h2h_score", 0.50)
        )

        momentum = self._safe_number(
            features.get("momentum", 0.50)
        )

        league_strength = self._safe_number(
            features.get("league_strength", 0.50)
        )

        # Keep all values between 0 and 1
        home_form = self._clamp(home_form)
        away_form = self._clamp(away_form)

        home_attack = self._clamp(home_attack)
        away_attack = self._clamp(away_attack)

        home_defense = self._clamp(home_defense)
        away_defense = self._clamp(away_defense)

        home_advantage = self._clamp(home_advantage)

        h2h = self._clamp(h2h)
        momentum = self._clamp(momentum)
        league_strength = self._clamp(league_strength)

        # Calculate home team strength
        home_strength = (
            home_form * 0.25 +
            home_attack * 0.25 +
            home_defense * 0.20 +
            home_advantage * 0.15 +
            h2h * 0.05 +
            momentum * 0.05 +
            league_strength * 0.05
        )

        # Calculate away team strength
        away_strength = (
            away_form * 0.30 +
            away_attack * 0.30 +
            away_defense * 0.25 +
            (1 - h2h) * 0.05 +
            (1 - momentum) * 0.05 +
            (1 - league_strength) * 0.05
        )

        return {
            "home_strength": round(home_strength, 3),
            "away_strength": round(away_strength, 3)
        }

    def _safe_number(self, value):
        """
        Convert values to numbers safely.
        Prevents errors when API data contains strings,
        None, or unexpected values.
        """

        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.5

    def _clamp(self, value):
        """
        Keep a value between 0 and 1.
        """

        return max(0.0, min(1.0, value))
