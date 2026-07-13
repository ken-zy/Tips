#!/usr/bin/env python3
import argparse
from pathlib import Path, PurePosixPath

OLD_HOST = b"jiadingyi.github.io"
NEW_ORIGIN = b"https://ken-zy.github.io/Tips/"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--generated", required=True, type=Path)
    args = parser.parse_args()

    entries = [line.strip() for line in args.manifest.read_text().splitlines() if line.strip()]
    if len(entries) != 73:
        fail(f"expected 73 legacy paths, found {len(entries)}")

    invalid = [entry for entry in entries if PurePosixPath(entry).is_absolute() or ".." in PurePosixPath(entry).parts]
    if invalid:
        fail(f"invalid manifest paths: {invalid}")

    if not (args.generated / "index.html").is_file():
        fail("generated index.html is missing")

    missing = [entry for entry in entries if not (args.generated / entry).is_file()]
    if missing:
        fail("missing legacy paths:\n" + "\n".join(missing))

    old_host_files: list[str] = []
    new_origin_found = False
    for file_path in args.generated.rglob("*"):
        if not file_path.is_file():
            continue
        data = file_path.read_bytes()
        if OLD_HOST in data:
            old_host_files.append(str(file_path.relative_to(args.generated)))
        if NEW_ORIGIN in data:
            new_origin_found = True

    if old_host_files:
        fail("old hostname remains in:\n" + "\n".join(old_host_files))
    if not new_origin_found:
        fail("new origin was not found in generated output")

    print(f"verified {len(entries)} legacy paths; old host absent; new origin present")


if __name__ == "__main__":
    main()
