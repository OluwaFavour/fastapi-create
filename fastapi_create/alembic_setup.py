from pathlib import Path
import subprocess
import typer
from rich import print
from rich.prompt import Prompt
from fastapi_create.utils import generate_file_content, write_file


def alembic_folder_name_prompt() -> str:
    """Prompt for the Alembic folder name."""
    return Prompt.ask("Enter the name of the Alembic folder", default="alembic")


def generate_alembic_env_code(db_thread_type: str) -> str:
    """Generate Alembic env.py code from a template."""
    print("[yellow]Generating Alembic env.py code...[/yellow]")
    return generate_file_content(
        "alembic_env_template.py.jinja2", is_async=db_thread_type == "async"
    )


def alembic_setup(folder_name: str, base_path: Path) -> None:
    """Initialize Alembic and configure env.py."""
    print("[yellow]Initializing Alembic...[/yellow]")
    try:
        subprocess.run(["alembic", "init", folder_name], cwd=base_path, check=True)
    except subprocess.CalledProcessError:
        print("[red]Error initializing Alembic[/red]", file="stderr")
        raise RuntimeError("Error initializing Alembic")
    print("[green]Alembic initialized successfully[/green]")
    env_path = base_path / folder_name / "env.py"
    env_code = generate_alembic_env_code(
        db_thread_type="async"
    )  # Assuming db_thread_type is passed or determined
    write_file(env_path, env_code)
    print("[green]Alembic env.py configured successfully[/green]")
