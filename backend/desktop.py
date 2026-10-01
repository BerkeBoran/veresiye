import base64
import logging
import os
import socket
import sys
import threading
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

import uvicorn
import webview

from app.core.config import DATA_DIR
from app.main import app

HOST = "127.0.0.1"
PORT = 8765
APP_TITLE = "Veresiye Takip"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s %(name)s: %(message)s",
    handlers=[RotatingFileHandler(DATA_DIR / "veresiye.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")]
)
logger = logging.getLogger("desktop")


def show_error(message: str) -> None:
    logger.error(message)
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, APP_TITLE, 0x10)
    else:
        print(message, file=sys.stderr)


def port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((HOST, port)) == 0


def start_server() -> uvicorn.Server:
    config = uvicorn.Config(app, host=HOST, port=PORT, log_config=None, lifespan="on")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, name="uvicorn", daemon=True)
    thread.start()
    while not server.started:
        if not thread.is_alive():
            raise RuntimeError("Sunucu Başlatılamadı")
        time.sleep(0.05)
    return server


class Api:


    def save_file(self, file_name: str, data_base64: str) -> None:
        desktop = Path.home() / "Desktop"
        result = webview.windows[0].create_file_dialog(
            webview.FileDialog.SAVE,
            directory=str(desktop if desktop.exists() else Path.home()),
            save_filename=file_name,
            file_types=("Excel dosyası (*.xlsx",),
        )
        if not result:
            return None
        path = Path(result if isinstance(result, str) else result[0])
        path.write_bytes(base64.b64decode(data_base64))
        logger.info("Excel kaydedildi: %s", path)
        return str(path)


def main() -> None:
    if port_in_use(PORT):
        show_error("Veresiye takip zaten açık.")
        return

    try:
        server = start_server()
    except Exception:
        logger.exception("Sunucu başlatılamadı")
        show_error(f"Program başlatılamadı. \n\nAyrıntılar: {DATA_DIR / 'veresiye.log'}")
        return
    webview.create_window(
        APP_TITLE,
        f"http://{HOST}:{PORT}/",
        js_api=Api(),
        maximized=True,
        min_size=(1100, 700),
    )
    webview.start()
    server.should_exit = True


if __name__ == "__main__":
    main()