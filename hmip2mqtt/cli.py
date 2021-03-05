import homematicip
from homematicip.home import Home

from pathlib import Path

import typer
from appdirs import AppDirs

app = typer.Typer()
appdirs = AppDirs("hmip2mqtt", "")

@app.command("run")
def run():
    config = homematicip.find_and_load_config_file()
    if config is None:
        typer.echo("No configuration found", err=True)
        raise typer.Exit(code=1)
    else:
        home = Home()
        home.set_auth_token(config.auth_token)
        home.init(config.access_point)
        home.get_current_state()
        for group in [group if group.groupType=="META" for group in home.groups]:
            typer.echo(group)
            # if group.groupType=="META":
            #     for device in group.devices:

def main():
  app()
