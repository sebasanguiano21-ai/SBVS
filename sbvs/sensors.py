from __future__ import annotations

import math
import random
from datetime import datetime, timedelta
from typing import Dict, Generator, Iterable, List

from .models import FrameData, GameEvent, Position


class CameraSensor:
    """Simulated optical tracker that yields player and ball positions."""

    def __init__(self, frame_rate: int = 25) -> None:
        self.frame_rate = frame_rate

    def stream_frames(
        self, players: Iterable[str], duration_seconds: int = 10
    ) -> Generator[FrameData, None, None]:
        timestamp = datetime.utcnow()
        positions: Dict[str, Position] = {
            player_id: (random.uniform(0, 94), random.uniform(0, 50))
            for player_id in players
        }
        ball_position: Position = (47.0, 25.0)

        for _ in range(self.frame_rate * duration_seconds):
            timestamp += timedelta(milliseconds=int(1000 / self.frame_rate))
            new_positions: Dict[str, Position] = {}
            speed: Dict[str, float] = {}
            events: List[GameEvent] = []
            for player_id, (x, y) in positions.items():
                dx = random.uniform(-1.5, 1.5)
                dy = random.uniform(-1.0, 1.0)
                nx, ny = _clamp_position((x + dx, y + dy))
                new_positions[player_id] = (nx, ny)
                speed[player_id] = math.hypot(dx, dy) * self.frame_rate

                if random.random() < 0.01:
                    events.append(
                        GameEvent(
                            player_id=player_id,
                            event_type="shot",
                            metadata={"expected_points": random.choice([2, 3])},
                        )
                    )
            ball_dx = random.uniform(-2.0, 2.0)
            ball_dy = random.uniform(-1.5, 1.5)
            ball_position = _clamp_position((ball_position[0] + ball_dx, ball_position[1] + ball_dy))
            ball_speed = math.hypot(ball_dx, ball_dy) * self.frame_rate
            yield FrameData(
                timestamp=timestamp,
                player_positions=new_positions,
                ball_position=ball_position,
                speed=speed,
                ball_speed=ball_speed,
                events=events,
            )
            positions = new_positions


def _clamp_position(position: Position) -> Position:
    x, y = position
    return (max(0, min(94, x)), max(0, min(50, y)))
