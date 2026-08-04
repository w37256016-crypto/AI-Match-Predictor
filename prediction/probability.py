class ProbabilityEngine:
    def __init__(self):
        pass

    def calculate(self, home_strength, away_strength):
        total = home_strength + away_strength

        if total == 0:
            return {
                "home_win": 33.3,
                "draw": 33.4,
                "away_win": 33.3
            }

        home_win = (home_strength / total) * 100
        away_win = (away_strength / total) * 100

        strength_diff = abs(home_strength - away_strength)

        if strength_diff < 0.10:
            draw = 30
        elif strength_diff < 0.25:
            draw = 25
        else:
            draw = 15

        scale = 100 - draw
        total_wins = home_win + away_win

        home_win = (home_win / total_wins) * scale
        away_win = (away_win / total_wins) * scale

        return {
            "home_win": round(home_win, 2),
            "draw": round(draw, 2),
            "away_win": round(away_win, 2)
        }
