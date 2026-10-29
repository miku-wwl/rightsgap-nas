"""Local Phase 2.2 evidence utilities. No model, credential or NAS access."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'validation/results/phase2-2'
FIX = ROOT / 'validation/fixtures/phase2-2'


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')


def verify_freeze(name):
    receipt = load(FIX / 'freeze.json')
    path = FIX / name
    if sha(path) != receipt['sha256'][name]:
        raise ValueError('Frozen fixture changed: ' + name)
    return load(path)
