from __future__ import annotations

from typing import List

from .models import Player, Scoreboard
from .predictor import PerformancePredictor
from .sensors import CameraSensor
from .stats import PlayerDashboard
from .tracking import RosterManager, TrackingEngine


def build_demo_players() -> List[Player]:
    return [
        Player(player_id="p1", name="Alex Guard", position="PG", team="Home", season_stats={"points": 220, "games": 10, "assists": 60}),
        Player(player_id="p2", name="Casey Wing", position="SF", team="Home", season_stats={"points": 180, "games": 10, "rebounds": 80}),
        Player(player_id="p3", name="Jordan Big", position="C", team="Away", season_stats={"points": 150, "games": 10, "rebounds": 100}),
    ]


def demo_run(duration_seconds: int = 5) -> None:
    roster_manager = RosterManager()
    players = build_demo_players()
    roster_manager.register_team("Home", [players[0], players[1]])
    roster_manager.register_team("Away", [players[2]])

    sensor = CameraSensor(frame_rate=10)
    scoreboard = Scoreboard(home_team="Home", away_team="Away")
    engine = TrackingEngine(roster=roster_manager.roster_lookup(), scoreboard=scoreboard)
    predictor = PerformancePredictor()

    for frame in sensor.stream_frames(engine.roster.keys(), duration_seconds=duration_seconds):
        engine.process_frame(frame)

    for player in players:
        dashboard = PlayerDashboard(player, engine.stat_book)
        predictions = predictor.predict_next_game(player)
        print("\n" + dashboard.formatted())
        print("Predicted next game: ", predictions)

    print("\nScoreboard display:")
    print(engine.scoreboard.render())
    print("\nSummary:")
    print(engine.summary())


if __name__ == "__main__":
    demo_run()
