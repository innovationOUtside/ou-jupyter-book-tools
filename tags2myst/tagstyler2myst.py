import nbformat
from pathlib import Path


# NOTE: The admonition styling is defined via:
# https://sphinx-book-theme.readthedocs.io/en/latest/reference/demo.html#admonitions
# danger, success, warning

# Sphinx:
# Yellow: attention (! in circle), caution (! in triangle), warning (! in triangle)
# danger, error, hint, important, warning, note

# Custom: admonition
def tagstyler2myst(path, overwrite=False, remove=True):
    """Map tagstyler tagged cells onto myst equivalent."""

    # Parse notebooks
    nb_dir = Path(path)
    tag_set = ['alert-danger', 'alert-success', 'alert-warning', 'alert-info']
    for p in nb_dir.iterdir():
        if p.is_file() and p.suffix == '.ipynb' and not p.name.endswith('__myst.ipynb'):
            # Read notebook
            with p.open('r') as f:
                nb = nbformat.read(f, nbformat.NO_CONVERT)
                updates = False
                # Enumerate through cells
                for i, cell in enumerate(nb['cells']):

                    #For each markdown cell
                    if cell['cell_type']=='markdown' and 'tags' in nb['cells'][i]["metadata"]:
                        # We'll capture tags per cell
                        tags = nb['cells'][i]["metadata"]['tags']
                        source = nb['cells'][i]['source']
                        # we can also use note for blue
                        if 'alert-success' in tags:
                            nb['cells'][i]['source'] = f":::{{admonition}} Note\n:class: tip\n{source}\n:::"
                            updates = True
                        elif 'alert-warning' in tags:
                            nb['cells'][i]['source'] = f":::{{admonition}} Note\n:class: attention\n{source}\n:::"
                            updates = True
                        elif 'alert-danger' in tags:
                            nb['cells'][i]['source'] = f":::{{admonition}} Note\n:class: danger\n{source}\n:::"
                            updates = True
                        elif 'alert-info' in tags:
                            nb['cells'][i]['source'] = f":::{{admonition}} Note\n:class: tip\n{source}\n:::"
                            updates = True

                        if remove:
                            for t in tag_set:
                                # Clear cell output if no report
                                nb['cells'][i]["tags"] = nb['cells'][i]["tags"].remove(t)

            if updates:
                # Create output filename
                out_path =  p if overwrite else p.with_name(f'{p.stem}__myst{p.suffix}') 
        
                # Write out annotated notebook
                nbformat.write(nb, out_path.open('w'), nbformat.NO_CONVERT)