param(
  [switch]$GpuCu121,
  [switch]$FastText
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
  python -m venv .venv
}

.\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel

if ($GpuCu121) {
  .\.venv\Scripts\python.exe -m pip install -r requirements-gpu-cu121.txt
} elseif ($FastText) {
  .\.venv\Scripts\python.exe -m pip install -e ".[dev,viz,fasttext]"
} else {
  .\.venv\Scripts\python.exe -m pip install -r requirements.txt
}

.\.venv\Scripts\python.exe -m pytest
