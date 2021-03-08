import os
import json
import time

from pathlib import Path

from getmac import get_mac_address

import homematicip
from homematicip.home import Home
from paho.mqtt import client as mqtt_client

import typer
from appdirs import AppDirs

app = typer.Typer()

config_path = (Path(AppDirs("hmip2mqtt", "").user_config_dir))
config_file_path = config_path / "config.ini"
config_path.mkdir(parents=True, exist_ok=True)
os.chdir(config_path)

@app.command("run")
def run(broker: str):
    port = 1883
    client_id = f'homematicip_{"".join(get_mac_address().split(":")).upper()}'
    teleperiod = 60
    prefix = 'hmip_'

    if not config_file_path.exists():
        typer.echo("No configuration found", err=True)
        os.system('hmip_generate_auth_token.py')

    typer.echo(f"Loading {config_file_path}")
    config = homematicip.load_config_file(config_file_path)

    if config is None:
        typer.echo("No configuration found", err=True)
        raise typer.Exit(code=1)

    home = Home()
    home.set_auth_token(config.auth_token)
    home.init(config.access_point)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to {broker}:{port} as {client_id}")
        else:
            typer.echo(f"Failed to connect, return code {rc}", err=True)
            raise typer.Exit(code=1)
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)

    client.on_connect = on_connect
    try:
        client.connect(broker, port)
    except:
        typer.echo(f"Failed to connect to {broker}:{port}", err=True)
        raise typer.Exit(code=1)

    client.loop_start()

    while True:
        try:
            home.get_current_state()
            for group in home.groups:
                if group.groupType=="META":
                    for device in group.devices:
                        label = '_'.join(device.label.split()).encode("ascii", "ignore").decode()
                        topic1 = f"tele/{prefix}{label}/STATE"
                        typer.echo(topic1)
                        # typer.echo(json.dumps(device._rawJSONData))
            time.sleep(teleperiod)
        except KeyboardInterrupt:
            typer.echo('Stopping')
            break

def main():
  app()
