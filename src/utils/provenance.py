"""
Where a saved model comes from:
    - Fingerprint of the data it was trained on
    - Git commit of the code that trained it
"""

# Imports
import hashlib
import subprocess

import pandas as pd

from src.config.paths import ROOT


def data_fingerprint(data):
    """Short hash of the rows and columns of data: same data → same fingerprint."""
    rows = pd.util.hash_pandas_object(data, index=False).to_numpy().tobytes()
    columns = ",".join(data.columns).encode()
    return hashlib.sha256(columns + rows).hexdigest()[:16]


def code_version():
    """Git commit of the code, with '-dirty' if src/ has uncommitted changes."""
    commit = git("rev-parse", "--short", "HEAD")
    changed = git("status", "--porcelain", "--", "src")
    return commit + ("-dirty" if changed else "")


def git(*arguments):
    """Output of a git command run at the project root."""
    return subprocess.run(["git", *arguments], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
