from pathlib import Path
from rich import print
from fastapi_create.utils import generate_file_content, write_file


def generate_readme_code(project_name: str) -> str:
    """
    Generate README code from a template.

    Args:
        project_name (str): The name of the project to be used in the README.

    Returns:
        str: The generated README content.
    """
    print("[yellow]Generating README code...[/yellow]")
    return generate_file_content("readme_template.md.jinja2", project_name=project_name)


def configure_readme_in_project(base_path: Path) -> None:
    """
    Configure the README.md file in the project.

    This function generates the content for the README.md file based on the
    project's base path name and writes it to the README.md file located at
    the specified base path.

    Args:
        base_path (Path): The base path of the project where the README.md
                          file will be created.

    Returns:
        None
    """
    readme_path = base_path / "README.md"
    print("[yellow]Writing README.md to the project...[/yellow]")
    write_file(readme_path, generate_readme_code(base_path.name))
    print("[green]README.md written successfully[/green]")
