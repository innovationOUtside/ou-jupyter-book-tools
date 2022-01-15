# empinken2myst
# Map nb_extension_empinken tags on to MyST structures

import nbformat
from pathlib import Path


# NOTE: The admonition styling is defined via:
# https://jupyterbook.org/content/content-blocks.html#custom-div-blocks
# Tags: commentate, activity, student, solution

# Sphinx:
# Additional styling: https://jupyterbook.org/advanced/sphinx.html#custom-assets
# Yellow: attention (! in circle), caution (! in triangle), warning (! in triangle)
# danger, error, hint, important, warning, note

# Custom: admonition
def empinken2myst(path, overwrite=False, remove=True):
    """Map tagstyler tagged cells onto myst equivalent."""

    # Parse notebooks
    # TO DO - this just applies to markdown cells
    # Cell tags for code cells are automatically mapped over with class tag_X
    nb_dir = Path(path)
    tag_set = ['style_commentate', 'style_activity', 'style_student', 'style_solution']
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
                        # Tags in empinken tags
                        # We should have only one... However...?!
                        match_tags = [f'tag_{t}' for t in set(tag_set).intersection(tags)]
                        if len(match_tags):
                            nb['cells'][i]['source'] = f"```{{div}} {' '.join(match_tags)}\n{source}\n```"
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