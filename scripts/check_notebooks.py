"""Validate notebooks; allow saved dataset previews only in the main notebook."""
from pathlib import Path
import argparse
import ast
import sys
import nbformat

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / 'Lab2_ADF_ARIMA_SARIMA.ipynb'
PREVIEW_TAG = 'dataset-preview'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-clean', action='store_true', help='Reject exercise outputs; allow tagged main-notebook dataset previews.')
    parser.add_argument('--clear-outputs', action='store_true', help='Clear exercise outputs; preserve dataset previews.')
    parser.add_argument('--clear-previews', action='store_true', help='Also clear previews; use only when intentionally removing saved data previews.')
    args = parser.parse_args()
    paths = [MAIN] + sorted(p for p in (ROOT / 'contributions').rglob('*.ipynb')
                            if not any(part.startswith('.') for part in p.relative_to(ROOT).parts))
    failures = []
    previews = 0
    for path in paths:
        try:
            notebook = nbformat.read(path, as_version=4)
            nbformat.validate(notebook)
            dirty = False
            for index, cell in enumerate(notebook.cells, start=1):
                if cell.cell_type != 'code':
                    continue
                source = cell.source
                if any(line.lstrip().startswith(('%', '!')) for line in source.splitlines()):
                    from IPython.core.inputtransformer2 import TransformerManager
                    source = TransformerManager().transform_cell(source)
                ast.parse(source, filename=f'{path.name}:cell-{index}')
                if any(output.output_type == 'error' for output in cell.outputs):
                    raise ValueError(f'Cell {index} has a saved execution error.')
                preview = path == MAIN and PREVIEW_TAG in cell.metadata.get('tags', [])
                previews += int(preview and bool(cell.outputs))
                if (args.clear_outputs or args.clear_previews) and (not preview or args.clear_previews):
                    cell.execution_count = None
                    cell.outputs = []
                if not preview:
                    dirty |= cell.execution_count is not None or bool(cell.outputs)
            if args.require_clean and dirty:
                raise ValueError('Exercise outputs are not clean; run --clear-outputs before commit.')
            if args.clear_outputs or args.clear_previews:
                notebook.metadata.pop('widgets', None)
                nbformat.write(notebook, path)
            print('PASS', path.relative_to(ROOT).as_posix())
        except Exception as exc:
            failures.append(f'{path.name}: {exc}')
    for failure in failures:
        print('FAIL', failure, file=sys.stderr)
    if failures:
        return 1
    print(f'NOTEBOOKS_OK: count={len(paths)}; schema=PASS; syntax=PASS; exercise_outputs=CLEAN; preview_cells_with_output={previews}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
