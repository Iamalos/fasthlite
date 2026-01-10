import re
import json
import argparse

def update_notebook(nb_path, py_path, new_nb=None):
    """Update notebook cells with content from .py file
    
    Args:
        nb_path: Path to .ipynb notebook file
        py_path: Path to .py file
        new_nb: Output path (if None, updates in place)
    """
    with open(py_path, 'r') as f: py_content = f.read()
    parsed = parse_py_cells(py_content)
    with open(nb_path, 'r') as f: nb = json.load(f)
    
    for cell_idx, new_content in parsed.items():
        if cell_idx == 0: continue
        if cell_idx >= len(nb['cells']):
            raise IndexError(f"Cell index {cell_idx} not found in notebook (has {len(nb['cells'])} cells)")
        nb['cells'][cell_idx]['source'] = ('#| export\n' + new_content.strip()).splitlines(keepends=True)
    
    output_path = new_nb if new_nb is not None else nb_path
    with open(output_path, 'w') as f: json.dump(nb, f, indent=1)

def main():
    parser = argparse.ArgumentParser(description='Sync nbdev .py file changes back to .ipynb notebook')
    parser.add_argument('notebook', help='Path to .ipynb notebook file')
    parser.add_argument('pyfile', help='Path to .py file')
    parser.add_argument('-o', '--output', help='Output notebook path (default: overwrites input)', default=None)
    
    args = parser.parse_args()
    
    update_notebook(args.notebook, args.pyfile, args.output)
    output = args.output or args.notebook
    print(f"✅ Updated {output}")

if __name__ == '__main__':
    main()