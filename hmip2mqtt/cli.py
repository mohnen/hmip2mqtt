from pathlib import Path

import typer
from appdirs import AppDirs

app = typer.Typer()
appdirs = AppDirs("hmip2mqtt", "")

@app.command("run")
def run():
  typer.echo('Hello General Kenobi')

def main():
  app()
