from pathlib import Path
from rich import print
from fastapi_create.utils import generate_file_content, write_file


def generate_core_utils_security_code(
    verification_enabled: bool,
    auth_system: str,
) -> str:
    """
    Generate core security utilities code from a template.

    This function prints a message indicating that the core security utilities
    code is being generated, and then it generates the content of the core security
    utilities file using a Jinja2 template.

    Args:
        verification_enabled (bool): Whether email verification is enabled.
        auth_system (str): The authentication system being used.

    Returns:
        str: The generated core security utilities code as a string.
    """
    print("[yellow]Generating core security utilities code...[/yellow]")
    return generate_file_content(
        "core_security_template.py.jinja2",
        verification_enabled=verification_enabled,
        auth_system=auth_system,
    )


def configure_core_utils_security_in_project(
    base_path: Path,
    verification_enabled: bool,
    auth_system: str,
):
    """
    Configure core security utilities in the project.

    This function generates the core security utilities code and writes it to a file
    in the project directory.

    Args:
        base_path (Path): The base path of the project directory.
        verification_enabled (bool): Whether email verification is enabled.
        auth_system (str): The authentication system being used.
    """
    core_utils_security_path = base_path / "app" / "core" / "utils" / "security.py"
    print(
        f"[yellow]Configuring core security utilities in {core_utils_security_path}...[/yellow]"
    )
    write_file(
        core_utils_security_path,
        generate_core_utils_security_code(
            verification_enabled=verification_enabled,
            auth_system=auth_system,
        ),
    )
    print("[green]Core security utilities configured successfully![/green]")
