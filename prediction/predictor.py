from .model import MatchPredictionModel


class MatchPredictor:
    def __init__(self):
        self.model = MatchPredictionModel()

    def predict(
        self,
        league_id,
        season,
        fixture_id,
        home_team_id,
        away_team_id
    ):
        result = self.model.predict(
            league_id,
            season,
            fixture_id,
            home_team_id,
            away_team_id
        )

        return {
            "fixture_id": fixture_id,
            "league_id": league_id,
            "season": season,
            "home_team_id": home_team_id,
            "away_team_id": away_team_id,
            "prediction": result,
            winner = max(
    ["home_win", "draw", "away_win"],
    key=lambda x: result[x]
)

return {
    "fixture_id": fixture_id,
    "league_id": league_id,
    "season": season,
    "home_team_id": home_team_id,
    "away_team_id": away_team_id,
    "prediction": result,
    "winner": winner
}
        }
