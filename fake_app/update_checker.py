import hashlib, os, subprocess, sys, tempfile, requests
from pathlib import Path
from packaging.version import Version

# === конфигурация ===
GH_USER      = "BAD4R"
BASE_URL     = f"https://raw.githubusercontent.com/{GH_USER}/auto-updater-demo/main/releases/FakeApp"
LATEST_VER   = f"{BASE_URL}/latest_version.txt"
LATEST_SHA   = f"{BASE_URL}/latest_sha256.txt"
LATEST_FILE  = f"{BASE_URL}/fake_app.bat"

TIMEOUT = (5, 10)           # connect/read
LOCAL_DIR = Path(__file__).parent
TARGET    = LOCAL_DIR / "fake_app.bat"

def sha256sum(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def fetch_text(url: str) -> str:
    return requests.get(url, timeout=TIMEOUT).text.strip()

def download(url: str, dst: Path):
    r = requests.get(url, timeout=TIMEOUT)
    r.raise_for_status()
    dst.write_bytes(r.content)

def main():
    if len(sys.argv) != 2:
        print("[Updater] Аргумент: локальная_версия"); return
    local_ver = Version(sys.argv[1])

    try:
        remote_ver = Version(fetch_text(LATEST_VER))
    except Exception as e:
        print("[Updater] Не смог получить удалённую версию:", e); return

    if remote_ver <= local_ver:
        print("[Updater] Установлена актуальная версия."); return

    print(f"[Updater] Доступно обновление: {local_ver} → {remote_ver}")
    choice = input(" Обновить сейчас? (y/N): ").lower()
    if choice != "y":
        return

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp) / "fake_app.new"
        print("[Updater] Скачиваю новую версию...")
        download(LATEST_FILE, tmp_path)

        remote_sha = fetch_text(LATEST_SHA)
        if sha256sum(tmp_path) != remote_sha:
            print("[Updater] Контрольная сумма не совпала! Отмена."); return

        # записываем временный update.bat
        upd = LOCAL_DIR / "update.bat"
        upd.write_text(fr"""@echo off
timeout /t 2 >nul
move /y "{tmp_path}" "{TARGET}"
del "%~f0"
""", encoding="utf-8")

        print("[Updater] Запускаю установку...")
        subprocess.Popen(['cmd', '/c', 'start', '', str(upd)])  # фоново
        print(" Закройте окно FakeApp и запустите программу снова.")
if __name__ == "__main__":
    main()
