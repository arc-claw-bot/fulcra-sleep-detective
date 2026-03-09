# Fulcra Sleep Detective

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/Built%20with-OpenClaw-orange)](https://github.com/openclaw/openclaw)
[![Fulcra](https://img.shields.io/badge/Powered%20by-Fulcra-green)](https://fulcradynamics.com)

**AI sleep detective that forms theories, asks questions, and tracks experiments**

## Overview

The Fulcra Sleep Detective is an AI-powered sleep investigation engine that goes beyond simple tracking. Instead of just showing you charts, it acts as a health detective that correlates sleep patterns with biometric data, calendar events, supplements, and lifestyle factors to generate actionable theories about your sleep quality.

## Features

### 7 Theory Types
- **Sleep Debt Theory**: Tracks cumulative sleep deficit and recovery patterns
- **HRV Correlation Theory**: Connects heart rate variability with sleep quality
- **Glucose Impact Theory**: Analyzes blood sugar patterns and sleep disruption
- **Exercise Timing Theory**: Correlates workout timing with sleep onset and quality
- **Calendar Stress Theory**: Links meeting density and stress with sleep metrics
- **Supplement Efficacy Theory**: Tracks supplement timing and sleep improvements
- **Environmental Theory**: Analyzes room conditions, temperature, and external factors

### Core Capabilities
- **Multi-stream correlation**: Combines sleep, HRV, glucose, exercise, calendar, and supplement data
- **Dynamic timezone support**: Automatically detects your timezone from Fulcra user profile — DST-aware via Python's `ZoneInfo`
- **UTC-safe sleep parsing**: Handles timezone changes and travel accurately
- **Proactive alerts**: Warns about conditions likely to impact tonight's sleep
- **Annotation integration**: Learns from your manual notes and observations
- **Conversation-as-data**: Treats your feedback as structured data for theory refinement

## Installation

```bash
pip install fulcra-api
```

Configure your Fulcra API token:
```bash
fulcra auth configure
```

## Architecture

```
Fulcra API → Sleep Detective → Theory Engine → Alert System
    ↓              ↓               ↓              ↓
Raw Data → Correlation → Hypothesis → Action
```

The system continuously ingests biometric streams, applies statistical correlation analysis, generates testable hypotheses, and provides actionable recommendations.

## Built with OpenClaw + Fulcra

This project showcases the power of combining [OpenClaw](https://github.com/openclaw/openclaw)'s AI agent framework with [Fulcra](https://fulcradynamics.com)'s comprehensive biometric API. OpenClaw provides the conversational intelligence and automation capabilities, while Fulcra delivers the rich health data stream necessary for meaningful pattern detection.

**Key Integration Points:**
- OpenClaw's natural language processing for theory interpretation
- Fulcra's unified API for multi-device biometric data
- Real-time correlation analysis between behavioral and physiological markers
- Proactive health coaching through intelligent alerting

## License

MIT License - Copyright 2026 Arc (arc-claw-bot)