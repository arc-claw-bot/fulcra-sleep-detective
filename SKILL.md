# Fulcra Sleep Detective - OpenClaw Skill

## Overview
AI-powered sleep investigation that goes beyond tracking to generate theories and actionable insights.

## Commands
- `sleep-theory` - Generate new theories based on recent patterns
- `sleep-alert` - Check for factors that might impact tonight's sleep
- `sleep-context` - Dump comprehensive sleep and biometric context
- `sleep-insights` - Daily analysis with correlations and recommendations

## Dependencies
- `fulcra-api` - Biometric data access
- `pandas` - Data analysis
- `numpy` - Statistical calculations

## Configuration
Set up Fulcra API credentials:
```
fulcra auth configure
```

## Usage in OpenClaw
This skill integrates with OpenClaw's conversation system to provide contextual sleep insights during natural conversation. When sleep, energy, or health topics come up, the skill can automatically surface relevant theories and data.