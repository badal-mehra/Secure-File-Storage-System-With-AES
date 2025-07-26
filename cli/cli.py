import typer
import requests
import os
import json

app = typer.Typer()
CONFIG_PATH = os.path.expanduser("~/.secureai_drive_config.json")

def save_token(token: str):
    config = {"token": token}
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)

def load_token() -> str:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f).get("token")
    return None

@app.command()
def login(username: str, password: str):
    response = requests.post("http://localhost:8000/token", data={"username": username, "password": password})
    if response.status_code == 200:
        token = response.json()["access_token"]
        save_token(token)
        typer.echo("Login successful")
    else:
        typer.echo("Login failed")

@app.command()
def upload(filepath: str):
    if not os.path.exists(filepath):
        typer.echo("File not found")
        return
    token = load_token()
    if not token:
        typer.echo("Please login first")
        return
    with open(filepath, "rb") as f:
        response = requests.post(
            "http://localhost:8000/upload",
            files={"file": f},
            headers={"Authorization": f"Bearer {token}"}
        )
    typer.echo(response.json())

@app.command()
def download(filename: str):
    token = load_token()
    if not token:
        typer.echo("Please login first")
        return
    response = requests.get(
        f"http://localhost:8000/download/{filename}",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        typer.echo(f"File {filename} downloaded successfully")
    else:
        typer.echo("Download failed")

@app.command()
def list_files():
    token = load_token()
    if not token:
        typer.echo("Please login first")
        return
    response = requests.get("http://localhost:8000/files", headers={"Authorization": f"Bearer {token}"})
    for file in response.json():
        typer.echo(f"Filename: {file['filename']}, Tags: {file['tags']}, Uploaded: {file['uploaded_at']}")

if __name__ == "__main__":
    app()
