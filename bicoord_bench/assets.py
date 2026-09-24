"""Download the simulation assets for an installed ``bicoord_bench``.

    python -m bicoord_bench.assets [DATA_DIR]
"""

from __future__ import annotations

import os
import sys
import zipfile
from pathlib import Path

from huggingface_hub import hf_hub_download

DEFAULT_DATA_DIR = Path("~/.cache/bicoord-bench").expanduser()

# (dataset repo, zip, where it unpacks under assets/). BiCoord's objects.zip
# holds extra object folders at its top level, so it goes inside objects/.
ZIPS = [
    ("TianxingChen/RoboTwin2.0", "embodiments.zip", "."),
    ("TianxingChen/RoboTwin2.0", "objects.zip", "."),
    ("GradiusTwinbee/BiCoord", "objects.zip", "objects"),
]


def ensure(data_dir: str | os.PathLike | None = None) -> Path:
    """Download whatever assets are missing into ``data_dir`` (default
    ``$BICOORD_DATA``, else ``~/.cache/bicoord-bench``), fill in the embodiment
    configs' paths, set ``$BICOORD_DATA`` to it and return it."""
    data = Path(data_dir or os.environ.get("BICOORD_DATA") or DEFAULT_DATA_DIR)
    assets = data.expanduser().resolve() / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    for repo, name, dest in ZIPS:
        done = assets / f".{repo.replace('/', '_')}_{name}.done"
        if not done.exists():
            print(f"Downloading {repo}/{name} into {assets}", file=sys.stderr)
            with zipfile.ZipFile(hf_hub_download(repo, name, repo_type="dataset")) as z:
                z.extractall(assets / dest)
            done.touch()
    # What upstream's script/update_embodiment_config_path.py does.
    for template in (assets / "embodiments").rglob("*_tmp.yml"):
        text = template.read_text().replace("${ASSETS_PATH}", str(assets.parent))
        text = text.replace("$ASSETS_PATH", str(assets.parent))
        template.with_name(template.name.replace("_tmp.yml", ".yml")).write_text(text)
    os.environ["BICOORD_DATA"] = str(assets.parent)
    return assets.parent


if __name__ == "__main__":
    print(ensure(sys.argv[1] if len(sys.argv) > 1 else None))
