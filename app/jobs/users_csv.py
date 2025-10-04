from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import List, Dict
import httpx

DEFAULT_URL = os.getenv("USERS_URL", "https://jsonplaceholder.typicode.com/users")
DEFAULT_OUT = Path(os.getenv("OUTPUT_DIR", "data")) / "users.csv"


def fetch_users(url: str = DEFAULT_URL) -> List[Dict]:
    """Fetch users from public API and return as list[dict]."""
    with httpx.Client(timeout=30.0) as client:
        resp = client.get(url)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            raise ValueError("Unexpected response format: expected a list.")
        return data


def save_users_csv(users: List[Dict], out_path: Path = DEFAULT_OUT) -> Path:
    """Write id, name, email to CSV; return output path."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "email"])
        for u in users:
            writer.writerow([u.get("id"), u.get("name"), u.get("email")])
    return out_path


def run(url: str = DEFAULT_URL, out_path: Path = DEFAULT_OUT) -> Path:
    """Fetch and save; return final CSV path."""
    users = fetch_users(url)
    if not users:
        raise ValueError("No users returned from API.")
    return save_users_csv(users, out_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetch users and save as CSV.")
    parser.add_argument("--url", default=DEFAULT_URL, help="Source URL")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output CSV path")
    args = parser.parse_args()

    out_path = run(url=args.url, out_path=Path(args.out))
    print(f"Saved CSV to: {out_path.resolve()}")
