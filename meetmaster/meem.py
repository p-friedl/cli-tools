import click


@click.group()
def cli():
    pass


@cli.command()
def test1():
    click.echo('Initialized the database')


@cli.command()
def test2():
    click.echo('Dropped the database')


@cli.command()
@click.option('--count', default=1, help='number of greetings')
@click.argument('name')
def hello(count, name):
    for x in range(count):
        click.echo('Hello %s!' % name)


if __name__ == '__main__':
    cli()
