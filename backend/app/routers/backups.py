from datetime import datetime
from http.client import HTTPException

from fastapi import APIRouter

from app.core.config import settings
from app.services.backup_service import list_backups, last_scheduled_time, last_status, latest_backup_time, \
    record_status, run_backup

router = APIRouter(prefix="/backups", tags=["backups"])


@router.get("/")
def get_backups():
    try:
        files = list_backups()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Supabase'e ulaşılamadı: {exc}")

    latest = latest_backup_time(files)
    return {
        "last_backup_at": latest.isoformat() if latest else None,
        "up_to_date": latest is not None and latest >= last_scheduled_time(datetime.now()),
        "backup_hour": settings.backup_hour,
        "keep_days": settings.backup_keep_days,
        "last_status": last_status,
        "files": [
            {"name": file["name"], "size_bytes": file["metadata"]["size"], "updated_at": file["updated_at"]}
            for file in files
        ]
    }


@router.post("/run")
def run_backup_now():
    try:
        result = run_backup()
    except Exception as exc:
        record_status(False, str(exc))
        raise HTTPException(status_code=502, detail=f"Yedek Alınamadı: {exc}")
    record_status(True, f"{result['file']} yüklendi")
    return result