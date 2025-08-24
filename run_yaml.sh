#!/usr/bin/env bash
set -euo pipefail

# ---------- Locators ----------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Prefer the converter sitting next to this script:
SCRIPT_DEFAULT="${SCRIPT_DIR}/excel_to_yaml_single.py"
# Fallback if you keep things in Documents:
SCRIPT_DOCS="${HOME}/Documents/excel_to_yaml_single.py"

if [[ -f "${SCRIPT_DEFAULT}" ]]; then
  SCRIPT="${SCRIPT_DEFAULT}"
elif [[ -f "${SCRIPT_DOCS}" ]]; then
  SCRIPT="${SCRIPT_DOCS}"
else
  echo "❌ Could not find excel_to_yaml_single.py."
  echo "   Expected at: ${SCRIPT_DEFAULT}  (preferred)  or  ${SCRIPT_DOCS}"
  exit 1
fi

# ---------- Inputs / Outputs ----------
DOCS="${HOME}/Documents"
INPUT="${DOCS}/input.xlsx"            # default: Documents/input.xlsx
OUTPUT="${DOCS}/output.yaml"          # default: Documents/output.yaml

# Allow overriding input/output from CLI: ./run_yaml.sh /path/to/in.xlsx /path/to/out.yaml
if [[ "${#}" -ge 1 ]]; then INPUT="$1"; fi
if [[ "${#}" -ge 2 ]]; then OUTPUT="$2"; fi

# Python binary (can override): PYTHON_BIN=.venv/bin/python ./run_yaml.sh
PYTHON_BIN="${PYTHON_BIN:-python3}"

# ---------- Checks ----------
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "❌ ${PYTHON_BIN} not found. On macOS: brew install python"
  exit 1
fi

if [[ ! -f "${INPUT}" ]]; then
  echo "❌ ERROR: ${INPUT} not found"
  echo "   Put your Excel as 'input.xlsx' in ${DOCS},"
  echo "   or run: ./run_yaml.sh /full/path/to/your.xlsx"
  exit 1
fi

# Ensure pandas/openpyxl are available; install appropriately for venv vs system
if ! "${PYTHON_BIN}" - <<'PY' >/dev/null 2>&1
import importlib
importlib.import_module("pandas")
importlib.import_module("openpyxl")
PY
then
  echo "📦 Installing required Python packages (pandas, openpyxl)..."
  if [[ -n "${VIRTUAL_ENV:-}" ]]; then
    "${PYTHON_BIN}" -m pip install --upgrade pip
    "${PYTHON_BIN}" -m pip install pandas openpyxl
  else
    "${PYTHON_BIN}" -m pip install --upgrade pip
    "${PYTHON_BIN}" -m pip install --user pandas openpyxl
  fi
fi

# ---------- Convert ----------
echo "✅ Converting ${INPUT} → ${OUTPUT} using ${SCRIPT} ..."
"${PYTHON_BIN}" "${SCRIPT}" "${INPUT}" -o "${OUTPUT}" \
  --fail-on-duplicate-nzbn \
  --fail-on-duplicate-account \
  --require-numeric-paymentlimit \
  --max-fourth 5000 \
  --max-creditor 1

echo "🎉 Done. YAML at: ${OUTPUT}"
