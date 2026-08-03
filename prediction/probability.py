class ProbabilityEngine:

    def calculate(self, home_strength, away_strength):
        total = home_strength + away_strength

        if total == 0:
            return {
                "home": 33.3,
                "draw": 33.4,
                "away": 33.3
            }

        home = (home_strength / total) * 100
        away = (away_strength / total) * 100
        draw = max(0, 100 - home - away)

        return {
            "home": round(home, 2),
            "draw": round(draw, 2),
            "away": round(away, 2)
        }
