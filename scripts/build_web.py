import os
import subprocess
import sys
import tempfile
from pathlib import Path

deps_dir = Path(tempfile.gettempdir()) / "car_game_pygbag_deps"

subprocess.check_call([
    sys.executable,
    "-m",
    "pip",
    "install",
    "--target",
    str(deps_dir),
    "pygbag",
])

env = os.environ.copy()
existing_pythonpath = env.get("PYTHONPATH", "")
env["PYTHONPATH"] = str(deps_dir) if not existing_pythonpath else f"{deps_dir}{os.pathsep}{existing_pythonpath}"

subprocess.check_call([
    sys.executable,
    "-m",
    "pygbag",
    "--build",
    "--disable-sound-format-error",
    "--ume_block",
    "0",
    "--width",
    "480",
    "--height",
    "640",
    "--title",
    "Car Mini Game",
    "--icon",
    "favicon.png",
    ".",
], env=env)

subprocess.check_call([sys.executable, "scripts/postbuild.py"])
