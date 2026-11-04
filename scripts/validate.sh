#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
bash -n scripts/install.sh scripts/validate.sh
python3 -m unittest discover -s tests -v
