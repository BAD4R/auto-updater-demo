#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path
from git import Repo

BASE = Path(__file__).resolve().parents[1] / "releases" / "FakeApp"
ver_file = BASE / "latest_version.txt"
sha_file = BASE / "latest_sha256.txt"
installer = BASE / "fake_app.bat"

def sha256sum(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def main():
    new_ver = input("Введите новую версию (x.y.z): ").strip()
    if not new_ver:
        print("Отменено."); return

    ver_file.write_text(new_ver + "\n", encoding="utf-8")
    sha_file.write_text(sha256sum(installer) + "\n", encoding="utf-8")

    repo = Repo(BASE.parents[2])
    repo.index.add([str(ver_file), str(sha_file), str(installer)])
    repo.index.commit(f"release FakeApp v{new_ver}")
    repo.remote().push()
    print(f"v{new_ver} опубликована на GitHub")

if __name__ == "__main__":
    main()
