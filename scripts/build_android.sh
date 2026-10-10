#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v python3.12 >/dev/null 2>&1; then
    echo "Python 3.12 tidak ditemukan. Jalankan bash .devcontainer/setup-android.sh terlebih dahulu." >&2
    exit 1
fi

if [[ ! -x .venv/bin/python ]]; then
    python3.12 -m venv .venv
fi

if [[ "$(.venv/bin/python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')" != "3.12" ]]; then
    echo "Environment .venv harus menggunakan Python 3.12. Hapus .venv lalu jalankan script ini lagi." >&2
    exit 1
fi

JAVA_HOME=""
for candidate in /usr/lib/jvm/java-17-openjdk-amd64 /usr/lib/jvm/java-21-openjdk-amd64; do
    if [[ -x "$candidate/bin/java" ]]; then
        JAVA_HOME="$candidate"
        break
    fi
done

if [[ -z "$JAVA_HOME" ]]; then
    echo "JDK 17/21 tidak ditemukan. Jalankan bash .devcontainer/setup-android.sh terlebih dahulu." >&2
    exit 1
fi

export JAVA_HOME
export PATH="$JAVA_HOME/bin:$ROOT_DIR/.venv/bin:$PATH"
export PIP_CONSTRAINT="$ROOT_DIR/requirements-build.txt"
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-build.txt

if [[ -d .buildozer/android/platform ]]; then
    find .buildozer/android/platform -mindepth 3 -maxdepth 3 \
        -type d -path '*/build/venv' -prune -exec rm -rf -- {} +
fi

exec buildozer android debug