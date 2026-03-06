#!/usr/bin/env python3
"""
MIT License

Copyright (c) 2026 OpenClaw Community

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Fulcra Sleep Data Utility Library

A comprehensive utility library for accessing and processing sleep data from
the Fulcra API. Handles timezone conversion, sleep stage analysis, and 
provides convenient functions for sleep pattern analysis.

Key Features:
- Automatic timezone handling (ET ↔ UTC conversion)
- Sleep stage analysis (deep, core, REM, awake)
- Fragmentation and efficiency calculations
- Historical sleep data retrieval
- Robust error handling for API inconsistencies

Built with OpenClaw + Fulcra for health data automation.
"""

import json
import os
import pandas as pd
from datetime import datetime, timedelta, timezone, date
from zoneinfo import ZoneInfo


ET = ZoneInfo('America/New_York')
STAGE_NAMES = {2: 'deep', 3: 'core', 4: 'rem', 5: 'awake'}


def get_fulcra_client():
    """Get authenticated Fulcra API client with configurable token path."""
    from fulcra_api.core import FulcraAPI
    api = FulcraAPI()
    
    # Configurable token path via environment variable
    token_path = os.environ.get(
        "FULCRA_TOKEN_PATH", 
        os.path.expanduser("~/.config/fulcra/token.json")
    )
    
    with open(token_path, 'r') as f:
        td = json.load(f)
    
    api.set_cached_access_token(td['access_token'])
    api.set_cached_refresh_token(td['refresh_token'])
    return api


def _get_target_utc_date(for_date=None):
    """
    Get the correct UTC period date for "last night's sleep."
    
    The key insight: today's date in ET IS the UTC period date where
    last night's sleep data lives. This works because:
    - Sleep 11 PM ET Mar 5 → 6 AM ET Mar 6 lands in UTC Mar 6 bucket
    - On Mar 6 in ET (any time of day), we want that Mar 6 bucket
    - Using today's ET date (not current UTC date) avoids the PM bug
    
    Args:
        for_date: Optional date object (ET date). Defaults to today ET.
        
    Returns:
        date: The correct UTC period date for sleep data retrieval
    """
    if for_date is not None:
        return for_date
    return datetime.now(ET).date()


