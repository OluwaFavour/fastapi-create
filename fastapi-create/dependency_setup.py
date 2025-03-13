import subprocess
import typer
from rich import print
from constants import DEPENDENCIES


def install_dependencies(db_thread_type: str) -> None:
    """Install project dependencies based on database thread type."""
    dependencies = DEPENDENCIES.copy()
    if db_thread_type == "async":
        dependencies.append("sqlalchemy[asyncio]")
    else:
        dependencies.append("sqlalchemy")
    for dependency in dependencies:
        print(f"[yellow]Installing dependency {dependency}...[/yellow]")
        try:
            subprocess.run(["pip", "install", dependency], check=True)
        except subprocess.CalledProcessError:
            print(f"[red]Error installing {dependency}[/red]", file="stderr")
            raise typer.Exit(code=1)
    print("[green]Dependencies installed successfully[/green]")
