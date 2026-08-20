import zipfile
import requests
from loguru import logger
from pathlib import Path
from rich.progress import (
    Progress,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    TextColumn,
)

WESAD_URL = "https://uni-siegen.sciebo.de/public.php/dav/files/HGdUkoNlW1Ub0Gx"
STORAGE_PATH = "file.zip"
EXTRACT_PATH = "data/"

CHUNK_SIZE = 1024 * 1024  # =1MB


def download(url: str, destination: Path) -> None:
    """Download a zip file from `url` and save as `destination` with progress bar"""

    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()

        # get total size
        total_size = int(response.headers.get("content-length", 0))

        # build progress bar
        with Progress(
            TextColumn("[bold]Downloading"),
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task("download", total=total_size or None)

            # NOTE: write to file
            with destination.open("wb") as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
                        progress.update(task, advance=len(chunk))


def extract(zip_path: Path, destination: Path) -> None:
    """Extract a zip file at `zip_path` to `destination` with visualized progress"""

    with zipfile.ZipFile(zip_path, "r") as archive:
        members = archive.infolist()
        total_size = sum(m.file_size for m in members if not m.is_dir())

        with Progress(
            TextColumn("[bold]Extracting"),
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task("extract", total=total_size)

            for member in members:
                output_path = destination / member.filename

                if member.is_dir():
                    output_path.mkdir(parents=True, exist_ok=True)
                    continue

                output_path.parent.mkdir(parents=True, exist_ok=True)

                with archive.open(member, "r") as src:
                    with output_path.open("wb") as dst:
                        while chunk := src.read(CHUNK_SIZE):
                            dst.write(chunk)
                            progress.update(task, advance=len(chunk))


def main():
    zip_path = Path(STORAGE_PATH)
    extract_path = Path(EXTRACT_PATH)

    logger.info(f"WESAD Dataset URL: {WESAD_URL}")
    logger.info(f"Saving zip file to {STORAGE_PATH}")
    download(WESAD_URL, zip_path)

    logger.info(f"Extracting to {EXTRACT_PATH}")
    extract(zip_path, extract_path)

    logger.info(f"Removing temporary zip file")
    zip_path.unlink()

    logger.info("Download and extract complete!")
