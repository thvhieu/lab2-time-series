"""Check hashes, schemas, row counts and monthly continuity of original CSVs."""
from pathlib import Path
from datetime import datetime
import csv
import hashlib
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    sources = json.loads((ROOT / 'data' / 'manifest.json').read_text(encoding='utf-8'))
    for name, spec in sources.items():
        path = ROOT / 'data' / name
        if hashlib.sha256(path.read_bytes()).hexdigest() != spec['sha256']:
            raise ValueError(f'{name}: source hash mismatch')
        with path.open(encoding='utf-8-sig', newline='') as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames != spec['columns']:
                raise ValueError(f'{name}: unexpected columns')
            rows = list(reader)
        if len(rows) != spec['rows']:
            raise ValueError(f'{name}: unexpected row count')
        date_col, value_col = spec['columns']
        dates = [datetime.fromisoformat(row[date_col] + ('-01' if len(row[date_col]) == 7 else '')) for row in rows]
        months = [date.year * 12 + date.month for date in dates]
        if any(date.day != 1 for date in dates) or any(b - a != 1 for a, b in zip(months, months[1:])):
            raise ValueError(f'{name}: expected unique, consecutive, ordered monthly observations')
        if not all(math.isfinite(float(row[value_col])) for row in rows):
            raise ValueError(f'{name}: nonfinite target')
        print(f'PASS {name}: rows={len(rows)}; sha256=PASS; monthly=PASS')
    print(f'DATA_OK: {len(sources)} dataset(s); source bytes preserved')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as exc:
        print('FAIL', exc, file=sys.stderr)
        raise SystemExit(1)
