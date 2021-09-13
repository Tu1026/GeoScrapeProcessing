import click
##Builiding command line options. Cannot figure out how to modularize click options

version = 0.01
softwareName = "Post GEO Filter"

def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options

credentials_option = [click.option('-p','--password', help="GEMMA password"), 
click.option('-u','--username', required=True, help="GEMMA username")]

@click.group()
def cli():
    print(f'{softwareName} ============================================================================ version: {version} initiating')

@cli.command("process")
@add_options(credentials_option)
def process(**kwargs):
    print("placeholder")

if __name__ == "__main__":
    cli()