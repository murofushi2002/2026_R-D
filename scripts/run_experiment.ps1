param(
  [string]$Config = "configs/experiment.example.yaml",
  [switch]$SkipDownloads,
  [switch]$SkipTraining
)

$ErrorActionPreference = "Stop"
$Python = ".\.venv\Scripts\python.exe"

& $Python -m sentipersona_airbnb.cli init -c $Config

if (-not $SkipDownloads) {
  & $Python -m sentipersona_airbnb.cli download -c $Config --all
}

& $Python -m sentipersona_airbnb.cli preprocess-airbnb -c $Config
& $Python -m sentipersona_airbnb.cli validate-occupancy -c $Config
& $Python -m sentipersona_airbnb.cli label-airbnb-sentiment -c $Config

if (-not $SkipTraining) {
  & $Python -m sentipersona_airbnb.cli train -c $Config
  & $Python -m sentipersona_airbnb.cli evaluate-sentiment-encoder -c $Config
}

& $Python -m sentipersona_airbnb.cli embed -c $Config
& $Python -m sentipersona_airbnb.cli cluster -c $Config
& $Python -m sentipersona_airbnb.cli personas -c $Config
& $Python -m sentipersona_airbnb.cli timeseries -c $Config
& $Python -m sentipersona_airbnb.cli evaluate -c $Config
