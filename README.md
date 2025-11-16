# SBVS

Simulated camera and sensor stack that tracks basketball player and ball movement, updates a scoreboard, and exposes player/coach views for stats and predictions.

## Features
- **Camera simulation:** `CameraSensor` streams frame data with player/ball positions and shot events.
- **Tracking engine:** Processes frames, logs movement, and updates a live `Scoreboard` whenever a shot is made.
- **Coach inputs:** `RosterManager` lets coaches register teams and players for tracking.
- **Player dashboard:** `PlayerDashboard` aggregates per-game and season stats so players can view their data.
- **Performance prediction:** `PerformancePredictor` forecasts next-game points, rebounds, and assists using weighted averages.

## Running the demo
```bash
python -m sbvs.app
```
The script simulates a short game segment, prints player dashboards with predictions, and displays the scoreboard state.

## Running in GitHub Codespaces
1. Create or open a Codespace for this repository (it ships with Python preinstalled).
2. In the Codespace terminal, run `python -m sbvs.app` to start the simulation demo.
3. Watch the console for live scoreboard updates, player dashboards, and next-game predictions generated from the simulated frames.
