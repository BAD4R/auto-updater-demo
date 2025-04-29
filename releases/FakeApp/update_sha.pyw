#!/usr/bin/env python3
"""
update_sha256.py

Вычисляет SHA-256 указанного файла и записывает его значение в файл latest_sha256.txt.
Использование:
    python update_sha256.py \
        --source fake_app.bat \
        --dest   latest_sha256.txt

Если аргументы не заданы, по умолчанию возьмёт вышеуказанные пути.
"""
import argparse
import hashlib
from pathlib import Path

def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    p = argparse.ArgumentParser(description='Update latest_sha256.txt from source file')
    p.add_argument('--source', '-s', type=Path,
                   default=Path('fake_app.bat'),
                   help='Путь к исходному файлу для хеширования')
    p.add_argument('--dest', '-d', type=Path,
                   default=Path('latest_sha256.txt'),
                   help='Путь к целевому файлу для записи хеша')
    args = p.parse_args()

    src = args.source.resolve()
    dst = args.dest.resolve()

    if not src.exists():
        print(f"Ошибка: исходный файл не найден: {src}")
        return

    sha = compute_sha256(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open('w', encoding='utf-8') as f:
        f.write(sha + '\n')

    print(f"Записан SHA-256 '{sha}' в {dst}")

if __name__ == '__main__':
    main()
