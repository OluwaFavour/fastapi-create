from pathlib import Path
from rich import print
from utils import load_template, write_file


def generate_manage_code() -> str:
    """Generate manage code from a template."""
    print("[yellow]Generating manage code...[/yellow]")
    return load_template("manage_template.py")


def configure_manage_in_project(base_path: Path) -> None:
    """Configure manage.py in the project."""
    manage_path = base_path / "manage.py"
    print("[yellow]Writing manage.py to the project...[/yellow]")
    write_file(manage_path, generate_manage_code())
    print("[green]manage.py written successfully[/green]")
