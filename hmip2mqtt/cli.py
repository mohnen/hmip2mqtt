import json
# from pathlib import Path

import homematicip
from homematicip.home import Home
from paho.mqtt import client as mqtt_client

import typer
# from appdirs import AppDirs

app = typer.Typer()
# appdirs = AppDirs("hmip2mqtt", "")

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


        broker = 'house.mohnen.net'
        port = 1883
        client_id = 'homematicip'

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

        home.get_current_state()
        for group in home.groups:
            if group.groupType=="META":
                typer.echo(group)
                for device in group.devices:
                    pass#typer.echo(json.dumps(device._rawJSONData))

def main():
  app()
