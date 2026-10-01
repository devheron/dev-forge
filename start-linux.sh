#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
if ! command -v python3 >/dev/null || ! python3 -c 'import tkinter' 2>/dev/null; then
  echo 'Instale o requisito: sudo apt-get update && sudo apt-get install python3 python3-tk'
  exit 1
fi
exec python3 app.py
