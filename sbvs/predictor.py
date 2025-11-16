from __future__ import annotations

from typing import Dict

from .models import Player


class PerformancePredictor:
    """Simple predictor using weighted averages of historical stats."""

    def __init__(self, lookback_games: int = 5) -> None:
        self.lookback_games = lookback_games

    def predict_next_game(self, player: Player) -> Dict[str, float]:
        points = player.season_stats.get("points", 0.0)
        games = max(player.season_stats.get("games", 1), 1)
        average_points = points / games
        trend = player.season_stats.get("recent_points", average_points)

        predicted_points = 0.7 * average_points + 0.3 * trend
        predicted_reb = player.season_stats.get("rebounds", 0.0) / games
        predicted_ast = player.season_stats.get("assists", 0.0) / games

        return {
            "predicted_points": round(predicted_points, 2),
            "predicted_rebounds": round(predicted_reb, 2),
            "predicted_assists": round(predicted_ast, 2),
        }
