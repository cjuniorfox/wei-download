# WEI Fansubs Downloader

Downloads and renames episodes from WEI Fansubs website Google Drive links.

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

Downloads files to the current directory and renames them to a clean format (e.g., My Dear Donovan S01E01.mp4).

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
docker run --rm -v "$(pwd):/data" weifansubs [URL] [--season 1] [--episode 14] 
```

## What It Does

- Scrapes episode links from WEI Fansubs pages
- Downloads video files from Google Drive
- Renames files to a normalized pattern (e.g., Title S01E01.ext)
- Normalizes formatting (removes prefixes, replaces underscores, proper casing)
