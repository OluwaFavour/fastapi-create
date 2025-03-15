from pathlib import Path
from typing import Any
from rich.prompt import Prompt, Confirm
from fastapi_create.constants import (
    SMTP_HOST_REGEX,
    SMTP_PORT_REGEX,
    SMTP_USERNAME_REGEX,
)
from fastapi_create.utils import (
    generate_file_content,
    recursive_prompt_with_validation,
    add_key_value_to_env_file,
    write_file,
)


def validate_smtp_host(host: str) -> bool:
    """
    Validates the given SMTP host string against a predefined regular expression.

    Args:
        host (str): The SMTP host string to validate.

    Returns:
        bool: True if the host string matches the regular expression, False otherwise.
    """
    return bool(SMTP_HOST_REGEX.match(host))


def validate_smtp_port(port: str) -> bool:
    """
    Validate if the given SMTP port is within the valid range and matches the expected format.

    Args:
        port (str): The SMTP port as a string.

    Returns:
        bool: True if the port is valid, False otherwise.
    """
    if not SMTP_PORT_REGEX.match(port):
        return False
    return 1 <= int(port) <= 65535


def validate_smtp_username(username: str) -> bool:
    """
    Validate the given SMTP username against a predefined regex pattern.

    Args:
        username (str): The SMTP username to validate.

    Returns:
        bool: True if the username matches the regex pattern, False otherwise.
    """
    return bool(SMTP_USERNAME_REGEX.match(username))


def smtp_settings_prompt() -> tuple[bool, dict[str, Any] | None]:
    """
    Prompts the user to enter SMTP settings and returns them as a dictionary.

    The function will recursively prompt the user for the SMTP host, port,
    username, and password. It validates the host, port, and username using
    the respective validation functions.

    Returns:
        bool | tuple[bool, dict[str, Any]]: A tuple containing a boolean value
        indicating whether SMTP is enabled and a dictionary containing the SMTP
        settings with the following keys:
            - "smtp_host" (str): The SMTP host.
            - "smtp_port" (int): The SMTP port.
            - "smtp_login" (str): The SMTP username.
            - "smtp_password" (str): The SMTP password.
    """
    smtp_enabled = Confirm.ask("Do you need SMTP setup?", default=True)
    if not smtp_enabled:
        return False, None
    smtp_host = recursive_prompt_with_validation(
        prompt="Enter SMTP host (e.g., smtp.gmail.com)",
        validation_func=validate_smtp_host,
        error_msg="Error: Invalid SMTP host",
    )
    smtp_port = recursive_prompt_with_validation(
        prompt="Enter SMTP port (e.g., 587)",
        validation_func=validate_smtp_port,
        error_msg="Error: Invalid SMTP port",
        prompt_kwargs={"default": "587"},
    )
    smtp_username = Prompt.ask("Enter SMTP username")
    smtp_password = Prompt.ask("Enter SMTP password", password=True)
    return True, {
        "smtp_host": smtp_host,
        "smtp_port": int(smtp_port),
        "smtp_login": smtp_username,
        "smtp_password": smtp_password,
    }


def configure_smtp_settings(base_path: Path) -> bool:
    """
    Configure SMTP settings by prompting the user to enter the required details.

    The function prompts the user to enter the SMTP host, port, username, and password.
    It then adds these settings to the .env file using the add_key_value_to_env_file function.

    Args:
        base_path (Path): The base path of the project where the .env file is located.

    Returns:
        bool: A boolean indicating whether SMTP is enabled.
    """
    smtp_enabled, smtp_settings = smtp_settings_prompt()
    if not smtp_enabled:
        return smtp_enabled
    add_key_value_to_env_file(
        base_path / ".env", "SMTP_HOST", smtp_settings["smtp_host"]
    )
    add_key_value_to_env_file(
        base_path / ".env", "SMTP_PORT", str(smtp_settings["smtp_port"])
    )
    add_key_value_to_env_file(
        base_path / ".env", "SMTP_LOGIN", smtp_settings["smtp_login"]
    )
    add_key_value_to_env_file(
        base_path / ".env", "SMTP_PASSWORD", smtp_settings["smtp_password"]
    )
    print("[green]SMTP settings configured successfully![/green]")
    return smtp_enabled


def generate_core_messages_code(is_async: bool) -> str:
    """
    Generate core messages code from a template.

    This function prints a message indicating that the core messages code
    is being generated, and then it generates the content of the core
    messages file using a Jinja2 template.

    Returns:
        str: The generated core messages code as a string.
    """
    print("[yellow]Generating core messages code...[/yellow]")
    return generate_file_content("core_messages_template.py.jinja2", is_async=is_async)


def configure_core_messages_in_project(base_path: Path, is_async: bool = True) -> None:
    """
    Write core messages to the project.

    This function generates the core messages code and writes it to the
    appropriate file within the project directory structure.

    Args:
        base_path (Path): The base path of the project where the core messages
                          file will be created.
        is_async (bool): Whether the application is using asynchronous messages.
                         If True, the messages will be asynchronous. Defaults to True.

    Returns:
        None
    """
    messages_path = base_path / "app" / "core" / "messages.py"
    print("[yellow]Writing core messages to the project...[/yellow]")
    write_file(messages_path, generate_core_messages_code(is_async))
    print("[green]Core messages written successfully[/green]")
