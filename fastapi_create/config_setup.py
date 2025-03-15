from pathlib import Path
from rich import print
from fastapi_create.utils import generate_file_content, write_file


def generate_core_config_code(smtp_enabled: bool, cors_enabled: bool) -> str:
    """
    Generate core configuration code from a template.

    This function prints a message indicating that the core configuration code
    is being generated, and then it generates the content of the core
    configuration file using a Jinja2 template.

    Args:
        smtp_enabled (bool): Whether SMTP settings are enabled in the configuration.
                                If True, the configuration will include SMTP settings
                                for sending emails.
        cors_enabled (bool): Whether CORS settings are enabled in the configuration.
                                If True, the configuration will include CORS settings.

    Returns:
        str: The generated core configuration code as a string.
    """
    print("[yellow]Generating core config code...[/yellow]")
    return generate_file_content(
        "core_config_template.py.jinja2",
        smtp_enabled=smtp_enabled,
        cors_enabled=cors_enabled,
    )


def configure_core_config_in_project(
    base_path: Path, cors_enabled: bool = True, smtp_enabled: bool = True
) -> None:
    """
    Write core configuration to the project.

    This function generates the core configuration code and writes it to the
    appropriate file within the project directory structure.

    Args:
        base_path (Path): The base path of the project where the core configuration
                          file will be created.
        cors_enabled (bool): Whether CORS settings are enabled in the configuration.
                             If True, the configuration will include CORS settings.
                             Defaults to True.
        smtp_enabled (bool): Whether SMTP settings are enabled in the configuration.
                                If True, the configuration will include SMTP settings
                                for sending emails. Defaults to True.

    Returns:
        None
    """
    config_path = base_path / "app" / "core" / "config.py"
    print("[yellow]Writing core config to the project...[/yellow]")
    write_file(config_path, generate_core_config_code(smtp_enabled, cors_enabled))
    print("[green]Core config written successfully[/green]")
