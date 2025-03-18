from pathlib import Path
from rich import print
from fastapi_create.utils import generate_file_content, write_file


def generate_core_dependencies_code(
    is_async: bool,
    auth_model: str,
    auth_system: str,
    auth_enabled: bool,
    smtp_enabled: bool,
    verification_enabled: bool,
) -> str:
    """
    Generate core dependencies code from a template.

    This function prints a message indicating that the core dependencies code
    is being generated, and then it generates the content of the core
    dependencies file using a Jinja2 template.

    Args:
        is_async (bool): Whether the application is using asynchronous dependencies.
                         If True, the dependencies will be asynchronous.
        auth_model (str): The authentication model to be used in the application.
        auth_system (str): The authentication system to be used in the application.
        auth_enabled (bool): Whether authentication is enabled.
        smtp_enabled (bool): Whether the application is using SMTP for sending emails.
        verification_enabled (bool): Whether email verification is enabled.

    Returns:
        str: The generated core dependencies code as a string.
    """
    print("[yellow]Generating core dependencies code...[/yellow]")
    return generate_file_content(
        "core_dependencies_template.py.jinja2",
        is_async=is_async,
        auth_model=auth_model,
        auth_system=auth_system,
        smtp_enabled=smtp_enabled,
        verification_enabled=verification_enabled,
        auth_enabled=auth_enabled,
    )


def configure_core_dependencies_in_project(
    base_path: Path,
    is_async: bool,
    auth_model: str,
    auth_system: str,
    auth_enabled: bool,
    smtp_enabled: bool,
    verification_enabled: bool,
) -> None:
    """
    Write core dependencies to the project.

    This function generates the core dependencies code and writes it to the
    appropriate file within the project directory structure.

    Args:
        base_path (Path): The base path of the project where the core dependencies
                          file will be created.
        is_async (bool): Whether the application is using asynchronous dependencies.
                         If True, the dependencies will be asynchronous. Defaults to True.
        auth_model (str): The authentication model to be used in the application.
        auth_system (str): The authentication system to be used in the application.
        auth_enabled (bool): Whether authentication is enabled.
        smtp_enabled (bool): Whether the application is using SMTP for sending emails.
        verification_enabled (bool): Whether email verification is enabled.
    Returns:
        None
    """
    dependencies_path = base_path / "app" / "core" / "dependencies.py"
    print("[yellow]Writing core dependencies to the project...[/yellow]")
    write_file(
        dependencies_path,
        generate_core_dependencies_code(
            is_async,
            auth_model,
            auth_system,
            auth_enabled,
            smtp_enabled,
            verification_enabled,
        ),
    )
    print("[green]Core dependencies written successfully[/green]")
