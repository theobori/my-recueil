#!/usr/bin/env python3

import sys
import subprocess

from pathlib import Path


def transform_image(path: Path) -> None:
    """Compress, strip metadata and optimize an image from a given path.

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


if __name__ == "__main__":
    paths_str = sys.argv[1:]

    for path_str in paths_str:
        path = Path(path_str).absolute()

        try:
            transform_image(path)
        except subprocess.CalledProcessError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
        except ValueError as e:
            print(e, file=sys.stderr)
            continue
