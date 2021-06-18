import click
from .tagstyler2myst import tagstyler2myst

@click.group()
def cli():
	pass


@cli.command()
@click.argument('path', default='.', type=click.Path(exists=True))
@click.option('--overwrite/--no-overwrite', default=False, help="Overwrite original notebook cell outputs.")
@click.option('--remove/--no-remove', default=False, help="Remove mapped cell tags.")
def tagstyler(path, overwrite=False, remove=True):
	"""Map tagstyler tagged cells to myst marked up cells."""
	click.echo('Using file/directory: {}'.format(path))
	tagstyler2myst(path, overwrite, remove )