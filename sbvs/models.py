from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Tuple

Position = Tuple[float, float]


@dataclass
class Player:
    player_id: str
    name: str
    position: str
    team: str
    season_stats: Dict[str, float] = field(default_factory=dict)

    def record_stat(self, key: str, value: float) -> None:
        self.season_stats[key] = self.season_stats.get(key, 0.0) + value


@dataclass
class Team:
    name: str
    players: Dict[str, Player] = field(default_factory=dict)

    def add_player(self, player: Player) -> None:
        self.players[player.player_id] = player

    def remove_player(self, player_id: str) -> None:
        self.players.pop(player_id, None)


@dataclass
class FrameData:
    timestamp: datetime
    player_positions: Dict[str, Position]
    ball_position: Position
    speed: Dict[str, float]
    ball_speed: float
    events: List["GameEvent"] = field(default_factory=list)


@dataclass
class GameEvent:
    player_id: str
    event_type: str
    metadata: Dict[str, float]


@dataclass
class Scoreboard:
    home_team: str
    away_team: str
    home_score: int = 0
    away_score: int = 0

    def update_score(self, scoring_team: str, points: int) -> None:
        if scoring_team == self.home_team:
            self.home_score += points
        elif scoring_team == self.away_team:
            self.away_score += points

    def render(self) -> str:
        return f"{self.home_team} {self.home_score} - {self.away_score} {self.away_team}"
