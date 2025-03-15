from pathlib import Path
import subprocess
import typer
from rich import print
from rich.prompt import Prompt
from fastapi_create.utils import (
    generate_file_content,
    write_file,
    recursive_prompt_with_validation,
)
from fastapi_create.constants import PROJECT_NAME_REGEX


def validate_alembic_folder_name(folder_name: str) -> bool:
    """
    Validate the Alembic folder name to ensure it is a valid directory name.

    Args:
        folder_name (str): The name of the Alembic folder to validate.

    Returns:
        bool: True if the folder name is valid, False otherwise.
    """
    if not PROJECT_NAME_REGEX.match(folder_name):
        print(
            "[red]Error: Invalid Alembic folder name. Must be a valid directory name.[/red]"
        )
        return False
    return True


def alembic_folder_name_prompt() -> str:
    """
    Prompt the user to enter the name of the Alembic folder.

    Returns:
        str: The name of the Alembic folder entered by the user, or the default value "alembic" if no input is provided.
    """
    """Prompt for the Alembic folder name."""
    # return Prompt.ask("Enter the name of the Alembic folder", default="alembic")
    return recursive_prompt_with_validation(
        prompt="Enter the name of the Alembic folder",
        validation_func=validate_alembic_folder_name,
        prompt_kwargs={"default": "alembic"},
    )


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
