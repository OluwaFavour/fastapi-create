from pathlib import Path
from rich import print
from fastapi_create.utils import generate_file_content, write_file


def generate_core_config_code() -> str:
    """
    Generate core configuration code from a template.

    This function prints a message indicating that the core configuration code
    is being generated, and then it generates the content of the core
    configuration file using a Jinja2 template.

    Returns:
        str: The generated core configuration code as a string.
    """
    print("[yellow]Generating core config code...[/yellow]")
    return generate_file_content("core_config_template.py.jinja2")


def configure_core_config_in_project(base_path: Path) -> None:
    """
    Write core configuration to the project.

    This function generates the core configuration code and writes it to the
    appropriate file within the project directory structure.

    Args:
        base_path (Path): The base path of the project where the core configuration
                          file will be created.

    Returns:
        None
    """
    config_path = base_path / "app" / "core" / "config.py"
    print("[yellow]Writing core config to the project...[/yellow]")
    write_file(config_path, generate_core_config_code())
    print("[green]Core config written successfully[/green]")
