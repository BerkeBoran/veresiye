import gzip
import sqlite3
import tempfile
from datetime import date, timedelta
from pathlib import Path

from supabase import create_client, Client

from app.core.config import settings

BACKUP_FOLDER = "daily"


def get_supabase() -> Client:
    return create_client(settings.supabase_url, settings.supabase_service_key.get_secret_value())


def backup_file_name(day: date) -> str:
    return f"{BACKUP_FOLDER}/{day.isoformat()}.db.gz"


def make_snapshot() -> bytes:
    with tempfile.TemporaryDirectory() as tmp:
        snapshot_path = Path(tmp) / "snapshot.db"
        source = sqlite3.connect(settings.database_path)
        target = sqlite3.connect(snapshot_path)
        try:
            source.backup(target)
        finally:
            target.close()
            source.close()
        return  snapshot_path.read_bytes()


def list_backups() -> list[dict]:
    bucket = get_supabase().storage.from_(settings.backup_bucket)
    files = bucket.list(BACKUP_FOLDER, {"sortBy": {"column": "name", "order": "desc"}})
    return  [file for file in files if file["name"].endswith(".db.gz")]


def delete_old_backups(today: date) -> list[str]:
    cutoff = today - timedelta(days=settings.backup_keep_days)
    old = []
    for file in list_backups():
        day = date.fromisoformat(file["name"].removesuffix(".db.gz"))
        if day < cutoff:
            old.append(f"{BACKUP_FOLDER}/{file['name']}")
    if old:
        get_supabase().storage.from_(settings.backup_bucket).remove(old)
    return old


def run_backup() -> dict:
    today = date.today()
    data = gzip.compress(make_snapshot())
    path = backup_file_name(today)

    bucket = get_supabase().storage.from_(settings.backup_bucket)
    bucket.upload(path, data, {"content-type": "application/gzip", "upsert": "true"})

    deleted = delete_old_backups(today)
    return {"file": path, "size_bytes": len(data), "deleted": deleted}