def get_last_night_sleep(client=None, target_date=None):
    """
    Get last night's sleep data from the correct UTC period bucket.
    
    Args:
        client: FulcraAPI instance (created if None)
        target_date: date object (ET date for the morning after sleep).
                     Defaults to today ET. This maps directly to the
                     UTC period bucket containing that night's data.
    
    Returns:
        dict with keys: status, total_sleep_h, stages (dict of minutes),
        deep_pct, rem_pct, frag_pct, frag_label, awake_min, bedtime_str,
        wake_str, efficiency, sleep_start, sleep_end
    """
    if client is None:
        client = get_fulcra_client()
    
    target = _get_target_utc_date(target_date)
    
    # Query window: target date ± 1 day to handle sync delays
    start = datetime(target.year, target.month, target.day,
                     tzinfo=timezone.utc) - timedelta(days=2)
    end = datetime(target.year, target.month, target.day,
                   tzinfo=timezone.utc) + timedelta(days=2)
    
    try:
        df = client.sleep_agg(start.isoformat(), end.isoformat())
    except Exception as e:
        return {"status": "error", "error": str(e)}
    
    if not hasattr(df, 'iterrows') or len(df) == 0:
        return {"status": "no_data"}
    
    # Parse period dates and select the target bucket
    df['period_date'] = pd.to_datetime(df['period_start_time']).dt.date
    night = df[df['period_date'] == target]
    
    if len(night) == 0:
        # Sync delay: fall back to the most recent bucket before target
        available = df[df['period_date'] <= target]
        if len(available) == 0:
            return {"status": "no_data"}
        latest = available['period_date'].max()
        night = df[df['period_date'] == latest]
    
    if len(night) == 0:
        return {"status": "no_data"}
    
    # Parse stages from the single UTC bucket (contains complete night)
    stages = {}
    total_sleep_ms = 0
    awake_ms = 0
    sleep_start = None
    sleep_end = None
    
    for _, row in night.iterrows():
        stage = int(row['value'])
        ms = float(row.get('sum_ms', 0) or 0)
        name = STAGE_NAMES.get(stage, f'stage_{stage}')
        stages[name] = stages.get(name, 0) + round(ms / 60000, 1)
        
        if stage in (2, 3, 4):
            total_sleep_ms += ms
            min_start = str(row.get('min_start_time', ''))
            max_end = str(row.get('max_end_time', ''))
            if min_start and min_start != 'nan' and (not sleep_start or min_start < sleep_start):
                sleep_start = min_start
            if max_end and max_end != 'nan' and (not sleep_end or max_end > sleep_end):
                sleep_end = max_end
        elif stage == 5:
            awake_ms += ms
    
    total_bed_ms = total_sleep_ms + awake_ms
    total_sleep_h = total_sleep_ms / 3600000
    awake_min = awake_ms / 60000
    frag_pct = (awake_ms / total_bed_ms * 100) if total_bed_ms > 0 else 0
    
    # Calculate sleep stage percentages
    deep_ms = stages.get('deep', 0) * 60000
    deep_pct = (deep_ms / total_sleep_ms * 100) if total_sleep_ms > 0 else 0
    rem_ms = stages.get('rem', 0) * 60000
    rem_pct = (rem_ms / total_sleep_ms * 100) if total_sleep_ms > 0 else 0
    core_ms = stages.get('core', 0) * 60000
    core_pct = (core_ms / total_sleep_ms * 100) if total_sleep_ms > 0 else 0
    
    # Sleep efficiency calculation
    efficiency = (total_sleep_ms / total_bed_ms * 100) if total_bed_ms > 0 else 0
    
    # Fragmentation analysis with emoji indicators
    if frag_pct < 10:
        frag_label, emoji = "low", "🟢"
    elif frag_pct < 20:
        frag_label, emoji = "moderate", "🟡"
    elif frag_pct < 30:
        frag_label, emoji = "high", "🟠"
    else:
        frag_label, emoji = "severe", "🔴"
    
    # Format bedtime and wake times for display
    bedtime_str = ""
    wake_str = ""
    if sleep_start:
        try:
            dt = datetime.fromisoformat(sleep_start.replace('Z', '+00:00'))
            bedtime_str = dt.astimezone(ET).strftime('%-I:%M %p')
        except:
            pass
    if sleep_end:
        try:
            dt = datetime.fromisoformat(sleep_end.replace('Z', '+00:00'))
            wake_str = dt.astimezone(ET).strftime('%-I:%M %p')
        except:
            pass
    
    return {
        "status": "ok",
        "total_sleep_h": round(total_sleep_h, 1),
        "total_sleep_min": round(total_sleep_ms / 60000),
        "stages": stages,
        "deep_pct": round(deep_pct, 1),
        "rem_pct": round(rem_pct, 1),
        "core_pct": round(core_pct, 1),
        "frag_pct": round(frag_pct, 1),
        "frag_label": frag_label,
        "frag_emoji": emoji,
        "awake_min": round(awake_min),
        "efficiency": round(efficiency, 1),
        "bedtime_str": bedtime_str,
        "wake_str": wake_str,
        "sleep_start": sleep_start,
        "sleep_end": sleep_end,
    }


def get_sleep_history(client=None, days=7):
    """
    Get multiple nights of sleep data for trend analysis.
    
    Args:
        client: FulcraAPI instance (created if None)
        days: Number of days of history to retrieve (default: 7)
    
    Returns:
        list: Sleep data dicts (newest first), one per night.
              Each night uses the ET date as the key.
    """
    if client is None:
        client = get_fulcra_client()
    
    today_et = datetime.now(ET).date()
    results = []
    
    for d in range(days):
        target = today_et - timedelta(days=d)
        night = get_last_night_sleep(client, target_date=target)
        if night.get("status") == "ok":
            night["date"] = str(target)
            results.append(night)
    
    return results


# Example usage and testing
if __name__ == "__main__":
    print("Testing Fulcra sleep utility...")
    print(f"Today ET: {datetime.now(ET).date()}")
    print(f"Current UTC: {datetime.now(timezone.utc).date()}")
    print()
    
    result = get_last_night_sleep()
    if result["status"] == "ok":
        print(f"Last night: {result['total_sleep_h']}h sleep, {result['efficiency']:.0f}% efficiency")
        print(f"  Deep: {result['stages'].get('deep', 0):.0f}min ({result['deep_pct']:.0f}%)")
        print(f"  Core: {result['stages'].get('core', 0):.0f}min ({result['core_pct']:.0f}%)")
        print(f"  REM: {result['stages'].get('rem', 0):.0f}min ({result['rem_pct']:.0f}%)")
        print(f"  Awake: {result['awake_min']}min ({result['frag_pct']:.0f}%)")
        print(f"  Bedtime: {result['bedtime_str']} → Wake: {result['wake_str']}")
    else:
        print(f"Status: {result}")
    
    print("\nHistory (last 5 nights):")
    for night in get_sleep_history(days=5):
        print(f"  {night['date']}: {night['total_sleep_h']}h, deep {night['deep_pct']:.0f}%, REM {night['rem_pct']:.0f}%, eff {night['efficiency']:.0f}%")