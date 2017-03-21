import click
import natasha


@click.group()
def cli():
    pass

@cli.command()
def build_pipelines():
    click.echo('=> Building pipeline dictionaries ...')
    for pipeline in natasha.DEFAULT_PIPELINES:
        pipeline = pipeline()
        click.echo('Building {0}...'.format(pipeline.__class__.__name__))
        pipeline.build()

if __name__ == '__main__':
    cli()
