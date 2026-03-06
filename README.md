# 🔍 Fulcra Sleep Detective

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Built with OpenClaw](https://img.shields.io/badge/Built%20with-OpenClaw-blue)](https://openclaw.ai)
[![Powered by Fulcra](https://img.shields.io/badge/Powered%20by-Fulcra-purple)](https://fulcradynamics.com)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-yellow.svg)](https://python.org)

**AI-powered sleep investigation engine that forms theories, asks questions, and tracks experiments using real biometric data.**

Not another sleep dashboard. This is a health detective — it correlates sleep stages with HRV, glucose, exercise, calendar density, supplement timing, and lifestyle factors to find what actually moves the needle for your sleep.

## Features

- **🧠 Theory-Driven Investigation** — Forms testable hypotheses about your sleep, tracks evidence and counter-evidence
- **📊 Multi-Stream Correlation** — Every insight requires data from 2+ streams (sleep + glucose, HRV + exercise, calendar + deep sleep)
- **⏰ UTC-Safe Sleep Parsing** — Correctly handles overnight sleep sessions that span UTC day boundaries (a surprisingly common bug)
- **🚨 Proactive Alerts** — 7 alert types with cooldown deduplication, only fires when something actionable changes
- **📝 Annotation Integration** — Leverages Fulcra's annotation system (medications, supplements, devices) as positive signals
- **💬 Conversation as Data Source** — Context from human conversation feeds back into the analysis
- **🔄 Investigation Loops** — Observe anomaly → ask user same day → record answer → suggest change → track results → report back

## Data Sources (via Fulcra API)

| Stream | Source | What It Tells You |
|--------|--------|-------------------|
| Sleep stages | Apple Watch | Deep/Core/REM/Awake architecture |
| HRV (SDNN) | Apple Watch | Autonomic nervous system recovery |
| Blood Glucose | Dexcom CGM | Overnight glucose crashes, dawn effect |
| Workouts | Apple Watch | Exercise timing and intensity impact |
| Calendar | Apple Calendar | Meeting density → stress → sleep quality |
| Location | Apple/Google | Travel, environment changes |
| Nutrition | Lose It! | Late eating, macronutrient balance |
| Annotations | Fulcra App | Medication timing, supplement tracking |

## Quick Start

```bash
# Install dependencies
pip install fulcra-api pandas numpy scipy

# Configure Fulcra credentials
# Get your token at https://fulcradynamics.com
export FULCRA_TOKEN_PATH="~/.config/fulcra/token.json"

# Run sleep analysis
python scripts/fulcra_sleep_utils.py

# Run full daily insights
python scripts/fulcra-daily-insights.py

# Run proactive alerts
python scripts/fulcra-proactive-alerts.py
```

## Architecture

```
Fulcra Context API
    ├── sleep_agg()          → Sleep stages, duration, timing
    ├── metric_samples()     → HRV, HR, glucose, steps
    ├── apple_workouts()     → Exercise sessions
    ├── calendar_events()    → Schedule density
    ├── location_visits()    → Travel detection
    ├── moment_annotations() → Medication/supplement timing
    └── scale_annotations()  → Mood ratings
         │
         ▼
    Sleep Detective Engine
    ├── fulcra_sleep_utils.py   — UTC-safe sleep data parsing
    ├── fulcra-daily-insights.py — Cross-domain pattern detection
    ├── fulcra-proactive-alerts.py — Multi-stream anomaly alerting
    └── fulcra-context-dump.py  — Raw data export for LLM reasoning
         │
         ▼
    Theory Engine
    ├── Form hypotheses from data patterns
    ├── Ask user questions to gather context
    ├── Track evidence + counter-evidence
    ├── Suggest behavior experiments
    └── Monitor experiment results
```

## How It Works

1. **Data Collection** — Pulls biometric data from Fulcra every 2 hours during waking hours
2. **Pattern Detection** — 16 built-in detectors scan for cross-domain correlations
3. **Theory Formation** — When a pattern is detected, a testable theory is created
4. **Investigation** — The AI asks the user targeted questions to gather context sensors can't capture
5. **Experiment Tracking** — Behavior changes are suggested and their results monitored
6. **Insight Deduplication** — Never surfaces the same observation twice

## Example Theories

- "Late bedtime correlates with reduced deep sleep — optimal window appears to be 11:00-11:15 PM"
- "Heavy meeting days (6+) predict 40% less deep sleep than light days"
- "Overnight glucose crashes to 75 mg/dL coincide with 1-1.5h wakeups"
- "Exercise improves sleep quality but temporarily suppresses HRV for 24h"

## Privacy

- All data stays local — no cloud processing beyond the Fulcra API
- No PII in this repo — all examples use anonymized data
- Token paths are configurable via environment variables
- Designed for self-hosted OpenClaw deployments

## Built With

- **[OpenClaw](https://openclaw.ai)** — Open-source AI agent framework
- **[Fulcra](https://fulcradynamics.com)** — Personal context API for health data
- **[Context by Fulcra](https://apps.apple.com/us/app/context-by-fulcra/id1633037434)** — iOS app for data collection

## License

MIT — see [LICENSE](LICENSE)
