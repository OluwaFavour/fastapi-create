from pathlib import Path
import subprocess
import typer
from rich import print
from fastapi_create.constants import DEPENDENCIES
from fastapi_create.requirements_setup import generate_requirements_txt


def install_dependencies(
    base_path: Path,
    is_async: bool,
    db_dependency: str | None = None,
    auth_system: str | None = None,
) -> None:
    """
    Install project dependencies based on database thread type.

    Args:
        base_path (Path): The base path where the requirements.txt file will be generated.
        is_async (bool): Whether the application is using asynchronous dependencies.
        db_dependency (str | None, optional): An additional database dependency to install. Defaults to None.

    Raises:
        RuntimeError: If there is an error installing any of the dependencies.
    """
    dependencies = DEPENDENCIES.copy()
    if is_async:
        dependencies.extend(["sqlalchemy[asyncio]", "aiosmtplib"])
    else:
        dependencies.append("sqlalchemy")
    if db_dependency:
        dependencies.append(db_dependency)
    if auth_system:
        if auth_system == "jwt":
            dependencies.append("pyjwt")
    print("[yellow]Installing project dependencies...[/yellow]")
    for dependency in dependencies:
        try:
            subprocess.run(["pip", "install", dependency], check=True)
        except subprocess.CalledProcessError:
            print(f"[red]Error installing {dependency}[/red]", file="stderr")
            raise RuntimeError(f"Error installing {dependency}")
    print("[green]Dependencies installed successfully[/green]")
    generate_requirements_txt(base_path)
