#!/usr/bin/env bash
set -euo pipefail

target_dir="${1:?usage: scripts/install-hugo.sh TARGET_DIR}"
version="0.105.0"

case "$(uname -s)-$(uname -m)" in
  Darwin-arm64|Darwin-x86_64)
    artifact="hugo_extended_${version}_darwin-universal.tar.gz"
    expected_sha="7d4189cefa61bb5a6d077880a1f7a6e18c5335a3ac469cc5a1e7ee7ce0512206"
    ;;
  Linux-x86_64)
    artifact="hugo_extended_${version}_linux-amd64.tar.gz"
    expected_sha="3cd7b9d2fc3812b5d0a130b1735e5894b273210d6e7c03f68facad26b2d2e8a9"
    ;;
  *)
    echo "unsupported platform: $(uname -s)-$(uname -m)" >&2
    exit 1
    ;;
esac

mkdir -p "$target_dir"
archive="$target_dir/$artifact"
url="https://github.com/gohugoio/hugo/releases/download/v${version}/${artifact}"
curl -fsSL --retry 3 --retry-all-errors -o "$archive" "$url"

if command -v sha256sum >/dev/null 2>&1; then
  actual_sha="$(sha256sum "$archive" | awk '{print $1}')"
else
  actual_sha="$(shasum -a 256 "$archive" | awk '{print $1}')"
fi

if [[ "$actual_sha" != "$expected_sha" ]]; then
  echo "Hugo checksum mismatch" >&2
  exit 1
fi

tar -xzf "$archive" -C "$target_dir" hugo
rm -f "$archive"
"$target_dir/hugo" version | grep -F "v${version}"
