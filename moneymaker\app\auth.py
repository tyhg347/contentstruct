"""Simple API key authentication module."""

import json
import secrets
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _ensure_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _keys_path() -> Path:
    return DATA_DIR / "api_keys.json"


def _usage_path() -> Path:
    return DATA_DIR / "usage.json"


def _load_json(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def _save_json(path: Path, data: dict):
    _ensure_dir()
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def init_default_keys():
    """Create a default admin key on first run."""
    keys = _load_json(_keys_path())
    if not keys:
        api_key = "cs_" + secrets.token_hex(16)
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        keys[key_hash] = {
            "name": "Default Admin Key",
            "plan": "pro",
            "created": datetime.now(timezone.utc).isoformat(),
            "monthly_limit": 10000,
            "usage_this_month": 0,
            "active": True,
        }
        _save_json(_keys_path(), keys)
        sep = "=" * 60
        key_line = "DEFAULT API KEY (save this!): " + api_key
        sys.stdout.buffer.write(("\n" + sep + "\n").encode("utf-8"))
        sys.stdout.buffer.write((key_line + "\n").encode("utf-8"))
        sys.stdout.buffer.write((sep + "\n\n").encode("utf-8"))
        sys.stdout.buffer.flush()
        # Also save to a file for easy access
        key_file = DATA_DIR.parent / ".api_key.txt"
        key_file.write_text(api_key, encoding="utf-8")
    return keys


def verify_key(api_key: str | None) -> dict | None:
    """Verify an API key and return its record."""
    if not api_key:
        return None
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    keys = _load_json(_keys_path())
    record = keys.get(key_hash)
    if record and record.get("active", False):
        return record
    return None


def record_usage(api_key: str, endpoint: str, success: bool):
    """Record API usage."""
    usage = _load_json(_usage_path())
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if today not in usage:
        usage[today] = {}
    if key_hash not in usage[today]:
        usage[today][key_hash] = {"calls": 0, "success": 0, "failed": 0}

    usage[today][key_hash]["calls"] += 1
    if success:
        usage[today][key_hash]["success"] += 1
    else:
        usage[today][key_hash]["failed"] += 1
    _save_json(_usage_path(), usage)

    keys = _load_json(_keys_path())
    if key_hash in keys:
        keys[key_hash]["usage_this_month"] = keys[key_hash].get("usage_this_month", 0) + 1
        _save_json(_keys_path(), keys)


def get_usage_report(api_key: str) -> dict:
    """Get usage stats for an API key."""
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    usage = _load_json(_usage_path())
    monthly = _load_json(_keys_path()).get(key_hash, {})

    total = 0
    daily: dict[str, dict] = {}
    for date, day_data in sorted(usage.items()):
        if key_hash in day_data:
            daily[date] = day_data[key_hash]
            total += day_data[key_hash]["calls"]

    return {
        "total_calls": total,
        "monthly_limit": monthly.get("monthly_limit", 0),
        "usage_this_month": monthly.get("usage_this_month", 0),
        "daily": daily,
        "plan": monthly.get("plan", "free"),
    }
