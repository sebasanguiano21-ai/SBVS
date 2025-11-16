from __future__ import annotations

from collections import defaultdict
from typing import Dict

from .models import Player


class StatBook:
    def __init__(self) -> None:
        self._game_stats: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))

    def record_stat(self, player: Player, key: str, value: float) -> None:
        self._game_stats[player.player_id][key] += value
        player.record_stat(key, value)

    def get_game_stats(self, player_id: str) -> Dict[str, float]:
        return dict(self._game_stats.get(player_id, {}))


class PlayerDashboard:
    def __init__(self, player: Player, stat_book: StatBook) -> None:
        self.player = player
        self.stat_book = stat_book

    def as_dict(self) -> Dict[str, float]:
        game_stats = self.stat_book.get_game_stats(self.player.player_id)
        combined = {**self.player.season_stats}
        for key, value in game_stats.items():
            combined[f"game_{key}"] = value
        return combined

    def formatted(self) -> str:
        stats = self.as_dict()
        lines = [f"Dashboard for {self.player.name} ({self.player.team})"]
        lines += [f"- {k}: {v}" for k, v in sorted(stats.items())]
        return "\n".join(lines)
