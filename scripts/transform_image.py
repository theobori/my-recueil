#!/usr/bin/env python3

import sys
import subprocess
import os

from pathlib import Path
from typing import List
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED


def transform_image(path: Path) -> None:
    """Compress, strip metadata and optimize an image from a given
    path.

    :param path: The image file path.
    :type path: Path
    :returns:

    """

    parts = str(path).split(".")
    if len(parts) < 2:
        raise ValueError(f"Missing ext on path '{path}'.")

    ext = parts[-1]
    match ext:
        case "png":
            result = subprocess.run(
                f"pngquant --verbose {path} --force --strip --ext '.png'",
                shell=True,
                capture_output=True,
                text=True,
                check=True,
            )
        case "jpg" | "jpeg":
            result = subprocess.run(
                f"jpegoptim -s {path}",
                shell=True,
                capture_output=True,
                text=True,
                check=True,
            )
        case _:
            raise ValueError(f"The file path '{path}' could not be handled.")

    print(result.stdout)

    result = subprocess.run(
        f"exiftool -overwrite_original -all= {path}",
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    )

    print(result.stdout)
    print(f"Successfully transformed the image at '{path}'")


def transform_images_from_dir(path: Path, max_workers: int = 10) -> None:
    """Recursively walk on every files in the directory and transform
    the image file if possible.

    :param path: The directory path.
    :type path: Path
    :param max_workers: The maximum amount of worker threads.
    :type max_workers: int
    :returns:

    """

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                parts = filename.split(".")
                if len(parts) < 2:
                    continue

                ext = parts[-1]
                if not ext in {"png", "jpg", "jpeg", "gif"}:
                    continue

                filepath = os.path.join(root, filename)
                future = executor.submit(transform_image, filepath)
                futures.append(future)

        for future in futures:
            try:
                future.result()
            except Exception as e:
                raise e

        wait(futures, timeout=None, return_when=ALL_COMPLETED)

    print(f"Successfully transformed the images in the directory '{path}'")


if __name__ == "__main__":
    assert len(sys.argv) > 1
    path_str = sys.argv[1]
    path = Path(path_str).absolute()

    try:
        if path.is_dir():
            transform_images_from_dir(path, 20)
        else:
            transform_image(path)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
