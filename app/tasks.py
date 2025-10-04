import os
from pathlib import Path
from .celery_app import celery_app
from .jobs.users_csv import run as fetch_and_save

USERS_URL = os.getenv("USERS_URL", "https://jsonplaceholder.typicode.com/users")
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/data"))
OUTPUT_FILE = OUTPUT_DIR / "users.csv"


@celery_app.task(name="app.tasks.fetch_and_save_users")
def fetch_and_save_users() -> str:
    """Celery task: fetch users and save CSV. Returns output file path."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = fetch_and_save(url=USERS_URL, out_path=OUTPUT_FILE)
    return str(csv_path)
