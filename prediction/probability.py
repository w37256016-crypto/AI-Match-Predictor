class ProbabilityEngine:
    def __init__(self):
        pass

    def calculate(self, home_strength, away_strength):

        total = home_strength + away_strength

        if total == 0:
            return {
                "home_win": 33.3,
                "draw": 33.4,
                "away_win": 33.3,
                "confidence": 0,
                "risk": "High"
            }

        home_ratio = home_strength / total
        away_ratio = away_strength / total

        strength_diff = abs(home_ratio - away_ratio)

        if strength_diff < 0.05:
            draw = 35
        elif strength_diff < 0.10:
            draw = 30
        elif strength_diff < 0.20:
            draw = 25
        else:
            draw = 15

        scale = 100 - draw

        home_win = home_ratio * scale
        away_win = away_ratio * scale

        confidence = round(max(home_win, away_win), 2)

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
