from pathlib import Path
from rich import print
from fastapi_create.utils import (
    create_file,
    generate_base_path,
    generate_secret_key,
    add_key_value_to_env_file,
)

PROJECT_STRUCTURE = {
    "": [".env", "README.md", "requirements.txt", "manage.py"],
    "app": ["__init__.py", "main.py"],
    "app/core": ["__init__.py", "config.py", "dependencies.py"],
    "app/core/utils": ["__init__.py", "security.py", "messages.py", "validators.py"],
    "app/db": ["config.py", "init_db.py", "models.py"],
    "app/schemas": ["__init__.py"],
    "app/routes": ["__init__.py"],
}


def create_skeleton(path_prefix: str | None = None) -> Path:
    """
    Create the FastAPI project skeleton.

    This function generates the base directory structure for a FastAPI project,
    creates necessary files, and adds a secret key to the .env file.

    Args:
        path_prefix (str | None): Optional prefix for the base path where the project skeleton will be created.

    Returns:
        Path: The path to the created project skeleton.
    """
    base_path = generate_base_path(path_prefix)
    secret_key = generate_secret_key()
    print("[yellow]Creating project skeleton...[/yellow]")
    for dir_path, files in PROJECT_STRUCTURE.items():
        directory = base_path / dir_path
        directory.mkdir(parents=True, exist_ok=True)
        for file_name in files:
            create_file(directory / file_name, "")
    add_key_value_to_env_file(base_path / ".env", "SECRET_KEY", secret_key)
    print(f"[green]Created project skeleton at {base_path.resolve()}[/green]")
    return base_path


def spin_up_project(project_name: str) -> Path:
    """
    Set up the project directory and skeleton.

    Args:
        project_name (str): The name of the project directory to create.
                            If the value is ".", the current directory will be used.

    Returns:
        Path: The path to the created project directory.
    """
    msg = "current directory" if project_name == "." else f"'{project_name}'"
    print(f"[yellow]Spinning up a new project in {msg}...[/yellow]")
    return create_skeleton(project_name)
