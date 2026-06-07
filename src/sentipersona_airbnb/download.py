from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from requests.utils import requote_uri
from tqdm import tqdm

from .config import cfg_get, standard_paths
from .utils import file_sha256, write_json

FASTTEXT_LID_URL = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"


@dataclass(frozen=True)
class DownloadedFile:
    filename: str
    url: str
    path: str
    sha256: str
    bytes: int


def download_file(url: str, dest: Path, chunk_size: int = 1024 * 1024) -> DownloadedFile:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()
        total = int(response.headers.get("content-length", 0))
        with dest.open("wb") as handle, tqdm(
            total=total,
            unit="B",
            unit_scale=True,
            desc=dest.name,
            disable=total == 0,
        ) as progress:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    handle.write(chunk)
                    progress.update(len(chunk))
    return DownloadedFile(
        filename=dest.name,
        url=url,
        path=str(dest),
        sha256=file_sha256(dest),
        bytes=dest.stat().st_size,
    )


def _extract_snapshot(url: str) -> str:
    match = re.search(r"/(\d{4}-\d{2}-\d{2})/", unquote(url))
    return match.group(1) if match else "unknown"


def discover_inside_airbnb_urls(cfg: dict) -> dict[str, str]:
    page_url = cfg_get(cfg, "data.inside_airbnb_page")
    city_slug = str(cfg_get(cfg, "data.city_slug", "")).lower()
    wanted_files = set(cfg_get(cfg, "data.inside_airbnb_files", []))
    snapshot = cfg_get(cfg, "data.inside_airbnb_snapshot", "latest")

    response = requests.get(page_url, timeout=60)
    response.raise_for_status()
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    candidates: dict[str, list[str]] = {filename: [] for filename in wanted_files}
    for anchor in soup.find_all("a", href=True):
        href = requote_uri(urljoin(page_url, anchor["href"]))
        parsed = urlparse(href)
        if "data.insideairbnb.com" not in parsed.netloc:
            continue
        decoded_path = unquote(parsed.path).lower()
        if f"/{city_slug}/" not in decoded_path:
            continue
        filename = Path(decoded_path).name
        if filename in wanted_files:
            candidates[filename].append(href)

    discovered: dict[str, str] = {}
    for filename, urls in candidates.items():
        if not urls:
            continue
        if snapshot and snapshot != "latest":
            matching = [url for url in urls if f"/{snapshot}/" in unquote(url)]
            if not matching:
                raise ValueError(f"No Inside Airbnb URL found for {filename} snapshot {snapshot}")
            discovered[filename] = matching[0]
        else:
            discovered[filename] = sorted(urls, key=_extract_snapshot)[-1]

    missing = sorted(wanted_files - set(discovered))
    if missing:
        raise ValueError(
            f"Could not discover Inside Airbnb URLs for {missing}. "
            f"Check city_slug={city_slug!r} and page={page_url!r}."
        )
    return discovered


def download_inside_airbnb(cfg: dict) -> dict:
    paths = standard_paths(cfg)
    urls = discover_inside_airbnb_urls(cfg)
    snapshot = _extract_snapshot(next(iter(urls.values())))
    dest_dir = paths["inside_airbnb_dir"] / snapshot
    downloaded = []
    for filename, url in urls.items():
        dest = dest_dir / filename
        if dest.exists() and dest.stat().st_size > 0:
            downloaded.append(
                DownloadedFile(
                    filename=filename,
                    url=url,
                    path=str(dest),
                    sha256=file_sha256(dest),
                    bytes=dest.stat().st_size,
                )
            )
            continue
        downloaded.append(download_file(url, dest))

    manifest = {
        "source": "Inside Airbnb",
        "city": cfg_get(cfg, "data.target_city"),
        "snapshot": snapshot,
        "files": [item.__dict__ for item in downloaded],
    }
    write_json(manifest, dest_dir / "manifest.json")
    write_json(manifest, paths["reports_dir"] / "inside_airbnb_manifest.json")
    return manifest


def download_fasttext_lid(cfg: dict) -> dict:
    paths = standard_paths(cfg)
    dest = paths["language_model_dir"] / "lid.176.bin"
    if dest.exists() and dest.stat().st_size > 0:
        item = DownloadedFile(
            filename=dest.name,
            url=FASTTEXT_LID_URL,
            path=str(dest),
            sha256=file_sha256(dest),
            bytes=dest.stat().st_size,
        )
    else:
        item = download_file(FASTTEXT_LID_URL, dest)
    manifest = {"source": "fastText language identification", "files": [item.__dict__]}
    write_json(manifest, paths["reports_dir"] / "fasttext_manifest.json")
    return manifest
