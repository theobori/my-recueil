#!/usr/bin/env python3

import sys
import subprocess
import shutil

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

    result: subprocess.CompletedProcess[str]
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
            raise ValueError(f"The file extension '{ext}' is not handled.")

    print(result.stdout)

if __name__ == "__main__":
    for program in ("pngquant", "jpegoptim",):
        if shutil.which(program) is None:
            print(f"The program '{program}' does not exist.", file=sys.stderr)
            sys.exit(1)

    transformed_count = 0
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

        transformed_count += 1
        print(f"Successfully transformed '{path}'.")

    print(f"Transformed {transformed_count} images.")
