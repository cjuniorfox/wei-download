# WEI Fansubs Downloader

Downloads and renames episodes from WEI Fansubs website's Google Drive links.

## Requirements

- Python 3.8+
- Internet connection

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Direct Python

```bash
python read_urls.py
```

Downloads files to the current directory and renames them to a clean format (e.g., `My Dear Donovan S01E01.mp4`).

### Docker/Podman

Pull from GitHub Container Registry:

```bash
docker pull ghcr.io/cjuniorfox/weifansubs:latest
```

Or build locally:

```bash
docker build -t weifansubs -f Containerfile .
```

Run (downloads to current directory):

```bash
docker run --rm -v "$(pwd):/data" weifansubs
```

## What It Does

1. Scrapes episode links from WEI Fansubs pages
2. Downloads video files from Google Drive
3. Renames files to: `<Title> S01E<Episode>.<ext>`
4. Removes "WEI FANSUB - " prefix and normalizes formatting

## Configuration

Edit the `base_url` in `read_urls.py` to change the series being downloaded.
