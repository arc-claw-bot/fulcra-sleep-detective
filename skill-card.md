# Fulcra Sleep Detective

Retired Fulcra sleep-analysis skill.

This package no longer ships sleep-analysis scripts, background monitors, proactive alerts, or broad context dumps. It exists as a compatibility pointer for agents and users who still discover the old `fulcra-sleep-detective` name.

## Use Instead

- `fulcra-context` for user-consented sleep, biometric, activity, calendar, location, and metric-catalog reads.
- `fulcra-annotations` for user-approved annotation writes.
- `fulcra-agent-teams`, `fulcra-memory`, and `fulcra-tracking` for coordination, memory, and event-tracking workflows.

## Safety Model

- Ask for consent for the current request.
- Read only the smallest useful time window and metric set.
- Prefer summaries and trends over raw records.
- Do not retain, export, screenshot, publish, or forward Fulcra records without explicit approval for that exact destination.
- Do not run background monitoring, scheduled polling, proactive alerts, or persistent files from this retired skill.
- Use synthetic data for public examples, demos, tests, and documentation by default.

## Current Path

For sleep questions, use `fulcra-context` and follow its current onboarding flow.
