from pathlib import Path
from rich import print
from fastapi_create.utils import generate_file_content, write_file


def generate_readme_code(project_name: str) -> str:
    """Generate README code from a template."""
    print("[yellow]Generating README code...[/yellow]")
    return generate_file_content("readme_template.md.jinja2", project_name=project_name)


def configure_readme_in_project(base_path: Path) -> None:
    """Configure README.md in the project."""
    readme_path = base_path / "README.md"
    print("[yellow]Writing README.md to the project...[/yellow]")
    write_file(readme_path, generate_readme_code(base_path.name))
    print("[green]README.md written successfully[/green]")
