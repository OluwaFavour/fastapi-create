from pathlib import Path
from rich import print
from fastapi_create.utils import generate_file_content, write_file


def generate_manage_code() -> str:
    """
    Generate manage code from a template.

    This function prints a message indicating that the manage code is being generated,
    and then it generates the content of the manage code file using a Jinja2 template.

    Returns:
        str: The generated manage code content.
    """
    print("[yellow]Generating manage code...[/yellow]")
    return generate_file_content("manage_template.py.jinja2")


def configure_manage_in_project(base_path: Path) -> None:
    """
    Configure the manage.py file in the given project directory.

    This function generates the manage.py file content and writes it to the specified
    base path directory. It prints status messages indicating the progress of the operation.

    Args:
        base_path (Path): The base directory path where the manage.py file will be created.

    Returns:
        None
    """
    manage_path = base_path / "manage.py"
    print("[yellow]Writing manage.py to the project...[/yellow]")
    write_file(manage_path, generate_manage_code())
    print("[green]manage.py written successfully[/green]")
