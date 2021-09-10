import click


@click.group()
@click.option('-p','--password', required=True, help="GEMMA password")
@click.option('-u','--username', required=True, help="GEMMA username")
def cli():
    pass

@cli.command()
def test():
    print("worked")


if __name__ == "__main__":
    cli()