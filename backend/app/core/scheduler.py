import threading

from app.services.backup_service import backup_if_needed

CHECK_INTERVAL_SECONDS = 10 * 60

_stop = threading.Event()


def _loop() -> None:
    while not _stop.is_set():
        backup_if_needed()
        _stop.wait(CHECK_INTERVAL_SECONDS)


def start_backup_scheduler() -> None:
    _stop.clear()
    threading.Thread(target=_loop, name="backup_scheduler", daemon=True).start()


def stop_backup_scheduler() -> None:
    _stop.set()