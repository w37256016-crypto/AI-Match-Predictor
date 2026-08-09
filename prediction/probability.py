class ProbabilityEngine:

    def __init__(self):
        pass

    def calculate(self, home_strength, away_strength):

        # Make sure the strengths are numbers
        try:
            home_strength = float(home_strength)
        except (TypeError, ValueError):
            home_strength = 0.5

        try:
            away_strength = float(away_strength)
        except (TypeError, ValueError):
            away_strength = 0.5

        # Prevent negative values
        home_strength = max(0.0, home_strength)
        away_strength = max(0.0, away_strength)

        total = home_strength + away_strength

        # If no useful data is available
        if total == 0:
            return {
                "home_win": 33.3,
                "draw": 33.4,
                "away_win": 33.3,
                "confidence": 0.0,
                "risk": "High"
            }

        # Convert team strengths into ratios
        home_ratio = home_strength / total
        away_ratio = away_strength / total

        # Difference between the teams
        strength_diff = abs(home_ratio - away_ratio)

        # Estimate draw probability
        if strength_diff < 0.05:
            draw = 35.0
        elif strength_diff < 0.10:
            draw = 30.0
        elif strength_diff < 0.20:
            draw = 25.0
        else:
            draw = 15.0

        # Remaining probability is divided between
        # home win and away win
        scale = 100.0 - draw

        home_win = home_ratio * scale
        away_win = away_ratio * scale

        # Highest outcome probability becomes confidence
        confidence = round(
            max(home_win, away_win),
            2
        )

        # Risk classification
        if confidence >= 75:
            risk = "Low"
        elif confidence >= 60:
            risk = "Medium"
        else:
            risk = "High"

        return {
            "home_win": round(home_win, 2),
            "draw": round(draw, 2),
            "away_win": round(away_win, 2),
            "confidence": confidence,
            "risk": risk
        }
