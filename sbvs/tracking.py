from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List

from .models import FrameData, GameEvent, Player, Scoreboard
from .stats import StatBook


@dataclass
class TrackingEngine:
    roster: Dict[str, Player]
    scoreboard: Scoreboard
    stat_book: StatBook = field(default_factory=StatBook)
    movement_log: List[FrameData] = field(default_factory=list)
    ball_path: List[tuple] = field(default_factory=list)

    def process_frame(self, frame: FrameData) -> None:
        self.movement_log.append(frame)
        self.ball_path.append(frame.ball_position)
        for event in frame.events:
            self._handle_event(event)

    def _handle_event(self, event: GameEvent) -> None:
        player = self.roster.get(event.player_id)
        if not player:
            return

        if event.event_type == "shot":
            expected_points = int(event.metadata.get("expected_points", 0))
            made = expected_points > 0
            if made:
                self.scoreboard.update_score(player.team, expected_points)
                self.stat_book.record_stat(player, "points", expected_points)
            self.stat_book.record_stat(player, "shots", 1)

    def summary(self) -> str:
        lines = [f"Movement frames: {len(self.movement_log)}"]
        last_ball_position = self.ball_path[-1] if self.ball_path else "N/A"
        lines.append(f"Last ball position: {last_ball_position}")
        lines.append(f"Scoreboard: {self.scoreboard.render()}")
        return "\n".join(lines)


@dataclass
class RosterManager:
    teams: Dict[str, List[Player]] = field(default_factory=dict)

    def register_team(self, team_name: str, players: Iterable[Player]) -> None:
        self.teams[team_name] = list(players)

    def register_player(self, team_name: str, player: Player) -> None:
        self.teams.setdefault(team_name, []).append(player)

    def roster_lookup(self) -> Dict[str, Player]:
        return {player.player_id: player for roster in self.teams.values() for player in roster}
