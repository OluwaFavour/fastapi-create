from pathlib import Path
import subprocess
import typer
from rich import print
from rich.prompt import Prompt
from utils import load_template, write_file


def alembic_folder_name_prompt() -> str:
    """Prompt for the Alembic folder name."""
    return Prompt.ask("Enter the name of the Alembic folder", default="alembic")


def generate_alembic_env_code(db_thread_type: str) -> str:
    """Generate Alembic env.py code from a template."""
    print("[yellow]Generating Alembic env.py code...[/yellow]")
    template_name = (
        f"{'sync' if db_thread_type == 'sync' else 'async'}_alembic_env_template.py"
    )
    return load_template(template_name)


def alembic_setup(folder_name: str, base_path: Path) -> None:
    """Initialize Alembic and configure env.py."""
    print("[yellow]Initializing Alembic...[/yellow]")
    try:
        subprocess.run(["alembic", "init", folder_name], cwd=base_path, check=True)
    except subprocess.CalledProcessError:
        print("[red]Error initializing Alembic[/red]", file="stderr")
        raise typer.Exit(code=1)
    print("[green]Alembic initialized successfully[/green]")
    env_path = base_path / folder_name / "env.py"
    env_code = generate_alembic_env_code(
        db_thread_type="async"
    )  # Assuming db_thread_type is passed or determined
    write_file(env_path, env_code)
    print("[green]Alembic env.py configured successfully[/green]")
