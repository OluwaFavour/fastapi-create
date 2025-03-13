import subprocess
from typing import Annotated

from rich import print
import typer

from app.core.config import get_settings

app = typer.Typer()


@app.command()
def makemigrations(comment: Annotated[str, typer.Argument()] = "auto"):
    """
    Make Alembic migrations
    """
    try:
        revision_command = f"alembic revision --autogenerate -m {comment}"
        print(f"Running Alembic migrations: {revision_command}")
        subprocess.run(revision_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[red]Error:[/red] {e}")
        return
    print("[green]Make migrations complete[/green]")


@app.command()
def migrate():
    """
    Run Alembic migrations
    """
    try:
        upgrade_command = "alembic upgrade head"
        print(f"Running Alembic upgrade: {upgrade_command}")
        subprocess.run(upgrade_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[red]Error:[/red] {e}")
        return
    print("[green]Migration complete[/green]")


@app.command()
def runserver():
    """
    Run the FastAPI server
    """
    try:
        server_command = (
            f"fastapi dev app/main.py"
            if get_settings().debug
            else f"fastapi run app/main.py"
        )
        print(f"Running FastAPI server: {server_command}")
        subprocess.run(server_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[red]Error:[/red] {e}")
        return


@app.callback()
def main(ctx: typer.Context):
    print(f"Executing the command: {ctx.invoked_subcommand}")


if __name__ == "__main__":
    app()