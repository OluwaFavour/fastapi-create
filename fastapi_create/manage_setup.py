from pathlib import Path
from rich import print
from fastapi_create.utils import generate_file_content, write_file


def generate_manage_code() -> str:
    """Generate manage code from a template."""
    print("[yellow]Generating manage code...[/yellow]")
    return generate_file_content("manage_template.py.jinja2")


def configure_manage_in_project(base_path: Path) -> None:
    """Configure manage.py in the project."""
    manage_path = base_path / "manage.py"
    print("[yellow]Writing manage.py to the project...[/yellow]")
    write_file(manage_path, generate_manage_code())
    print("[green]manage.py written successfully[/green]")
