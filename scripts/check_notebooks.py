"""Validate shared and contributor notebooks; optionally clear generated outputs."""
from pathlib import Path
import argparse
import ast
import sys
import nbformat

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-clean', action='store_true')
    parser.add_argument('--clear-outputs', action='store_true')
    args = parser.parse_args()
    paths = [ROOT / 'Lab2_ADF_ARIMA_SARIMA.ipynb']
    paths += sorted(p for p in (ROOT / 'contributions').rglob('*.ipynb')
                    if not any(part.startswith('.') for part in p.relative_to(ROOT).parts))
    failures = []
    for path in paths:
        try:
            notebook = nbformat.read(path, as_version=4)
            nbformat.validate(notebook)
            dirty = False
            for index, cell in enumerate(notebook.cells, start=1):
                if cell.cell_type != 'code':
                    continue
                # IPython magics are accepted using the same input transform as IPython.
                source = cell.source
                if any(line.lstrip().startswith(('%', '!')) for line in source.splitlines()):
                    try:
                        from IPython.core.inputtransformer2 import TransformerManager
                    except ImportError as exc:
                        raise ValueError('Dùng Python thuần hoặc cài IPython để kiểm tra cell có magic.') from exc
                    source = TransformerManager().transform_cell(source)
                ast.parse(source, filename=f'{path.name}:cell-{index}')
                dirty |= cell.execution_count is not None or bool(cell.outputs)
                if args.clear_outputs:
                    cell.execution_count = None
                    cell.outputs = []
            if args.clear_outputs:
                notebook.metadata.pop('widgets', None)
                nbformat.write(notebook, path)
                dirty = False
            if args.require_clean and dirty:
                raise ValueError('Còn output; chạy check_notebooks.py --clear-outputs trước commit.')
            print('PASS', path.relative_to(ROOT).as_posix())
        except Exception as exc:
            failures.append(f'{path.name}: {exc}')
    for failure in failures:
        print('FAIL', failure, file=sys.stderr)
    if failures:
        return 1
    print(f'NOTEBOOKS_OK: {len(paths)} notebook(s); schema=PASS; syntax=PASS; clean={args.require_clean or args.clear_outputs}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
