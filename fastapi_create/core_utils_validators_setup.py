from pathlib import Path
from rich import print
from fastapi_create.utils import generate_file_content, write_file


def generate_core_utils_validators_code() -> str:
    """
    Generate core validators code from a template.

    This function prints a message indicating that the core validators
    code is being generated, and then it generates the content of the core validators
    file using a Jinja2 template.

    Returns:
        str: The generated core validators code as a string.
    """
    print("[yellow]Generating core validators code...[/yellow]")
    return generate_file_content("core_validators_template.py.jinja2")


def configure_core_utils_validators_in_project(base_path: Path):
    """
    Configure core validators in the project.

    This function generates the core validators code and writes it to a file
    in the project directory.

    Args:
        base_path (Path): The base path of the project directory.
    """
    core_utils_validators_path = base_path / "app" / "core" / "utils" / "validators.py"
    print(
        f"[yellow]Configuring core validators in {core_utils_validators_path}...[/yellow]"
    )
    write_file(
        core_utils_validators_path,
        generate_core_utils_validators_code(),
    )
    print("[green]Core validators configured successfully![/green]")
