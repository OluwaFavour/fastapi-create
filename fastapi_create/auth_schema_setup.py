from pathlib import Path
from rich import print
from fastapi_create.utils import generate_file_content, write_file, get_plural_name


def generate_auth_schema_code(
    auth_model: str,
    auth_system: str,
    login_field: str,
    email_is_required: bool,
    phone_is_required: bool,
    username_is_required: bool,
    verification_enabled: bool,
) -> str:
    """
    Generate authentication schema code from a template.

    This function prints a message indicating that the authentication schema code
    is being generated, and then it generates the content of the authentication
    schema file using a Jinja2 template.

    Args:
        auth_model (str): The name of the authentication model.
        auth_system (str): The authentication system being used.
        login_field (str): The field used for login.
        email_is_required (bool): Whether the email field is required.
        phone_is_required (bool): Whether the phone field is required.
        username_is_required (bool): Whether the username field is required.
        verification_enabled (bool): Whether email verification is enabled.

    Returns:
        str: The generated authentication schema code as a string.
    """
    print("[yellow]Generating authentication schema code...[/yellow]")
    return generate_file_content(
        "auth_schema_template.py.jinja2",
        auth_model=auth_model,
        auth_system=auth_system,
        login_field=login_field,
        email_is_required=email_is_required,
        phone_is_required=phone_is_required,
        username_is_required=username_is_required,
        verification_enabled=verification_enabled,
    )


def configure_auth_schema_in_project(
    base_path: Path,
    auth_model: str,
    auth_system: str,
    login_field: str,
    email_is_required: bool,
    phone_is_required: bool,
    username_is_required: bool,
    verification_enabled: bool,
) -> None:
    """
    Write authentication schema to the project.

    This function generates the authentication schema code and writes it to the
    appropriate file within the project directory structure.

    Args:
        base_path (Path): The base path of the project where the authentication schema
                          file will be created.
        auth_model (str): The name of the authentication model.
        auth_system (str): The authentication system being used.
        login_field (str): The field used for login.
        email_is_required (bool): Whether the email field is required.
        phone_is_required (bool): Whether the phone field is required.
        username_is_required (bool): Whether the username field is required.
        verification_enabled (bool): Whether email verification is enabled.

    Returns:
        None
    """
    schema_path = (
        base_path / "app" / "schemas" / f"{get_plural_name(auth_model).lower()}.py"
    )
    print("[yellow]Writing authentication schema to the project...[/yellow]")
    write_file(
        schema_path,
        generate_auth_schema_code(
            auth_model=auth_model,
            auth_system=auth_system,
            login_field=login_field,
            email_is_required=email_is_required,
            phone_is_required=phone_is_required,
            username_is_required=username_is_required,
            verification_enabled=verification_enabled,
        ),
    )
    print("[green]Authentication schema written successfully[/green]")
