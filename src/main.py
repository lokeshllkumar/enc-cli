import click
import os
from enc import enc_file, dec_file

@click.group()
def cli():
    pass

@cli.command()
@click.argument('input_file')
@click.argument('ouput_file')
@click.option('--password', prompts = True, hide_input = True)
@click.option('--public-key', default = 'config/settings.json')
def encrypt(input_file, output_file, password, public_key):
    enc_file(input_file, output_file, password, public_key)
    click.echo(f"{input_file} encrypted to {output_file}")

@cli.command()
@click.argument('input_file')
@click.argument('output_file')
@click.option('--private_key', default = 'config/settings.json')
def decrypt(input_file, output_file, private_key):
    dec_file(input_file, output_file, private_key)
    click.echo(f"{input_file} decrypted to {output_file}")

@cli.command()
@click.option('--role', type = click.Choice(['admin', 'user']), required = True)
def generate_keys(role):
    if role == 'admin':
        os.system("openssl genpkey -algorithm RSA -out private_key.pem")
        os.system("openssl rsa -pubout -in private_key.pem -out public_key.pem")
    else:
        click.echo("Error! Cannot generate key")

if __name__ == '__main__':
    cli()