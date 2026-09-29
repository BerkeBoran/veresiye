import gzip
import logging
import sqlite3
import tempfile
from datetime import date, timedelta, datetime, time
from pathlib import Path

from supabase import create_client, Client

from app.core.config import settings

BACKUP_FOLDER = "daily"
NAME_FORMAT = "%Y-%m-%d_%H%M"

logger = logging.getLogger(__name__)
last_status = {"time": None, "ok": None, "message": None}


def get_supabase() -> Client:
    return create_client(settings.supabase_url, settings.supabase_service_key.get_secret_value())


def backup_file_name(taken_at: datetime) -> str:
    return f"{BACKUP_FOLDER}/{taken_at.strftime(NAME_FORMAT)}.db.gz"


def parse_backup_time(file_name: str) -> datetime | None:
    try:
        return datetime.strptime(file_name.removesuffix(".db.gz"), NAME_FORMAT)
    except ValueError:
        return None


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
    return  [file for file in files if parse_backup_time(file["name"]) is not None]


def delete_old_backups(today: date) -> list[str]:
    cutoff = today - timedelta(days=settings.backup_keep_days)
    old = []
    for file in list_backups():
        if parse_backup_time(file["name"]).date() < cutoff:
            old.append(f"{BACKUP_FOLDER}/{file['name']}")
    if old:
        get_supabase().storage.from_(settings.backup_bucket).remove(old)
    return old


def run_backup() -> dict:
    now = datetime.now()
    data = gzip.compress(make_snapshot())
    path = backup_file_name(now)

    bucket = get_supabase().storage.from_(settings.backup_bucket)
    bucket.upload(path, data, {"content-type": "application/gzip", "upsert": "true"})

    deleted = delete_old_backups(now.date())
    return {"file": path, "size_bytes": len(data), "deleted": deleted}


def last_scheduled_time(now: datetime) -> datetime:
    today_slot = datetime.combine(now.date(), time(hour=settings.backup_hour))
    if now >= today_slot:
        return today_slot
    return today_slot - timedelta(days=1)


def latest_backup_time(files: list[dict]) -> datetime | None:
    times = [parse_backup_time(file["name"]) for file in files]
    return max(times) if times else None


def record_status(ok: bool, message: str) -> None:
    last_status.update({"time": datetime.now().isoformat(timespec="seconds"), "ok": ok, "message": message})


def backup_if_needed() -> None:
    try:
        latest = latest_backup_time(list_backups())
        if latest is not None and latest >= last_scheduled_time(datetime.now()):
            return
        result = run_backup()
        record_status(True, f"{result['file']} yüklendi")
    except Exception as exc:
        logger.exception("Otomatik yedekleme başarısız oldu")
        record_status(False, str(exc))