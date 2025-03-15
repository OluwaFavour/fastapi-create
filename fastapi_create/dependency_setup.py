from pathlib import Path
import subprocess
import typer
from rich import print
from fastapi_create.constants import DEPENDENCIES
from fastapi_create.requirements_setup import generate_requirements_txt


def install_dependencies(
    base_path: Path, db_thread_type: str, db_dependency: str | None = None
) -> None:
    """Install project dependencies based on database thread type."""
    dependencies = DEPENDENCIES.copy()
    if db_thread_type == "async":
        dependencies.append("sqlalchemy[asyncio]")
    else:
        dependencies.append("sqlalchemy")
    if db_dependency:
        dependencies.append(db_dependency)
    print("[yellow]Installing project dependencies...[/yellow]")
    for dependency in dependencies:
        try:
            subprocess.run(["pip", "install", dependency], check=True)
        except subprocess.CalledProcessError:
            print(f"[red]Error installing {dependency}[/red]", file="stderr")
            raise RuntimeError(f"Error installing {dependency}")
    print("[green]Dependencies installed successfully[/green]")
    generate_requirements_txt(base_path)
