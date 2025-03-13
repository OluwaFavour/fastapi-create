from pathlib import Path
from rich import print
from utils import create_file, generate_secret_key, add_key_value_to_env_file

PROJECT_STRUCTURE = {
    "": [".env"],
    "app": ["__init__.py", "main.py"],
    "app/core": ["__init__.py", "config.py"],
    "app/db": [],
    "app/schemas": ["__init__.py"],
    "app/routes": ["__init__.py"],
}


def create_skeleton(path_prefix: str | None = None) -> Path:
    """Create the FastAPI project skeleton."""
    base_path = Path.cwd() if path_prefix == "." else Path(path_prefix or "")
    if not base_path.is_absolute():
        base_path = Path.cwd() / base_path
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
    """Set up the project directory and skeleton."""
    msg = "current directory" if project_name == "." else f"'{project_name}'"
    print(f"[yellow]Spinning up a new project in {msg}...[/yellow]")
    return create_skeleton(project_name)
