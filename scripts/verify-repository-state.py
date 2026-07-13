#!/usr/bin/env python3
import subprocess


FORBIDDEN_FILES = {"404.html", "index.html", "index.xml", "robots.txt", "sitemap.xml"}
FORBIDDEN_PREFIXES = ("assets/", "categories/", "page/", "post/", "tags/")
REQUIRED_PATHS = {
    ".github/workflows/hugo.yml",
    ".gitignore",
    ".gitmodules",
    "docs/migration/legacy-public-paths.txt",
    "scripts/install-hugo.sh",
    "scripts/verify-migration.py",
    "site/config.yml",
    "site/themes/PaperMod",
}


def tracked_paths() -> set[str]:
    output = subprocess.check_output(["git", "ls-files", "-z"])
    return {item.decode() for item in output.split(b"\0") if item}


def main() -> None:
    tracked = tracked_paths()
    forbidden = sorted(
        path
        for path in tracked
        if path in FORBIDDEN_FILES
        or path.startswith("._")
        or path.startswith(FORBIDDEN_PREFIXES)
    )
    missing = sorted(REQUIRED_PATHS - tracked)

    if forbidden:
        raise SystemExit("legacy root output remains tracked:\n" + "\n".join(forbidden))
    if missing:
        raise SystemExit("required migration paths are missing:\n" + "\n".join(missing))

    print("verified repository cleanup: no legacy root output tracked; migration source retained")


if __name__ == "__main__":
    main()
